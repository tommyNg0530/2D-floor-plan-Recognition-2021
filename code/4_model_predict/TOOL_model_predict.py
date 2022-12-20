import tensorflow as tf
import numpy as np
import cv2 as cv
import os
from keras.preprocessing.image import load_img, img_to_array
from PIL import Image
from tqdm import tqdm


#===========================================================================================
#== tune your variable here ==============
img_path = "test_set/complicate_office_original"                        # path for input (directory)     你放置想預測既圖片的位置    **冇需要輸入directory最後既/
graph_path = "wall_model/wall_model_v2/wall_v2_model_9073/wall_v2_513x513_9073_83.pb"     # .pd model file path         你想用咩model去做prediction   **以.pb格式
pre_path = "Raw_Prediction/"                                 # path for indexed image (directory)  你想儲存raw prediction的位置 **需要輸入directory最尾既/
index_to_rgb_path = "RGB_Prediction/"                             # path for rgb output (directory)   你想儲存rgb prediction的位置 **需要輸入directory最尾既/
wall_color = [18,252,217]                                   # wall color of the rgb output    你想要咩wall的顏色
#============================================================================================

if not os.path.isdir(index_to_rgb_path):
	print("creating folder: ",index_to_rgb_path)
	os.mkdir(index_to_rgb_path)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")

if not os.path.isdir(pre_path):
	print("creating folder: ",pre_path)
	os.mkdir(pre_path)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")
#===Step 1 Generate prediction image(indexed format in png)=====================================

graph = tf.Graph()
INPUT_TENSOR_NAME = 'ImageTensor:0'
OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
graph_def = None
with tf.compat.v1.gfile.FastGFile(graph_path, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

if graph_def is None:
    raise RuntimeError('Cannot find inference graph in tar archive.')

with graph.as_default():
    tf.import_graph_def(graph_def, name='')

sess = tf.compat.v1.Session(graph=graph)
print("<<Starting to predict......>>")
for filename in os.listdir(img_path):
    prename = filename[0:-4] + ".png"   #预测输出保存为 .png格式
    file_path = img_path + "/" + filename
    save_path = pre_path + '/' + prename
    img = load_img(file_path)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0).astype(np.uint8)

    result = sess.run(
        OUTPUT_TENSOR_NAME,
        feed_dict={INPUT_TENSOR_NAME: img})

    cv.imwrite(save_path, result.transpose((1, 2, 0)))

print("\n<<Finish prediction>>")
#==================== End of step 1 ===================================

#===================Step 2 Convert indexed prediction image to RGB================================

print("<<Start recolor prediction image to RGB.....>>")

label_files = os.listdir(pre_path)
#===Step 0===file initialize

def convert_from_Indexed_to_ColorRGB(arr_3d):

    # dimension       #elements in each dimension
    for i in range(0,arr_3d.shape[0]):
        for k in range(0,arr_3d.shape[1]):
            if (arr_3d[i, k]==[1,1,1]).all():
                #print(arr_3d[i,k])
                arr_3d[i,k]= np.array(wall_color) #change all the array that are [1,1,1] to another value
    return arr_3d

for l_f in tqdm(label_files):
    img = Image.open(pre_path + l_f)
    img = img.convert('RGB')  # Make sure to confirm your image channel through arr.shape (To convert all image to 3 dimension RGB first)
    arr = np.array(img)
    #print(np.unique(arr))
    #print(arr)
    arr_3d = convert_from_Indexed_to_ColorRGB(arr)
    #print(arr_3d)
    Image.fromarray(arr_3d).save(index_to_rgb_path + l_f)

print("<<End of the recoloring>>")
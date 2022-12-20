import numpy
from PIL import Image
from tqdm import tqdm
import numpy as np
import os

#======================Set your varaiable========================================
label_dir = 'test_set/complicate_office_original/'
new_label_dir = 'test_set/complicate_office_half/'

if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")


label_files = os.listdir(label_dir)



def normalize_image_withblackspace_noResize(runtimes_x,run_times_y,image_arr):
    arr = numpy.zeros(shape=(h * (int(run_times_y) + 1), h * (int(run_times_x) + 1), 3),
                      dtype=np.uint8)  # createa array with multiple格of 513x513
    image_arr = image_arr
    # print(arr.dtype)
    #print(image_arr.shape)
    #print(arr.shape)
    # print(image_arr.dtype)
    # assign the value of image_array to created 0 filled array
    for i in range(0, img_width):
        for j in range(0, img_height):
            arr[j][i] = image_arr[j][i]
    return arr


h = 513
for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f)
    #Get width, height
    img_width,img_height = img.size
    run_times_x = img_width / h
    run_times_y = img_height / h
    image_arr = np.array(img)

    #Call function ---generate non-resize image and fit to 513by513 crop
    return_array = normalize_image_withblackspace_noResize(run_times_x,run_times_y,image_arr)
    Image.fromarray(return_array).save(new_label_dir + l_f)
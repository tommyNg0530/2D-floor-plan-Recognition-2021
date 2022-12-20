
from PIL import Image
from tqdm import tqdm
import numpy as np

import os

#======================Set your varaiable========================================

# palette (color map) describes the (R, G, B): Label pair
palette = {(  0,    0,  0) : 0 , #blackground
           ( 18,  252, 217): 1   #wall
         }

label_dir = 'tempsave/'
new_label_dir = 'temp_mod_save/'

if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")


label_files = os.listdir(label_dir)



#用呢個fucntion之前要確保image size既係 x by x, 不能用於不相等既hight & width image
def convert_from_Indexed_to_ColorRGB(arr_3d):

    # dimension       #elements in each dimension
    for i in range(0,len(arr_3d)):
        for k in range(0,len(arr_3d)):
            if (arr_3d[i, k]==[1,1,1]).all():
                #print(arr_3d[i,k])
                arr_3d[i,k]= np.array([110, 255, 43]) #change all the array that are [1,1,1] to another value
    return arr_3d



for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f)
    img = img.convert('RGB')  # Make sure to confirm your image channel through arr.shape (To convert all image to 3 dimension RGB first)
    arr = np.array(img)
    print(np.unique(arr))
    #print(arr)
    arr_3d = convert_from_Indexed_to_ColorRGB(arr)
    #print(arr_3d)
    Image.fromarray(arr_3d).save(new_label_dir + l_f)
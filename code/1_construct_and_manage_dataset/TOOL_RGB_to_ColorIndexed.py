
from PIL import Image
from tqdm import tqdm
import numpy as np

import os, shutil

# Create a dictionary type to save the  rgb and indexed label
# palette (color map) describes the (R, G, B): Label pair
palette = {(  0,    0,  0) : 0 , # blackground
           #(18,  252, 217) : 1,  # wall
           (247, 96, 142)  : 1   # window & door
         }

def convert_from_RGB_to_indexed(arr_3d):

    #create an array that fill by 0 value
    arr_2d = np.zeros((arr_3d.shape[0], arr_3d.shape[1]),           dtype=np.uint8)
                       #dimension       #elements in each dimension

    #take the dictionary items through items()
    for key, value in palette.items():
            #compare the value
        m = np.all(arr_3d == np.array(key).reshape(1, 1, 3), axis=2)
        arr_2d[m] = value
    return arr_2d

def convert_from_indexed_to_RGB(arr_3d):

    # dimension       #elements in each dimension
    for i in range(0, len(arr_3d)):
        for k in range(0, len(arr_3d)):
            if (arr_3d[i, k] == [1, 1, 1]).all():
                # print(arr_3d[i,k])
                arr_3d[i, k] = np.array([110, 255, 43])  # change all the array that are [1,1,1] to another value

    return arr_3d

#For RGB to Indexed graph
label_dir = 'door/SegmentationClassRaw/'
new_label_dir = 'door/SegmentationClass/'

#For Indexed to RGB graph
#label_dir = 'Raw_Prediction/'
#new_label_dir = 'Index_to_rgb/'


if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")


label_files = os.listdir(label_dir)

for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f)

    img = img.convert('RGB')  # Make sure to confirm your image channel through arr.shape (To convert all image to 3 dimension RGB first)
    arr = np.array(img)
    #print(np.unique(arr))
    arr_2d = convert_from_RGB_to_indexed(arr)
    #print(arr_2d.shape)
    Image.fromarray(arr_2d).save(new_label_dir + l_f) # save the converted array as a new image
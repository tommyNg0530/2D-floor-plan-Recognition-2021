from PIL import Image
from tqdm import tqdm
import numpy as np

import os, shutil

label_dir = 'tempsave/'
new_label_dir = 'filled/'


def convert_color_with_detail_RGB_value(arr_3d):
    shape = arr_3d.shape
    img_width  = shape[1]
    img_height = shape[0]
    print(arr_3d)
    print(shape)
    if img_width >= img_height:
        for i in range(0, img_width):
            for j in range(0, img_height):
                if ((arr_3d[j][i] == [255, 255, 255]).all()):
                    arr_3d[j][i] = [0, 0, 0]
                elif ((arr_3d[j][i] == [0, 0, 0]).all()):
                    arr_3d[j][i] = [12,245,136]


    else:
        for j in range(0, img_height):
            for i in range(0, img_width):
                if ((arr_3d[j][i] == [255, 255, 255]).all()):
                    arr_3d[j][i] = [0,0,0]

                elif ((arr_3d[j][i] == [0, 0, 0]).all()):
                    arr_3d[j][i] = [12,245,136]
    return arr_3d


# check if their only exist 0 and 255
def check_normalize(arr_3d):
    shape = arr_3d.shape
    print(np.unique(arr_3d))
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            arr = arr_3d[x, y]
            #print(arr)

"""
def pixel_hole_fixer(arr_3d):
    shape = arr_3d.shape
    for x in range(1, shape[0]-1):
        for y in range(1, shape[1]-1):
            arr = arr_3d[x, y]
            # not do this when the pixel is on boundary

            if ((arr==[0,0,0]).all()):
                count =0
                if ((arr_3d[x,y-1]==[255,255,255]).all()):
                    count+=1
                if ((arr_3d[x, y+1] == [255, 255, 255]).all()):
                    count += 1
                if ((arr_3d[x+1, y] == [255, 255, 255]).all()):
                    count += 1
                if ((arr_3d[x-1,y]==[255,255,255]).all()):
                    count += 1

                if count>=3:
                    arr_3d[x,y] =[255,255,255]

    return arr_3d
"""

def normalize_Black_White(arr_3d):
    shape = arr_3d.shape
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            arr = arr_3d[x, y]
            if ((arr[0]==(255,255,255)).all()):
                arr_3d[x,y]= [0,0,0]
            else:
                arr_3d[x,y]= [255,255,255]
    return arr_3d

if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")


label_files = os.listdir(label_dir)
for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f)
    img = img.convert('RGB')  # Make sure to confirm your image channel through arr_3d.shape (To convert all image to 3 dimension RGB first)
    arr_3d = np.array(img)
    print(np.unique(arr_3d))
    arr_3d = convert_color_with_detail_RGB_value(arr_3d)
    Image.fromarray(arr_3d).save(new_label_dir + l_f)

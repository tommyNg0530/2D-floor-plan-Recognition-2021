"""
 This script is doing the weight calculation while setting the inintial weighting in the utils/train_utils.py

 this script calculate the no. of classes in each indexed SEGMENTEDCLASS image
"""

import os
from tqdm import tqdm
from PIL import Image
import numpy as np

label_dir = 'door/SegmentationClassRaw/'
label_files = os.listdir(label_dir)

class_number_of_Class_0 = 0
class_number_of_Class_1 = 0


def class_calculator(arr_2d,class_index):
    count=0
    class_index=int(class_index)
    for i in range(0,len(arr_2d)):
        for j in range(0,len(arr_2d)):
            if arr_2d[i][j] == class_index:
                count += 1
    return count



for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f) # Make sure to confirm your image channel through arr.shape (Need to be indexed image 8 uint)
    arr_2d = np.array(img).tolist()
    #print(arr_2d)
    #classes = np.unique(arr)
    #arr_2d.shape
    #print(arr_2d[0][0])
    no_of_index_0 = class_calculator(arr_2d,0)
    no_of_index_1 = class_calculator(arr_2d,1)
    class_number_of_Class_0 += no_of_index_0
    class_number_of_Class_1 += no_of_index_1
    print(class_number_of_Class_0)
    print(class_number_of_Class_1)

print()
print("Class 0: "+ str(class_number_of_Class_0))
print("Class 1: "+ str(class_number_of_Class_1))
print("Weight ratio(0/1): "+str(class_number_of_Class_0/class_number_of_Class_1))
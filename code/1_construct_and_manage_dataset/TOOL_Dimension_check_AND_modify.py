import cv2
from PIL import Image
from tqdm import tqdm
import numpy as np
import os, shutil


label_dir = 'door/SegmentationClassRaw/'
new_label_dir = 'door/SegmentationClassRaw/'  #the directory that you want to save the file after changing channel
if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)


label_files = os.listdir(label_dir)
new_label_filies = os.listdir(new_label_dir)

for l_f in label_files:
    img = Image.open(label_dir + l_f)
    arr_show = np.array(img)
    print(arr_show.shape)
    print(np.unique(arr_show))
x = input("\n--Do i need to modify all image to RGB --?(y/n)")

if ((x=="y" or x=="Y")):
    for l_f in tqdm(label_files):
        img = Image.open(label_dir + l_f)
        img = img.convert('RGB')
        arr = np.array(img)
        print(arr.shape)
        Image.fromarray(arr).save(new_label_dir + l_f)
        img.close()
else:
    print("\n--Choose end---")

y = input("\n--Do i need to resize all image --?(y/n)")
if (y == "y" or y == "Y"):
    for l_f in tqdm(os.listdir(label_dir)):
        img = cv2.imread(label_dir + l_f, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (513, 513))
        arr = np.array(img)
        print(arr.shape)
        Image.fromarray(arr).save(new_label_dir + l_f)
else:
    print("\n--program end---")



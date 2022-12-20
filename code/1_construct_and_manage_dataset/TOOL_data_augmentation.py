import cv2
import numpy as np
from PIL import Image
import os
import glob
from tqdm import tqdm

folder = "JPEGImages"
#folder = "SegmentationClass"
#folder = "SegmentationClassRaw"


inputFolder = "wall/"+folder+"/"
new_label_dir = "wallv2/"+folder+"/"

if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)

#Generate 90 degree rotation for an image, one image rotate 3 times
for img in tqdm(os.listdir(inputFolder)):
	image = cv2.imread(inputFolder+img)
	height, width = image.shape[:2]
	center = (width/2, height/2)
	x=0
	for i in range(1,5):
		rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=x, scale=1)
		rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
		x += 90
		#cv2.imshow("da",image)
		#cv2.waitKey(0)
		cv2.imwrite(new_label_dir+ str(i) +"_"+img, rotated_image)


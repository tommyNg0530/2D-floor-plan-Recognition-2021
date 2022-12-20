import os
from PIL import Image
import tqdm
import numpy as np
import cv2
folder = "prediction_results/"
m_folder = "prediction_results/"

image=[]
mask=[]
for filename in os.listdir(folder):
    img = cv2.imread(folder+filename,cv2.IMREAD_GRAYSCALE)
    print(img.shape)
    cv2.imshow("img",img)
    cv2.waitKey(0)


for filename in os.listdir(m_folder):
    img = cv2.imread(folder+filename,cv2.IMREAD_UNCHANGED)










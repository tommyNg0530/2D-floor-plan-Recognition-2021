
from PIL import Image
from tqdm import tqdm
import numpy as np
import os

#======================Set your varaiable========================================
label_dir = 'test_set/complicate_office_half/'
new_label_dir = 'test_set/complicate_office_crop/'
if not os.path.isdir(new_label_dir):
	print("creating folder: ",new_label_dir)
	os.mkdir(new_label_dir)
else:
	print("Folder alread exists. Delete the folder and re-run the code!!!")
label_files = os.listdir(label_dir)
print(label_files)
#======================End of Set your varaiable========================================

def image_513by513_croping(filename,run_times_x,run_times_y,crop_size,img):
    crop_size = crop_size
    x=0
    y=0
    filename = filename.split(".")
    print(filename[0])
    #print(filename[1])
    #Crp[ the image
    for i in range(0,run_times_y):
        for j in range(0,run_times_x):
            crop_image = img.crop((x,y,x+crop_size,y+crop_size))
            crop_image.save(new_label_dir +filename[0]+"_" + str(i+1)+"_"+str(j+1)+"."+filename[1])
            print("Image:"+l_f+" Crop no:"+"width("+str(j+1)+")"+" & height("+str(i+1)+")")
            x += crop_size
        x=0             #reset width
        y += crop_size  #increment height


size = 513
for l_f in tqdm(label_files):
    img = Image.open(label_dir + l_f)
    image_arr = np.array(img)
    img_width, img_height = img.size
    run_times_x = int(img_width / size)
    run_times_y = int(img_height / size)
    # print(run_times_x)
    #print(run_times_y)
    #Call function ---generate 513by513 crop
    return_array = image_513by513_croping(l_f,run_times_x,run_times_y,size,img)

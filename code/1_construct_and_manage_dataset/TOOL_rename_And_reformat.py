
import os
from PIL import Image

path = "door/SegmentationClassRaw/"
location = path

print("here are all the file format in the dir>>")
for count, filename in enumerate(os.listdir(path)):
    img = Image.open(path+str(filename))
    print(img.format)
    img.close()
print("====End of file listing====")

rename = input("If rename all file? (y/n)")
if (rename=="y" or rename=="Y"):
    for count, filename in enumerate(os.listdir(path)):
        src = path + filename
        filename = filename.split("_json")
        dst = str(filename[0]+filename[1])
        dst = path + dst

        # rename() function will
        # rename all the files
        os.rename(src, dst)

reformat = input("If reformat all files? (y/n)")
if (reformat == "y" or reformat == "Y"):

    format = str(input("Please input the format of the file:"))

    #e.g.  dir/dir/

    for count, filename in enumerate(os.listdir(path)):
        img = Image.open(path + str(filename))
        filename = filename.split(".")
        print(filename[0])
        img.save(location + str(filename[0]) + "."+format)

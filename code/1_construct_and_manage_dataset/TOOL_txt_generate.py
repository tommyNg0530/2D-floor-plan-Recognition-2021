import os

folder = "door_v2/JPEGImages/"
m_folder = "door_v2/SegmentationClass/"

print("This tool will generate three .txt file:"+ "\n  [train.txt]  \n  [val.txt]   \n  [trainval.txt]")

x= 0.8

# =======Sort the file name in ascending order==============

image_nameList = []
mask_nameList = []

for filename in os.listdir(folder):
    name = filename
    image_nameList.append(name)

for filename in os.listdir(m_folder):
    name = filename
    mask_nameList.append(name)



if len(image_nameList) == len(mask_nameList):
    cutting_index = int(len(mask_nameList)*x)
    print("Number of train image: "+ str(cutting_index))
    print("Number of val image: " + str(len(mask_nameList)-cutting_index))
    with open("train.txt","w") as f:
        for i in range(cutting_index):
            temp = image_nameList[i].split(".jpg")
            f.write(str(temp[0])+"\n")

    with open("val.txt","w") as f:
        for i in range(cutting_index,len(mask_nameList)):
            temp = image_nameList[i].split(".jpg")
            f.write(str(temp[0]) + "\n")

    with open("trainval.txt","w") as f:
        for i in range(len(mask_nameList)):
            temp = image_nameList[i].split(".jpg")
            f.write(str(temp[0]) + "\n")
    #======Combine both train and val list
    print("\nTool execute without bug")

else:
    print("\nTool unable to execute, please confirm the number of image are the same from two folders")

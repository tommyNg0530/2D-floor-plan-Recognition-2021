import os

folder = "wall_image/"
m_folder = "wall_mask/"

# =======Sort the file name in ascending order==============

image_nameList = []
mask_nameList = []

for filename in os.listdir(folder):
    name = filename
    image_nameList.append(name)

for filename in os.listdir(m_folder):
    name = filename
    mask_nameList.append(name)

image_nameList.sort()
mask_nameList.sort()

print(image_nameList)
print(mask_nameList)

# check if every index of two list is the same
for i in range(len(image_nameList)):
    if (image_nameList[i] != mask_nameList[i]):
        print("Warning! the index " + str(i + 1) + " is wrong")

print("If no warning, then these two file is save")
"""#============================
# This tool help you gather all label files to one directory after you generate
# a tons of json_dir by previous tool multi_json_label...
# Not limit to specific file, all file capable to use
"""

import os
import shutil

path ="door/labelme_dir/"                        #your path that save your all json filies generate by labelme
json_files_list = os.listdir(path)
path_for_Save_image_copies="door/SegmentationClass/"    #position to place your file
file_that_you_want_to_move = "/label.png"                  # file that you wanna select()

if not os.path.isdir(path_for_Save_image_copies):
	print("creating folder: ",path_for_Save_image_copies)
	os.mkdir(path_for_Save_image_copies)
else:
	print("Folder alread exists.")


for file in json_files_list:
    if os.path.isdir(os.path.join(path,file)):
        shutil.copy(os.path.join(path,file+file_that_you_want_to_move), path_for_Save_image_copies)
        os.rename(path_for_Save_image_copies+file_that_you_want_to_move,path_for_Save_image_copies+file+".png")

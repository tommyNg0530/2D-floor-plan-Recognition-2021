"""

    This script require a labelme interpretor to run !!!

"""
import os

path ="door/labelme_dir"
json_file = os.listdir(path)
os.system("activate labelme")
for file in json_file:
    os.system("labelme_json_to_dataset.exe %s"%(path + '/' + file))










"""



"""


# importing the module
import cv2
import numpy as np

#====for warning message color
class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    FAIL = '\033[91m'
#====End of setting warning color


#======= Variable setting here   ============================================================================
coord_list = []
color_of_the_drawing =(217, 252, 18)  # the color of the draw pen
image_path = 'mimi_colour.jpg'  # file_dir
save_path = 'mimi_colour.jpg'  # file_save

#======= End of variable setting ===========================================================================

#=======Start of [ Drawing function] ================================================================================
def draw_rectangle(coord_list):
    try:
        if controller == "draw_rectangle":
            #print(coord_list[0],coord_list[1])
            cv2.rectangle(img,(coord_list[0][0],coord_list[0][1]),(coord_list[1][0],coord_list[1][1]),(217, 252, 18),-1)

        elif controller =="draw_black":
            cv2.rectangle(img, (coord_list[0][0], coord_list[0][1]), (coord_list[1][0], coord_list[1][1]),(0, 0, 0), -1)
    except:
        print("\n")
        print(bcolors.FAIL+"You only select one points!"+ bcolors.ENDC)
        print(bcolors.WARNING+"Please Re-select two points before RightCLick & generate the draw"+ bcolors.ENDC)

#=======End of [ Drawing function] ================================================================================
'''
def draw_point(x,y):
    cv2.circle(img,(x,y),4,(0,72,255),-1)'''
def coord_order(list):
    i=0
    x1=list[i][0]
    y1=list[i][1]
    x2 = list[i+1][0]
    y2 = list[i+1][1]
    width = abs(x1-x2)
    height = abs(y1-y2)
    if x2<x1:
        x1=x2
    else:
        x1=x1
    if y2 < y1:
        y1 = y2
    else:
        y1 = y1
    return x1, y1, width, height

def save_for_recover(img,temp_save_record):
    x1,y1,width,height = coord_order(list)
    save_to_recover = img[y1:y1+height , x1:x1+width]
    return save_to_recover

#===========[Click event function]===================================================================
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(coord_list)<2:
            coord_list.append([x, y])
        else:
            print(bcolors.FAIL + "<<You have selected two points already>>" + bcolors.ENDC)
            print(bcolors.WARNING+"Please <Right-Click> to generate drawing / click <d> to clear all selected point"+ bcolors.ENDC)
            print()

    if event == cv2.EVENT_RBUTTONDOWN:
        draw_rectangle(coord_list)
        cv2.imshow(image_path, img)
        #temp_save_coord = coord_list.append()
        coord_list.clear()
        print("<<Rectangle drew>>")

#===========End of [Click event function]===================================================================

img = cv2.imread(image_path, 1)
img_in_np = np.float32(img)  #for action recover usage
cv2.namedWindow(image_path, 0)
cv2.resizeWindow(image_path, 900,900)
cv2.setMouseCallback(image_path, click_event)

controller = "draw_rectangle" # default pen
temp_save_coord=[]
temp_save_crop_img = []

while True:
    cv2.imshow(image_path,img)
    if cv2.waitKey(0) & 0xFF == ord("s"):
        cv2.imwrite(save_path, img)
        break

    elif cv2.waitKey(0) & 0xFF == ord("q"):
        break

    elif cv2.waitKey(0) & 0xFF ==ord("r"):
        break

    elif cv2.waitKey(0) & 0xFF == ord("c"):
        if controller == "draw_rectangle":
            controller = "draw_black"

        elif controller =="draw_black":
            controller = "draw_rectangle"
        print("<<Pen Changed to ["+controller+"]>>")

    elif cv2.waitKey(0) & 0xFF == ord("d"):
        coord_list=[]
        print("<<All selected point has been cleaned>>")

cv2.destroyAllWindows()
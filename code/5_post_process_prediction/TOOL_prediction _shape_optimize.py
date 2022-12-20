import cv2
import numpy as np
import os


#==================================================================================================================================================================
#<Part> Variable setting
epsilon_value=0.001                         #<tunable> this parameter to change the [[sensitivity of finding approx shape from contours]],
                                            #                                         [lower = more fit object's original shape] [higher = more abstract shape]
threshold_value_rectangle = 0.88            #<tunable> The minimum cover rate of a object to be determined as rectangle
threshold_noise_filter_when_Draw_box = 3    #<tunable> Prevent Noise point being detected, the object's area that lower than

img = cv2.imread('filled/Filterd_result.png') #Image that you want to input
save_path = "filled/"                         #Enter a directory to save all the image

#output control (Enter string "yes" to save that as a output)
save_img_with_boundaries = "yes"   #will still show, but no save if not yes
save_img_only_boundaries = "yes"
save_img_only_boundaries_filled = "yes"         #will not show & save
show_approx = "yes"                             #Enter to show approx contours
#==================================================================================================================================================================
if not os.path.isdir(save_path):
    print("creating folder: ",save_path)
    os.mkdir(save_path)

#<Part> Find contours
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)   #Need to be binary image(black & white)`
        # 4 variable can change(Refer tohttps://blog.csdn.net/hjxu2016/article/details/77833336)
        # contours => all object's contours in a list, can access each object's contour independently
length = len(contours)
print("Number of contours:" + str(length))

#==================================================================================================================================================================

#<Part> Shoelace formula [for calculate polygon's area]
def polygonArea(X, Y, n):                     #Recieve x_coord_list, y_coord_list & number of vertices
    # Initialize area
    area = 0.0
    # Calculate value of shoelace formula
    j = n - 1
    for i in range(0, n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i  # j is previous vertex to i
    # Return absolute value
    return int(abs(area / 2.0))

#<Part> Self-made algorithm
#       aim to optimize the object that determine as polygon with smooth line
#       accept two input (the approx to accept the approximate vertex from cv2.approxPolyDP)
#                        (approx_area is the area of the polygon object calculate by polygonArea algorithm, used to determine the threshold value based on object size)
def polygon_optimize(approx,approx_area):
    object_size = approx_area
    approx_save = np.array(approx)  #use to separate original approx & prevent change its value
    threshold_distance = 0
    #<Part> Decide threshold value based on object size
    #if object size input
    if object_size != None:
        if object_size < 4000:
            threshold_distance = 3     #<tunable>
        elif object_size>4000:
            threshold_distance = 50    #<tunable>  X/Y Difference smaller than this value will be
    print(threshold_distance)
    #<Part> Initialization
    start_vertex_x = approx[0][0][0]
    start_vertex_y = approx[0][0][1]
    best_fit_polygon = []
    best_fit_polygon.append([start_vertex_x, start_vertex_y]) #append the first vertex from approx

    #<Part> Access each vertex of a object
    for m in range(len(approx_save)-1):
        vertex_x1 = approx_save[m][0][0]
        vertex_y1 = approx_save[m][0][1]
        vertex_x2 = approx_save[m+1][0][0]
        vertex_y2 = approx_save[m+1][0][1]
        x_diff = vertex_x1 - vertex_x2
        y_diff = vertex_y1 - vertex_y2
        #<Part> Through slope to determine use x/y_diff as indicator
        if x_diff == 0:
            checker = "vertical"
        else:
            slope = y_diff/x_diff
            if slope == 0:
                checker = "horizontal"
            elif slope > 0:
                if slope > 1.19:                #<tunable> greater than 50 incline angle
                    checker = "vertical"
                elif slope < 0.839:             #<tunable> smaller than 40 incline angle0.839
                    checker = "horizontal"
                else:
                    checker = "slash"
            elif slope < 0:
                if slope > -1.19:                 #<tunable> smaller than 40 incline angle -1.19
                    checker = "horizontal"
                elif slope < -0.839:               #<tunable> greater than 50 incline angle -0.839
                    checker = "vertical"
                else:
                    checker="slash"

        #<Part> Determine x/y_diff should be watch based on slope
        if checker   == "horizontal":
            watch_value = x_diff
        elif checker == "vertical":
            watch_value = y_diff
        elif checker == "slash":
            watch_value = threshold_distance+1 # +1 just make it 100% pass the test

        #<Part> Determine whether the vertex should be keep or not
        if watch_value > threshold_distance:
            best_fit_polygon.append([vertex_x2,vertex_y2])
        else:
            #remove that vertex from approx
            if checker == "horizontal":
                approx_save[m+1][0][1] = approx_save[m][0][1]
                best_fit_polygon.append([vertex_x2, vertex_y1])
            elif checker == "vertical":
                approx_save[m+1][0][0] = approx_save[m][0][0]
                best_fit_polygon.append([vertex_x1, vertex_y2])
            continue

    return best_fit_polygon

#==================================================================================================================================================================

#<Part> Control output
if save_img_only_boundaries == "yes":
    # Initialize a blank image same with input img [To generate a img only save those boundaries]
    blank_image_only_boundaries = np.zeros((img.shape[0], img.shape[1], 3))
if save_img_only_boundaries_filled == "yes":
    blank_image_FILLED = np.zeros((img.shape[0], img.shape[1], 3))
if show_approx == "yes":
    img_approx = np.array(img)  #use to show approx

#==================================================================================================================================================================

#<Part> Access each object contours & do action
for i in range(length-1):  # The -1 is prevent showing the outermost boundary

    #<Part> find approximate points to represent a contour
    cnt = contours[i]                              #access the object[i]'s contours by getting it from findcontours above
    epsilon = epsilon_value * cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)  #會將一個object近似既shape以x,y coord既format, clockwise咁以list return番嚟
    number_of_vertices = len(approx)
    #calculate object's approx area from the points obtained in approxPolyDP
    print("\nNumber of vertices: " + str(number_of_vertices))

    #<Part> fill in the the vertices into X & Y list and input it into polygonArea
    x_list = []
    y_list = []
    for x in range(number_of_vertices):
        x_list.append(approx[x][0][0])
        y_list.append(approx[x][0][1])
    approx_area = polygonArea(x_list, y_list, number_of_vertices)
    print("Area of the object ["+str(i+1)+"] is = "+str(approx_area))
    #cv2.drawContours(img, approx, -1, (0, 0, 255), 3) #show contour points that find by approxPolyDP


    #<Part> Rectangle bounding box for rectangle-like object
    rect = cv2.minAreaRect(cnt)                    #Receive contour and generate minimum rectangle to bound the object
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #print(box)
    x_list_box = []
    y_list_box = []
    for x in range(4):
        x_list_box.append(box[x][0])
        y_list_box.append(box[x][1])
    rectangle_area = polygonArea(x_list_box, y_list_box, 4)

    #<Part> Calculate the Rectangle boundary box's cover rate [To filter non-rectangle object]
    boundary_cover_rate = approx_area / rectangle_area
    print("Area of the rectBoundary [" + str(i + 1) + "] is = " + str(rectangle_area))
    print("Cover rate of the rectangle boundary box: "+str(boundary_cover_rate))

    #<Part> Determine shape & further action
    if approx_area > threshold_noise_filter_when_Draw_box: #Prevent Noise point being detected
        #<Part> Shape optimize
        threshold_rectangle = threshold_value_rectangle

        #Rectanle case
        if boundary_cover_rate > threshold_rectangle:
            cv2.drawContours(img, [box], -1, (111 , 111, 252), thickness=2) #<tune> thickness -1 mean filled
            #Extra action if want to save boundaries only output
            if save_img_only_boundaries == "yes":
                cv2.drawContours(blank_image_only_boundaries, [box], -1, (111, 111, 252), thickness=2)              # draw same boundaries on the blank_image_only_boundaries image
            if save_img_only_boundaries_filled == "yes":
                cv2.drawContours(blank_image_FILLED, [box], -1, (111, 111, 252),thickness=-1)                       # draw same boundaries on the blank_image_FILLED image
            if show_approx == "yes":
                cv2.polylines(img_approx, [approx], True, (0, 0, 255), 2)
            #cv2.rectangle(img, [approx], True, (0, 0, 255), 2)

        #Polygon case
        elif boundary_cover_rate < threshold_rectangle:
            simplify_polygon = polygon_optimize(approx,approx_area)
            simplify_polygon = np.array(simplify_polygon, np.int32)
            print(simplify_polygon)
            cv2.drawContours(img, [simplify_polygon], -1, (255, 0, 191), thickness=2)
            if save_img_only_boundaries == "yes":
                cv2.drawContours(blank_image_only_boundaries, [simplify_polygon], -1, (255, 0, 191), thickness=2)  # draw same boundaries on the blank_image_only_boundaries image
            if save_img_only_boundaries_filled == "yes":
                cv2.drawContours(blank_image_FILLED, [simplify_polygon], -1, (111, 111, 252),thickness=-1)         # draw same boundaries on the blank_image_FILLED image
            if show_approx == "yes":
                cv2.drawContours(img_approx, [approx], -1, (202, 10, 255), thickness=4)  # show approx points

        #Non closed shape structure
        else:
            break
        #for showing the object id nearby the object
        #cv2.putText(img, str(i+1), (approx[0][0][0], approx[0][0][1] + 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2,cv2.LINE_AA)


#<Part> Show image here
print("<<Finish>>")
cv2.namedWindow("Image with boundaries", 0)
cv2.resizeWindow("Image with boundaries", 900,900)
cv2.imshow("Image with boundaries", img)

if show_approx=="yes":
    cv2.namedWindow("Original image", 0)
    cv2.resizeWindow("Original image", 900,900)
    cv2.imshow("Original image", img_approx)

if save_img_only_boundaries == "yes":
    cv2.namedWindow("Boundaries only", 0)
    cv2.resizeWindow("Boundaries only", 900,900)
    cv2.imshow("Boundaries only", blank_image_only_boundaries)

if save_img_only_boundaries_filled == "yes":
    cv2.namedWindow("Boundaries filled", 0)
    cv2.resizeWindow("Boundaries filled", 900,900)
    cv2.imshow("Boundaries filled", blank_image_FILLED)

#<Part> Control the output
if save_img_with_boundaries == "yes":
    cv2.imwrite(save_path+"img_with_boundaries.png", img)
if save_img_only_boundaries_filled == "yes":
    cv2.imwrite(save_path+"img_only_filled_boundaries.png", blank_image_FILLED)
if save_img_only_boundaries == "yes":
    cv2.imwrite(save_path + "img_only_boundaries.png", blank_image_only_boundaries)

cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

#======================== Start of Step 1 [connectedComponentsWithStats](For removing redundant pixel dots)=============================================
img = cv2.imread('mimi_colour.jpg', cv2.IMREAD_GRAYSCALE)
ret, binary_map = cv2.threshold(img,127,255,0) #turn image to black white binary image

# do connected components processing
nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_map, None, None, None, 8, cv2.CV_32S)
#get CC_STAT_AREA component as stats[label, COLUMN]
areas = stats[1:,cv2.CC_STAT_AREA]
result = np.zeros((labels.shape), np.uint8)
for i in range(0, nlabels - 1):
    if areas[i] >= 100:   #keep
        result[labels == i + 1] = 255

img=result
#======================== End of Step 1 =============================================

#======================== Start of step 2  [dilation] (for increase wall thickness) ==========================================
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

#======================== End of step 2   ===========================================

#cv2.imshow("Binary", binary_map)
#cv2.imshow("Result", result)
#cv2.imshow("Dilated",img)

#========================= Start of step 3 ==========================================
#img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  #opening
#========================= End of step 3 ==========================================


filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# Applying cv2.filter2D function on our Cybertruck image
img = cv2.filter2D(img,-1,filter)

#img = cv2.GaussianBlur(img,(13,13),0

img = cv2.dilate(result,kernel,iterations = 1)
cv2.imshow("OPENED",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)  # for change the save image format
cv2.imwrite("tempsave/Filterd_result3.png", img)

"""
          
#

cv2.imshow('opening', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
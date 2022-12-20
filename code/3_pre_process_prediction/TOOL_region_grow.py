import numpy as np
import cv2

#================ Set your variables ======================

image_path = 'mimi_colour.jpg'
save_path  = 'tempsave/growed_image.jpg'

#================ End of setting the variables ============


#================ Algorithm ~~~ refer to [region growing] ====
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def getGrayDiff(img, currentPoint, tmpPoint):
    return abs(int(img[currentPoint.x, currentPoint.y]) - int(img[tmpPoint.x, tmpPoint.y]))


def selectConnects(p):
    if p != 0:
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), \
                    Point(0, 1), Point(-1, 1), Point(-1, 0)]
    else:
        connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    return connects


def regionGrow(img, seeds, thresh, p=1):
    height, weight = img.shape
    seedMark = np.zeros(img.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)
    label = 1
    connects = selectConnects(p)
    while (len(seedList) > 0):
        currentPoint = seedList.pop(0)

        seedMark[currentPoint.x, currentPoint.y] = label
        for i in range(8):
            tmpX = currentPoint.x + connects[i].x
            tmpY = currentPoint.y + connects[i].y
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                continue
            grayDiff = getGrayDiff(img, currentPoint, Point(tmpX, tmpY))
            if grayDiff < thresh and seedMark[tmpX, tmpY] == 0:
                seedMark[tmpX, tmpY] = label
                seedList.append(Point(tmpX, tmpY))
    return seedMark

#===============End of region growing=======================

#====

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        seeds.append(Point(x, y))


    if event == cv2.EVENT_RBUTTONDOWN:
        print("<<Region grow is loading....>>")
        binaryImg = regionGrow(img, seeds, 10)
        cv2.imshow("output", binaryImg)
        print("<<Region grow is finish>>")

        cv2.imwrite(save_path, binaryImg)


#====

ori_img = cv2.imread(image_path,1)  #read as gray image

cv2.namedWindow("original image",0)
cv2.resizeWindow("original image", 800,800)
cv2.imshow("original image",ori_img)

seeds = [Point(10, 10), Point(82, 150), Point(20, 300)] #Point(10, 10), Point(82, 150), Point(20, 300)
img = cv2.imread(image_path,0)
img = regionGrow(img, seeds, 10)
cv2.imwrite(save_path, img)


cv2.namedWindow("output",0)
cv2.resizeWindow("output", 800,800)
cv2.imshow('output', img)
cv2.setMouseCallback('output', click_event)

cv2.waitKey(0) & 0xFF

while True:
    if cv2.waitKey(0) == ord("s"):
        break
    elif cv2.waitKey(0) == ord("q"):
        break
    elif cv2.waitKey(0) == ord("c"):

        print("<<Previous click record clear>>")

cv2.destroyAllWindows()
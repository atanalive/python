import cv2 as cv

img = cv.imread("alive.jpg", 1)
# img = cv.resize(img, (900, 900))
# img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
cv.imwrite("alive.png", img)


#1) importing libraries
import cv2                 # importing opencv library (image recog., image preprocessing)
import numpy as np         # importing numpy(to solve mathematical expression)

#2) taking image 
img = cv2.imread("rat.jpg")

# 3) Edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #converting to gray-scale
gray = cv2.medianBlur(gray, 5)                  #giving blur
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)   #defining image borders

# 4) Color
color = cv2.bilateralFilter(img, 9, 300, 300)       # assighning weights

# 5) Cartoon
cartoon = cv2.bitwise_and(color, color, mask=edges)  #image masking(applying algo for cartoonifying)

# 6) display
cv2.imshow("Image", img)
cv2. imshow("Edges", edges)
cv2. imshow("color", color)
cv2.imshow("Cartoon", cartoon)
cv2.imwrite("rat1.jpg",img)              #saving cartoon image in same folder
cv2.waitKey(0)
cv2.destroyAllWindows()


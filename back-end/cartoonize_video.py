#clone the github repository of original implementation of White-box-Cartoonization by Xinrui Wang and Jinze Yu.
!git clone --branch inference-tf-2.x https://github.com/steubk/White-box-Cartoonization.git

%tensorflow_version 1.x

import sys
sys.path.append('./White-box-Cartoonization/test_code')           #path-1  
import os
import matplotlib.pyplot as plt
import cartoonize
import tensorflow as tf 
from PIL import Image


#create a directory to upload the video
!mkdir -p ./video_input
!mkdir -p ./video_output


# Opens the Video file
import cv2
cap= cv2.VideoCapture('/content/vid.mp4')            #endpoint-1(giving video input for cartoonizing)
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('/content/video_input/sample'+str(i)+'.jpg',frame)        #path-2
    i+=1
 
cap.release()
cv2.destroyAllWindows()


#test the model with sample data
import os

model_path = './White-box-Cartoonization/test_code/saved_models'         #path-3
load_folder = './video_input'                                            #path-4
save_folder = './video_output'                                           #path-5
if not os.path.exists(save_folder):
    os.mkdir(save_folder)
    
cartoonize.cartoonize(load_folder, save_folder, model_path)



import cv2
import numpy as np
import os
 
from os.path import isfile, join
 
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    os.chdir("/content/video_output/")                           #path-6
      
    images = [img for img in os.listdir('.') 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
 
    #for sorting the file names properly
    files = sorted(images)
 
    for i in range(len(files)):
        filename=pathIn +"/" + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
 
def main():
    pathIn= '/content/video_output'                               #path-7
    pathOut = '/content/video.avi'                                #path-8
    fps = 25.0
    convert_frames_to_video(pathIn, pathOut, fps)
 
if __name__=="__main__":
    main()

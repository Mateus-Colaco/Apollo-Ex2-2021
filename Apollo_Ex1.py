# -*- coding: utf-8 -*-
"""CountPeople.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oQXeWMhBDhMU8ym6WnAlpJAy0djULTw2
"""

# Commented out IPython magic to ensure Python compatibility.
#!pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from google.colab.patches import cv2_imshow
from IPython.display import Image, clear_output
import os
from PIL import Image
from moviepy.editor import *

def ShrinkVideo(orig_video_path,path_shrinked,size_X,size_Y,fps): #Shrink size (X,Y) of video
    cap = cv2.VideoCapture(orig_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path_shrinked,fourcc,fps,(size_X,size_Y))
    while True:
      success,frame = cap.read()
      if not success:
        break
      else:
        frame_resized = cv2.resize(frame,(size_X,size_Y),fx=0,fy=0,interpolation = cv2.INTER_CUBIC)
        out.write(frame_resized)
    cap.release()
    out.release()

    return path_shrinked


def defModel(video_to_frame_path,custom_or_model,weights='',track =''):
  new_cap = cv2.VideoCapture(video_to_frame_path)
  frames_to_video = list()
  
  if weights == '':
    model = torch.hub.load('ultralytics/yolov5', custom_or_model)
    model.classes = [0]
  else:
    model = torch.hub.load('ultralytics/yolov5', custom_or_model,weights)
    
  while True:
    success,frames = new_cap.read()

    if not success:
      break
    
    bounding_box = model(frames)
    a = bounding_box.pandas()
    if weights =='':
      text = 'People:' + str(np.shape(a.xywh)[1])
    else:
      text = 'Number of Guns:' + str(np.shape(a.xywh)[1])
    cv2.putText(bounding_box.render()[0],text,(325,25),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
    frames_to_video.append(np.array(bounding_box.render()[0]))

  return frames_to_video


def writevideo(frames_to_video,size_X,size_Y,fps):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    final_video_base = cv2.VideoWriter('final_video.mp4',fourcc,fps,(size_X,size_Y))

    for frame in frames_to_video:
      final_video_base.write(frame)

    final_video_base.release()

    return final_video_base


if __name__ == "__main__":

  
  video_to_frame,video_to_frame_path = ShrinkVideo('/content/video_ex01.mp4')
  #video to split in frames
  new_cap = cv2.VideoCapture(video_to_frame_path)

  
  model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
  model.classes = [0] #Detect only People

  frames_from_video = frameArray(new_cap)
  final_video       = writevideo(frames_from_video)

  final_video = VideoFileClip('/content/final_video.avi')
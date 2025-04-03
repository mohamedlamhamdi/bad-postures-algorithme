import math
import cv2
import numpy as np
from time import time
import mediapipe as mp    # type: ignore
from utils import Alert,limit_lit,decision_bed,calculateAngle,classifyPose # type: ignore

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils 

cap = cv2.VideoCapture(0)
Tn_1=time()
fps=0
g_lit=[200,100,200,550] #gauche
d_lit=[600,100,600,550]  #droite
l_haut=[g_lit[0],g_lit[1],d_lit[0],g_lit[1]]
l_bas=[g_lit[0],d_lit[3],d_lit[0],d_lit[3]]

while True:
    _, img = cap.read()
    img = cv2.resize(img,(720,600))
    height,width,_ = img.shape
    #print(img.shape)
    #frames calculation
    Tn=time()
    diff=Tn-Tn_1
    fps=0.9*fps + 0.1/diff
    cv2.putText(img,"FPS : "+str(int(fps)),(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    Tn_1=time()
    
    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    landmarks=[]
    if results.pose_landmarks:
    
    # Draw Pose landmarks on the sample image.
        mp_drawing.draw_landmarks(image=img, landmark_list=results.pose_landmarks,
                              connections=mp_pose.POSE_CONNECTIONS)
         # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    try: 
        dist1=limit_lit(height,width,g_lit[0],g_lit[3]//2,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]) 
        dist2=limit_lit(height,width,d_lit[0],d_lit[3]//2,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
        decision_bed(dist1,dist2) 
        v,img=classifyPose(landmarks,img)
        if v!="Unknown Pose":
           Alert(v)
    except  IndexError :
        pass  
    cv2.line(img,(g_lit[0],g_lit[1]),(g_lit[2],g_lit[3]),(255,0,0),4)
    cv2.line(img,(d_lit[0],d_lit[1]),(d_lit[2],d_lit[3]),(255,0,0),4)
    cv2.line(img,(l_haut[0],l_haut[1]),(l_haut[2],l_haut[3]),(255,0,0),4)
    cv2.line(img,(l_bas[0],l_bas[1]),(l_bas[2],l_bas[3]),(255,0,0),4)
    cv2.imshow('img',img)
    #print(img.shape)
    if cv2.waitKey(1) == ord('q'):
       break    
cap.release()
cv2.destroyAllWindows()



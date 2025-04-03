import math
import cv2
import numpy as np
from time import time
import mediapipe as mp   # type: ignore
mp_pose = mp.solutions.pose
def Alert(string):
    print(string)
    
def limit_lit(h,w,l_x,l_y,landmark):
    x0, y0, _ = landmark
    x0,y0=x0/w,y0/h
    x1,y1=l_x/w,l_y/h  #normalisation des coordonnées
   # dist=((x0-x1)**2+(y1-y0)**2)**0.5 
    dist=abs(x0-x1)
    return(dist)
def decision_bed(dist1,dist2):
   limit=0.28
   if dist1 < limit :
        Alert("about to fall from the left")
   if dist2 < limit :   
        Alert("about to fall from the right") 
   if dist1 > limit and dist2 > limit :
       print("normal")
              

def calculateAngle(landmark1, landmark2, landmark3):
    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        # Add 360 to the found angle.
        angle += 360

    return angle              

def classifyPose(landmarks, output_image):
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)
     # Get the angle between the left hip, knee and ankle points. 
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points 
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    # Angles des hanches
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    
    # Angles des coudes
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    
    # Angles des épaules
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
    
    if ( right_hip_angle > 10 and right_hip_angle < 90 ) or ( left_hip_angle > 20 and left_hip_angle < 90 ):
        if ( right_knee_angle > 30 and right_knee_angle < 120) or ( left_knee_angle > 30 and left_knee_angle < 120 ) :
            label="GENOUX LEVER MAUVAISE POSITION"
    
    if ( right_hip_angle> 20  and right_hip_angle < 150 ) and ( left_hip_angle > 20 and left_hip_angle < 150 ) :
            label="GENOUX"
     # Critères pour la détection de la position "GENOUX LEVER MAUVAISE POSITION"
    if (right_knee_angle > 30 and right_knee_angle < 120) or (left_knee_angle > 30 and left_knee_angle < 120):
        if (right_hip_angle > 20 and right_hip_angle < 90) or (left_hip_angle > 20 and left_hip_angle < 90):
            if (right_hip_angle > 70 and right_hip_angle < 110) and (left_hip_angle > 160 or left_hip_angle < 20):
                if (left_knee_angle > 160 or left_knee_angle < 20):
                    if (right_shoulder_angle > 70 and right_shoulder_angle < 110):
                        label = "COUCHE SUR LE CÔTÉ"
    
    return label,output_image                
    
    
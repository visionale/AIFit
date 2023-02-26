import numpy as np
import cv2

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def plot_exercise_text(image, exercise):
    match exercise:
        case "Bicep curl":            
            cv2.putText(image, "Bicep curl with barbell side view", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

        case "Tricep rope":            
            cv2.putText(image, "Triceps with rope side view", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

        case "Pull up":            
            cv2.putText(image, "Pull ups back view", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

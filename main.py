import argparse
import cv2
import mediapipe as mp
import numpy as np
import imutils

from configs import *
from exercises_functions import *
from utils import calculate_angle, plot_exercise_text

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



def main(exercise=None):
    # VIDEO FEED
    video = cv2.VideoCapture(0)

    # Counter variables
    counter = 0 
    phase = None

    if save_video:
        #video_save = cv2.VideoWriter("Biceps.avi", cv2.VideoWriter_fourcc(*'XVID'), 15, (1280, 960))
        video_save = cv2.VideoWriter("Pull_up.mp4", cv2.VideoWriter_fourcc(*'MP4V'), 15, (1280, 960))

    ## Setup mediapipe instance
    with mp_pose.Pose(static_image_mode=False, enable_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while video.isOpened():
            ret, frame = video.read()
            frame = imutils.resize(frame, width=frame.shape[1] * 2)

            #print("shape:", frame.shape)
            fps = video.get(cv2.CAP_PROP_FPS)
            #print("fps:", fps)                    

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark            
                
                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                
                # Calculate angles            
                left_curl_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_curl_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)               

                
                # Visualize angle
                if draw_angles:
                    cv2.putText(image, str(np.round(left_curl_angle, 2)), tuple(np.multiply(left_elbow, [image.shape[1], image.shape[0]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(np.round(right_curl_angle, 2)), tuple(np.multiply(right_elbow, [image.shape[1], image.shape[0]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(np.round(left_shoulder_angle, 2)), tuple(np.multiply(left_shoulder, [image.shape[1], image.shape[0]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(image, str(np.round(right_shoulder_angle, 2)), tuple(np.multiply(right_shoulder, [image.shape[1], image.shape[0]]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                match exercise:
                    case "Bicep curl":
                        counter, phase = bicep_curl_barbell_side(left_shoulder_angle, left_curl_angle, phase, counter)
                        cv2.putText(image, "Bicep curl with barbell side view", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

                    case "Tricep":
                        counter, phase = tricep_rope_side(left_shoulder_angle, left_curl_angle, phase, counter)
                        cv2.putText(image, "Triceps", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

                    case "Pull up":
                        counter, phase = pull_up_back(left_shoulder_angle, right_shoulder_angle, phase, counter)
                        cv2.putText(image, "Pull ups back view", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)                
                
            except:
                pass

            #Render exercise name
            plot_exercise_text(image, exercise)           
            
            # Rep data
            if rep_data:
                cv2.putText(image, 'REPS', (15,55), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), 
                            (30,110), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            if stage_data:
                cv2.putText(image, 'FASE:', (125,55), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, phase, 
                            (200,55), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            # Render detections
            if render_detections:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))


            if save_video:
                video_save.write(image)  

            cv2.imshow('Main Screen', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                video_save.release()
                break
                
        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="AI Fitness", description="This program counts execution of exercises. But only the well done ones")
    parser.add_argument('-e', '--exercise', required=True, help="Enter the exercise you will be doing")

    args = parser.parse_args()

    main(exercise=args.exercise)
    
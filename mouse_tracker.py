import cv2
import mediapipe as mp
import pyautogui
cap = cv2.VideoCapture(0)                                   #open up Video camera 
hand_detector = mp.solutions.hands.Hands()                  #detect the hand
drawing_utils = mp.solutions.drawing_utils                  #hand tracking
screen_width, screen_height = pyautogui.size()              #set up the screen size
index_finger_y=0                                            #initialising index finger's y axis value 
while True:                                                 #to keep the camera access on 
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width,_ = frame.shape
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks         
    if hands:                                                #hand tracking using landmarks
        for hand in hands:
            drawing_utils.draw_landmarks(frame,hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x=int(landmark.x*frame_width)
                y=int(landmark.y*frame_height)
                print(x,y)
                #index
                if id==8:
                    cv2.circle(img=frame, center=(x,y), radius=20, color=(0,255,255))
                    index_finger_x = screen_width/frame_width*x
                    index_finger_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_finger_x,index_finger_y)
                #thumb
                if id==4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,100,100))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    print('outside',abs(index_finger_y - thumb_y))
                    if abs(index_finger_y-thumb_y)<50:
                        pyautogui.click()
                        pyautogui.sleep(1)
    cv2.imshow('Virtual Mouse',frame)
    cv2.waitKey(1)
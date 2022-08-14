import cv2
import numpy as np
from matplotlib import pyplot as plt
import mediapipe as mp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout



    
right_hand = True

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
holistic = mp_holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75)
mpHands=mp.solutions.hands
hands=mpHands.Hands(False,2,1,0.5,0.5)

def draw_landmarks(image,results):
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        
def extract_keypoints(results):
    if right_hand:
        if results.right_hand_landmarks:
            hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()
        else:
            hand = np.zeros(21*3)
    else:
        if results.left_hand_landmarks:
            hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()
        else:
            hand = np.zeros(21*3)
    return hand

actions = np.array(['write','idle','eraseall','erase'])

model = Sequential()
model.add(Dense(63, activation = 'relu', input_shape=(63,)))
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(32, activation = 'relu'))
model.add(Dense(4, activation = 'softmax'))

model.load_weights(r"D:\AiVirtualPainter\yomari-codecamp\classifier.h5")
res = np.zeros(10)

threshold = 0.7


    # def load_dependencies(self):

    #     mp_holistic = mp.solutions.holistic
    #     mp_drawing = mp.solutions.drawing_utils

    #     def draw_landmarks(image,results):
    #         mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    #         mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        
    #     def extract_keypoints(results):
    #         if right_hand:
    #             if results.right_hand_landmarks:
    #                 hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()
    #             else:
    #                 hand = np.zeros(21*3)
    #         else:
    #             if results.left_hand_landmarks:
    #                 hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()
    #             else:
    #                 hand = np.zeros(21*3)
    #         return hand

    #     self.actions = np.array(['write','erase','eraseall','idle'])

    #     model = Sequential()
    #     model.add(LSTM(64, return_sequences=True, activation = 'relu', input_shape=(10,63)))
    #     model.add(LSTM(128, return_sequences=True, activation = 'relu'))
    #     model.add(LSTM(64, return_sequences=False, activation = 'relu'))
    #     model.add(Dense(64, activation='relu'))
    #     model.add(Dense(32, activation='relu'))
    #     model.add(Dense(4, activation='softmax'))

    #     model.load_weights('final_classifier.h5')
    #     self.res = np.zeros(10)

    #     self.sequence = []
    #     self.threshold = 0.7

        
        
    
    # write this before calling class_return in calling module
    #with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    # or the following might work


def class_return(image,handNo=0):
    global res
    global coordinate
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    if right_hand:
        # Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    else:
        # Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        
    keypoints = extract_keypoints(results)
    res = model.predict(np.expand_dims(keypoints, axis=0))[0]
    print(actions[np.argmax(res)])
    coordinate = keypoints[23:25]

    ##########################For coordinate#####################

    lmList = []
    image = cv2.flip(image,1)

    if results.right_hand_landmarks:
        for id,lm in enumerate(results.right_hand_landmarks.landmark):
            # print(id,lm)
            h,w,c = image.shape
            # print(image.shape)
            cx,cy = int(lm.x*w), int(lm.y*h)
            # print(id,cx,cy)
            lmList.append([id,cx,cy])

    image = cv2.flip(image,1)




    ##############################################################

    if res[np.argmax(res)] > threshold:
        return actions[np.argmax(res)], image, lmList
    else:
        return "nothing", image, lmList

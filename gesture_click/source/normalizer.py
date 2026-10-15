# this is the main working file containing the source code for observing gestures and expression from the data produced.
# it contains the system responsible for the recogniton of different landmarks

#------------------------------------------------------------------------------------------------------------------------
# imports 
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision import HandLandmarkerResult
    from Gesture_landmark import Handtriangulator, DATA_DIR, MODEL_PATH

except ImportError as IR:
    print(IR)

try:
    import numpy as np
except ImportError as IR:
    print(IR)
try:
    import cv2 as cv
except ImportError as IR:
    print(IR)
# secondary
from pathlib import Path
from sqlite3 import DatabaseError
from typing import Optional
from os import path
import math

from cv2 import normalize 


#-----------------------------------------------------------------
class Normalizer():
    def __init__(self) -> None:# inialise the Ai
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'The system could not intiate the model :{e}')


    def translation_invariance(self,data_result:HandLandmarkerResult,anchor:int=0)->list:#the defualt reference anchor is wrist pos
        """This method normalizes the landmark coordinates ,making them relative to a anchor landmark"""
        try:

            if data_result is None:
                raise DatabaseError(
                    "The system could not fetch the landmarks data"
                )

            data_set = []

            for hand in data_result.hand_landmarks:

                reference = hand[anchor]

                normalized_hand = []

                for landmark in hand:

                    x = landmark.x - reference.x
                    y = landmark.y - reference.y
                    z = landmark.z - reference.z

                    normalized_hand.append([x, y, z])

                normalized_hand = np.array(
                    normalized_hand,
                    dtype=float
                )

                data_set.append(normalized_hand)

            return data_set

        except Exception as e:

            raise RuntimeError(
                f"System could not normalize the data: {e}"
            )
    def terminate(self)->None:
        pass

if __name__ == '__main__':
    
    Model = Normalizer()
    ANM = Handtriangulator(model_path=str(MODEL_PATH))
    ANM.analyise_landmarks(frame = str(DATA_DIR / "images" / "two_hands" / "test-image2.jpg"),timestamp=1)
    print(Model.translation_invariance(ANM.generation))

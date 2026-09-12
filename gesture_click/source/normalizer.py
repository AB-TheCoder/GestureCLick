# this is the main working file containing the source code for observing gestures and expression from the data produced.
# it contains the system responsible for the recogniton of different landmarks

#------------------------------------------------------------------------------------------------------------------------
# imports 
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision import HandLandmarkerResult


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
from typing import Optional
from os import path
import math 


#-----------------------------------------------------------------
class Normalizer():
    def __init__(self) -> None:# inialise the Ai
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'The system could not intiate the model :{e}')


    def translation_normalisation(self)->HandLandmarkerResult:
        """This method normalizes the landmark coordinates ,making them relative to a anchor landmark"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'system could not normalize the data::{e}')
    def scale_normalisation(self)-> HandLandmarkerResult:
        """this method normalises the size of the handgestures"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'system could not normalize the data::{e}')
    def terminate(self)->None:
        pass

if __name__ == '__main__':
    Model = Normalizer()

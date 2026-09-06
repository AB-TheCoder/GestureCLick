# this is the main working file containing the source code for observing gestures and expression from the data produced.
# it contains the system responsible for the recogniton of different landmarks

#------------------------------------------------------------------------------------------------------------------------
# imports 
try:
    import mediapipe as ann
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
from ast import Try
from nt import error
from pdb import run


#-----------------------------------------------------------------
class NeuralN():
    def __init__(self) -> None:# inialise the Ai
        pass

    @staticmethod
    def bgr_rgb(frame:np.ndarray) -> np.ndarray:
        """this static method converts the bgr format mat data to the required rgb format Numpy Array"""
        try:
            framePR=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            return framePR
        except Exception as e:
            raise RuntimeError(f'the bgr format could not be converted to RGB beacuse:{e}')
    def analyise_image(self)->list:
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the image could not be analyised because ::{e}')
    
    def terminate(self)->None:
        pass

if __name__ == '__main__':
    frame = cv.imread(r'gesture_click\data\temporary\2026-08-31_22-22-56-frame.png')
    print(NeuralN.bgr_rgb(frame))

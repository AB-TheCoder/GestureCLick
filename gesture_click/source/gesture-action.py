#this is the third component of the project 
#it will use the differnt landmarks to recognise gestures and then it execute the corresponding action 
#author:@AaravBhatt 

#-----------------------------------------------------------------------------------------------
#imports
#primary--------------------------

try:
    import cv2 as cv
except Exception as e:
    raise ImportError(f'cv2 could not be imported because{e}')
try:
    import numpy as np
except Exception as e:
    raise ImportError(f'Numpy could not be successfully imported becuase :{e}')
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision import HandLandmarkerResult
except Exception as e:
    raise ImportError(f'the following error occurred while importing the MediaPipe Hands:{e}')
try:
    import json
except Exception as e:
    raise ImportError(f'the following error occurred while importing the json package:{e}')
#-----------------------------------------------------------------------------------------------
#secondary--------------------------
try:
    import os 
    import sys 
    import math 
    from pathlib import Path
    from typing import Optional

except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the secondary modules:{e}')

#---------------------main-------------------------------------------------
class Model():
    def __init__(self):
        """this is the constructor class and it will initialise the kernel model and other necessary variables"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the following error occurred while initialising the kernel class:{e}')

    def terminate():
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the system could not terminate the program:{e}')


if __name__ =='__main':
    pass
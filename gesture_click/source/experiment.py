#this is the third component of the project 
#it will use the differnt landmarks to recognise gestures and then it execute the corresponding action 
#author:@AaravBhatt 

#-----------------------------------------------------------------------------------------------
#imports
#primary--------------------------
from mediapipe import tasks
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.audio import RunningMode
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
from mediapipe.tasks.python.vision.core import image


try:
    import cv2 as cv
except Exception as e:
    raise ImportError(f'cv2 could not be imported because{e}')
try:
    import numpy as np
except Exception as e:
    raise ImportError(f'Numpy could not be successfully imported becuase :{e}')
try:

    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the MediaPipe Hands:{e}')

#-----------------------------------------------------------------------------------------------
#secondary--------------------------
try:
    import os 
    import sys 
    import math 
    from pathlib import Path
    from typing import Optional
    from ast import Try # ??? 
    from nt import error    
except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the secondary modules:{e}')

#paths are built from this file's location so they work from any working directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

#---------------------main-------------------------------------------------
class ANN():
    Base_Options = tasks.BaseOptions
    Hand_Landmarker = tasks.vision.HandLandmarker
    Hand_LandmarkerOptions = tasks.vision.HandLandmarkerOptions
    Running_Mode = tasks.vision.RunningMode
    def __init__(self,model_path:str,max_hands:int=2,min_confidence:float=0.6,Running_mode = tasks.vision.RunningMode.VIDEO):
        """this is the constructor class and it will initialise the Ann model and other necessary variables""" 
        try:
            
            try:
                self.base_options = ANN.Base_Options(
                    model_asset_path = model_path,
                )
            except Exception as e:
                raise error(f'unable to create BaseOptions :{e}')
            try:
                self.Options = ANN.Hand_LandmarkerOptions(
                    num_hands = max_hands,
                    running_mode = Running_mode,
                    base_options = self.base_options,
                    min_tracking_confidence = min_confidence
                )
            except Exception as e:
                raise error(f'unable to create HandLandmarker Options:{e}')
            try:
                self.model = ANN.Hand_Landmarker.create_from_options(
                    self.Options
                )
            except Exception as e:
               raise error(f'unable to create handlandmarker model :{e}')

        except Exception as e:
            raise RuntimeError(f'the following error occurred while initialising the Gesture_recog class:{e}')
    def Image_wrapper(self,numpy)->image:
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'System could not wrap the image in Media_pipe Image object effectively:{e}')
    def analyise_landmarks(self) -> dict:
        """ this method will analyse the landmarks and return the gesture type
        it will return a dictionary with the gesture type and the confidence score"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the following error occurred while analysing the landmarks:{e}')
    
    def terminate(self) -> None:
        """ this method will terminate the program""" 
        pass


if __name__=="__main__":
    ANM =ANN(model_path=str(DATA_DIR / "hand_landmarker.task"))

    
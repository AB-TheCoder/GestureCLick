#this is the third component of the project 
#it will use the differnt landmarks to recognise gestures and then it execute the corresponding action 
#author:@AaravBhatt 

#-----------------------------------------------------------------------------------------------
#imports
#primary--------------------------
try:
    import cv2 as cv
    import numpy as np
    import mediapipe as Ann 


except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the modules:{e}')

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


#---------------------main-------------------------------------------------
class Gesture_recog():
    def __init__(self):
        """this is the constructor class and it will initialise the Ann model and other necessary variables""" 
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the following error occurred while initialising the Gesture_recog class:{e}')
    
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
    pass 
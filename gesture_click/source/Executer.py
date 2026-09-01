#this file will use the identified gestures and then match it with the required actions and execute it 
# this is the main executer of the actions intended by the user  
#author:@AaravBhatt 


 

#-----------------------------------------------------------------------------------------------
#imports
#primary--------------------------
try:
    import cv2 as cv
except Exception as e:
    raise ImportError(f'the following error occurred while importing the CV2 module:{e}')
try:
    import mediapipe as Ann
except Exception as e:
    raise ImportError(f'the following error occurred while importing the MediaPipe Hands module:{e}')

try:
    import numpy as np
except Exception as e:
    raise ImportError(f'the following error occurred while importing the Numpy module:{e}')

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
    raise ImportError(f'the following error occurred while importing the secondary modules:{e}') 


#---------------------main-------------------------------------------------
class Executer():
    def __init__(self):
        """this is the constructor method  and it will initialise the necessary variables and other library"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the following error occurred while initialising the Executer class:{e}')
    
    def execute_action(self,gesture:str) -> None:
        """ this method will execute the action based on the identified gesture"""
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'the following error occurred while executing the action:{e}') 


    def terminate(self) -> None:
        pass


if __name__=="__main__":
    pass 
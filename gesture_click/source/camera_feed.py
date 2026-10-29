# this is the main file for the camera feed which it the fondation of the entire culture
# this file will contain the source code for the basic data feed , the output will be used by another node which will recognise the gestures and expression
#aim: create a system to convert imagery input to numpy array in an organised and efficient way for Media-pipe Hand
#framerate-#required#

# Imports--------------------
# primary
try:
    import cv2 as cv
except ImportError as IR:
    print(IR)
try:
    import numpy as np
except ImportError as IR:
    print(IR)
# secondary
from nt import error
from pathlib import Path
from typing import Optional

from os import path
from datetime import datetime as dt

#paths are built from this file's location so they work from any working directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

#----------------------------------------------------------------
class Camera_Feed():
    def __init__(self,camera_index:int=0) ->None:
        """initializes the camera and sets basic variables ergo to be utilized"""
        try:
            self.cap = cv.VideoCapture(camera_index)    
            if not self.cap.isOpened():
                raise error('the Camera could no be opened')
        except Exception as e:
            raise RuntimeError(f'the initialization failed because:{e}')
    def Get_frame(self) -> np.ndarray:
        """ this method fetches the frame and returns the data in bgr(Format) numpy Array"""
        try:
            success,frame = self.cap.read()
            if not success:
                raise error('Cv was unable to fetch the frame')
            else:
                self.frame = frame
                return frame
        except Exception as e:
            raise RuntimeError(f"the frame could not be obtained because:{e}")
    def terminate(self) ->None:
        '''this method releases the camera ere utilized and terminates all windows ,thereby marking the end of the program'''
        try:
            self.cap.release()
            cv.destroyAllWindows()
            print('model Terminated')
            return None
        except Exception as e:
            raise RuntimeError(f'the system could not terminate CV because: {e}')
    def register(self,frame:np.ndarray,save_dir:str) ->str:
        '''this method updates the frame fetched in the from of a png image stored at the specific path denoted'''
        try:
            if path.isdir(save_dir) == False :
                raise FileNotFoundError('The system can locate the wished directory,recheck the path')
            else:
                timestamp= dt.now().strftime(r"%Y-%m-%d_%H-%M-%S")
                pathto =  Path(save_dir) / f"{timestamp}-frame.png"
                if not cv.imwrite(str(pathto),frame):
                    raise error('the library could not write the frame to the desired location')
               
                
        except Exception as e:
            raise RuntimeError(f'the data could not be updates because: {e}')



if __name__ == '__main__':
    model = Camera_Feed()
    # while True:
    #     cv.imshow('camera',model.Get_frame())
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         model.terminate()
    #         break
    model.Get_frame()
    save_dir = DATA_DIR / "temporary"
    save_dir.mkdir(exist_ok=True)
    model.register(model.frame,str(save_dir))
    model.terminate()
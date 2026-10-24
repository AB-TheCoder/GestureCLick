# this is the file with which will esatblish the webcam and integrete all the files i have completed till now.
# step 6 
# author -@Aarav Bhatt

# ----------------------------------------------------------------------------------------

# Imports 

# primary:







try:
    import cv2 as cv
except Exception as e:
    raise ImportError(f'cv2 could not be imported because{e}')
try:
    import numpy as np
except Exception as e:
    raise ImportError(f'Numpy could not be successfully imported becuase :{e}')

# Secondary 
try:
    import sys
    from pathlib import Path
    import time 
    from typing import Optional
except Exception as e:
    raise ImportError(f" Could not import Secondary Packages{e}")
SOURCE_DIR = Path(__file__).resolve().parent / "source"
sys.path.insert(0, str(SOURCE_DIR))
try:
    from camera_feed import Camera_Feed
    from Gesture_landmark import Handtriangulator,MODEL_PATH
    from normalizer import Normalizer # custom packages
except Exception as e:
    raise ImportError(f" Custom packages could not be installed:{e}")


#-------------------------------------------------------------------------------
# variables:
# MediaPipe hand landmark indices (row numbers in each (21, 3) array)
WRIST = 0

THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20


#-------------------------------------------------------------------------------
#THE LOOOOOPPPPPP:

class integretor():
    def __init__(self,Model_path:Optional[str]=MODEL_PATH )-> None:
        """ To initalise things and introduce basic variables(typicaly to do what a constructor does)"""

        try:
            self.tracker = Handtriangulator(model_path=str(Model_path))
            self.start=time.monotonic()
            self.camera = Camera_Feed()
            self.normalizer= Normalizer()
            self.frame_count=0
            
        except Exception as e:
            raise RuntimeError(f" could not Initialise the constructure due to:{e}")
    def FEED(self):
        try:
            

            while True:
                try:
                    frame = self.camera.Get_frame()
                    #drawing the landmarks
                    timestamp_ms=int((time.monotonic()-self.start)*1000)
                    result = self.tracker.analyise_landmarks(frame,timestamp_ms)
                    frame = self.tracker.visuals(frame,result)
                    # normalise

                    self.frame_count += 1
                    try:
                        translated = self.normalizer.translation_invariance(result)
                        scaled = self.normalizer.scale_invariance(translated)
                        rotated = self.normalizer.rotational_invariance(scaled)
                    except RuntimeError as e:
                        print("skipped frame:", e)
                        rotated = []

                    if self.frame_count % 15==0:
                        for hand in rotated:
                            print(np.round(hand[MIDDLE_MCP],3))

                    cv.imshow("GestureClick",frame)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
                except Exception as e:
                    raise RuntimeError(e)

        except Exception as e:
            raise RuntimeError(f"A error with the main loop ruined the fun;|.FIX IT: {e}")
        finally:
            self.camera.terminate()
            self.tracker.terminate()
if __name__ =="__main__":
    model = integretor()
    model.FEED()
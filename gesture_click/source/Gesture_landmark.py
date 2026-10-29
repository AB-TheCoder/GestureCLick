#this is the 2 component of the project 
#this file will use mediapipe to generate the coordinats of different landmarks which are to be used as input for other files
#author:@AaravBhatt 

#-----------------------------------------------------------------------------------------------
#imports
#primary------------------------------




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
    from mediapipe.tasks.python.vision import drawing_utils

except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the MediaPipe Hands:{e}')

#-----------------------------------------------------------------------------------------------
#secondary--------------------------
try:


    from pathlib import Path
    from typing import Optional
 
except Exception as e:
    raise RuntimeError(f'the following error occurred while importing the secondary modules:{e}')

#paths are built from this file's location so they work from any working directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_PATH = DATA_DIR / "hand_landmarker.task"


#---------------------main-------------------------------------------------
class Handtriangulator():
    Base_Options = mp.tasks.BaseOptions
    Hand_Landmarker = mp.tasks.vision.HandLandmarker
    Hand_LandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    Running_Mode = mp.tasks.vision.RunningMode
    def __init__(self,model_path:str,max_hands:int=2,min_confidence:float=0.6,Running_mode = mp.tasks.vision.RunningMode.VIDEO,img_path:Optional[str]=None):
        """this is the constructor class and it will initialise theHandtriangulator model and other necessary variables""" 
        try:
            
            try:
                self.base_options =Handtriangulator.Base_Options(
                    model_asset_path = model_path,
                )
            except Exception as e:
                raise SystemError(f'unable to create BaseOptions :{e}')
            try:
                self.Options =Handtriangulator.Hand_LandmarkerOptions(
                    num_hands = max_hands,
                    running_mode = Running_mode,
                    base_options = self.base_options,
                    min_tracking_confidence = min_confidence
                )
            except Exception as e:
                raise SystemError(f'unable to create HandLandmarker Options:{e}')
            try:
                self.model =Handtriangulator.Hand_Landmarker.create_from_options(
                    self.Options
                )
            except Exception as e:
               raise SystemError(f'unable to create handlandmarker model :{e}')

        except Exception as e:
            raise RuntimeError(f'the following error occurred while initialising the Gesture_recog class:{e}')


    def analyise_landmarks(self,frame:np.ndarray|str,timestamp:int) -> HandLandmarkerResult:
        """ this method will:-
        1.convert standered BGR format to rgb format for internal processing
        2. aquire a image object needed for again internal processing
        3. analyse the landmarks and return the generation
        it will return a handlandmarkerResult datatype with the landmarks and handness"""
        try:
            try:
                if type(frame)==np.ndarray:

                    frame_RGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
                else:
                    file_path = Path(frame)
                    if not file_path.exists():

                        raise FileNotFoundError('The system can locate the wished directory,recheck the path')
                    else:
                        self.img_path = file_path
                        frame_RGB = cv.cvtColor(cv.imread(frame),cv.COLOR_BGR2RGB)
                        
            except Exception as e:
                raise RuntimeError(f'the bgr format could not be converted to RGB beacuse:{e}')
            try:
                Image_frame = mp.Image(image_format=mp.ImageFormat.SRGB,data=frame_RGB)
                
            except Exception as e:
                raise RuntimeError(f'System could not wrap the image in Media_pipe Image object effectively:{e}')

            try:
                result = self.model.detect_for_video(
                    Image_frame,
                    timestamp
                )
              
            except Exception as e:
              raise RuntimeError(f'the following error occurred while analysing the landmarks:{e}')

            self.generation = result
            return self.generation
        except Exception as e:
            raise RuntimeError(f'the system could not anaylise for landmarks:{e}')
    def visuals(self,frame:np.ndarray|str|Path,generation:HandLandmarkerResult)->np.ndarray:
        """this method will be used to visuallize the landmark coordinates. #usefull when testing@temporary method"""
        try:
            if isinstance(frame, (str, Path)):
                loaded: np.ndarray | None = cv.imread(str(frame))
                if loaded is None:
                    raise ValueError(f'could not read image: {frame}')
                frame = loaded

            if generation.hand_landmarks:
                for hand_landmarks in generation.hand_landmarks:
                    drawing_utils.draw_landmarks(
                        frame,
                        hand_landmarks,
                        vision.HandLandmarksConnections.HAND_CONNECTIONS
                        )
                self.annotted  = frame
            return frame

        except Exception as e :
            raise RuntimeError(f'the system could not provide a visual view :{e}')
    def terminate(self) -> None:
        """ this method will terminate the program""" 
        try:
            self.model.close()  
            print('model Terminated')
            return None
        except Exception as e:
            raise RuntimeError(f'the system could not terminate API :{e}')


if __name__=="__main__":
    ANM = Handtriangulator(model_path=str(MODEL_PATH))
    ANM.analyise_landmarks(frame = str(DATA_DIR / "images" / "two_hands" / "test-image2.jpg"),timestamp=1)
    print(ANM.generation)



        
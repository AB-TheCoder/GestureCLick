# this is the main working file containing the source code Normalising
#  the landmark coordinate before recognition of gestures

#------------------------------------------------------------------------------------------------------------------------
# imports 

try:
    from mediapipe.tasks.python.vision import HandLandmarkerResult
    from Gesture_landmark import Handtriangulator, DATA_DIR, MODEL_PATH

except ImportError as IR:
    print(IR)

try:
    import numpy as np
except ImportError as IR:
    print(IR)


#-----------------------------------------------------------------
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


#-----------------------------------------------------------------
class Normalizer():
    def __init__(self) -> None:#
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'The system could not intiate the model :{e}')

    
    def translation_invariance(self,data_result:HandLandmarkerResult,anchor:int=WRIST,aspect:float=1.0)->list[np.ndarray]:#the defualt reference anchor is wrist pos
        """This method normalizes the landmark coordinates ,making them relative to a anchor landmark"""
        try:
            

            if not 0<= anchor <= PINKY_TIP:
                raise ValueError(f"anchor must be 0-20,got{anchor}")
            if data_result is None :
                raise ValueError(
                    "The system could not fetch the landmarks data"
                )


            data_set = []

            for hand in data_result.hand_landmarks:


                if len(hand) != 21:
                    raise ValueError(f"expected 21 landmarks, got {len(hand)}")
                reference = hand[anchor]

                normalized_hand = []

                for landmark in hand:

                    x = (landmark.x - reference.x)*aspect
                    y = landmark.y - reference.y # making the coordinate independent of the image
                    z = landmark.z - reference.z

                    normalized_hand.append([x, y, z])

                normalized_hand = np.array(
                    normalized_hand, # changing the way the data is going to be stored
                    dtype=float
                )
                if not np.all(np.isfinite(normalized_hand)):
                    raise ValueError("Hand Contains NaN or inf")
                data_set.append(normalized_hand)

 
            return data_set

        except Exception as e:

            raise RuntimeError(
                f"System could not normalize the data: {e}" 
            ) from e 
    def scale_invariance(self,data:list[np.ndarray]) -> list[np.ndarray]:
        """ In this Stage , i scale down the data to a uniform value so that all hand (bigger or smaller) give the same value"""
        try:
            
            if data is None :
                raise ValueError(
                    "The system could not fetch the landmarks data"
                )

            scaled_data = []
            for hand in data:
                if not np.all(np.isfinite(hand)):
                    raise ValueError("hand contains NaN or inf")

                S = np.linalg.norm(hand[MIDDLE_MCP] - hand[WRIST])
                if S < 1e-6:
                    raise ValueError("S is about zero::BAD Detection")
                new_hand = hand/S
                scaled_data.append(new_hand)
            

            return scaled_data
            
        except Exception as e:
            raise RuntimeError(
                f"System could not normalise the data: {e}"
            )from e 

    def rotational_invariance(self,data:list[np.ndarray]) ->  list[np.ndarray]:
        """ THis is the final stage of normalisation where i normalise the hand with respect to the degree to which it is tiled
        meaning that i am making it independent from tilt."""
        try:
                        
            if data is None :
                raise ValueError(
                    "The system could not fetch the landmarks data"
                )

            rotational_normalised_set=[]
            for hand in data:
                if not np.all(np.isfinite(hand)):
                    raise ValueError("hand contains NaN or inf")

                x9, y9 = hand[MIDDLE_MCP, 0] - hand[WRIST,0], hand[MIDDLE_MCP, 1] - hand[WRIST,1] # getting the refernce pos-middleMCP
                theta = np.arctan2(y9, x9) # retriving the angle by Tan inverse function 
                cos = np.cos(theta)
                sin= np.sin(theta) # doing the math,(dont ask how it works ;-)
                R = np.array([[cos,sin,0],
                [-sin,cos,0],
                [0,0,1]
                ])
                rotated_hand = hand@ R.T # Matrix Multiplication.rotates every coordinate with a angle
                rotational_normalised_set.append(rotated_hand)

            return rotational_normalised_set
        except Exception as e:
            raise RuntimeError(
                f"Rotational Invarience failed because of {e} " 
            )from e

    def terminate(self)->None:
        pass

if __name__ == '__main__':
    np.set_printoptions(suppress=True, precision=4) # to round up the output to 4 digits(normal outputs range on )
    Model = Normalizer()
    ANM = Handtriangulator(model_path=str(MODEL_PATH))
    ANM.analyise_landmarks(frame = str(DATA_DIR / "images" / "two_hands" / "test-image2.jpg"),timestamp=1)
    translated = Model.translation_invariance(ANM.generation)
    print("----------------------------------------------")
    print(Model.rotational_invariance(Model.scale_invariance(translated)))

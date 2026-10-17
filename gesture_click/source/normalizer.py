# this is the main working file containing the source code for observing gestures and expression from the data produced.
# it contains the system responsible for the recogniton of different landmarks

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
    def __init__(self) -> None:# inialise the Ai
        try:
            pass
        except Exception as e:
            raise RuntimeError(f'The system could not intiate the model :{e}')


    def translation_invariance(self,data_result:HandLandmarkerResult,anchor:int=0)->list[np.ndarray]:#the defualt reference anchor is wrist pos
        """This method normalizes the landmark coordinates ,making them relative to a anchor landmark"""
        try:

            if data_result is None:
                raise ValueError(
                    "The system could not fetch the landmarks data"
                )

            data_set = []

            for hand in data_result.hand_landmarks:

                reference = hand[anchor]

                normalized_hand = []

                for landmark in hand:

                    x = landmark.x - reference.x
                    y = landmark.y - reference.y
                    z = landmark.z - reference.z

                    normalized_hand.append([x, y, z])

                normalized_hand = np.array(
                    normalized_hand,
                    dtype=float
                )

                data_set.append(normalized_hand)

 
            return data_set

        except Exception as e:

            raise RuntimeError(
                f"System could not normalize the data: {e}" 
            ) from e 
    def scale_invariance(self,data:list[np.ndarray]) -> list:
        try:
            if data is None:
                raise ValueError(
                    "The system could not fetch the landmarks data"
                )
            else:
                scaled_data = []
                for hand in data:
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
    def terminate(self)->None:
        pass

if __name__ == '__main__':
    
    Model = Normalizer()
    ANM = Handtriangulator(model_path=str(MODEL_PATH))
    ANM.analyise_landmarks(frame = str(DATA_DIR / "images" / "two_hands" / "test-image2.jpg"),timestamp=1)
    translated = Model.translation_invariance(ANM.generation)
    print("----------------------------------------------")
    print(Model.scale_invariance(translated))

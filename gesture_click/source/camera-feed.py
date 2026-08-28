# this is the main file for the camera feed which it the fondation of the entire culture

# Imports--------------------
# primary
try:
    import cv2 as CV
except ImportError as IR:
    print(IR)

# secondary
from pathlib import Path
from typing import Optional


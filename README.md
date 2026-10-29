# GestureCLick

* the App with which taking photos have never been more easier . This App enables  you to capture your gestures into commands for clicking photos and taking videos.

## What sets it apart
* This idea in its entire isnt that novel . There are many app hithro which have already undertaken this trail
* what sets is appart is that it :-
    1. works on any laptop/webcam (not phone-only)
    2. it allows user-personalised gestures that the ai learns to recognise(not possible in anyother software)
    3. it can be used over an great range and is incredibily accurate

## Mission Statement:
* THe final app should look like a aesthetic camera application which allows user to set their own gestures as commands to take photos and videos.
* It should be accurate and working even from a distance
### this is not final but will be built upon with experince.

## Workings

*  it can be devided into 2 main systems running together.
1. The camera frame loop-
    * i will use opencv to create a camera loop which will be constanly capturing the frames
2. The CV Ai:
    * a specially trained ai will review each frame looking for the command gesture which when recieved will initialise the effects.
3. Normalisation:
    * The ai recognises hands and produces numerical data for the position of each featues.This step will remove the noise,unneccesory data,and make the data independent of the image ,thus making it suitable of recognising the gesture

4. Feature Extraction:
    * In this step, the Features are extracted from the data. This features then help to classify a the input into different gestures.
5. Gesture recognition:
    * This Step aims to recognise gestures and produce the end result
6. Execution:
    * this step aims to execute a particular command tied to the respective gesture.



### this is not final but will be built upon with experince.

## How to install and run

**You need:** Python 3.11, a webcam, and Git.

1. Clone the repo:
   git clone https://github.com/AB-TheCoder/GestureCLick.git
   cd GestureCLick

2. Make a virtual environment and turn it on:
   python -m venv .venv
   .venv\Scripts\activate        (Windows)
   source .venv/bin/activate     (Mac/Linux)

3. Install the libraries (OpenCV, MediaPipe, NumPy):
   pip install -r requirements.txt

4. Run it:
   python gesture_click/source/main.py

A window opens showing your webcam with the hand landmarks drawn on and the FPS in the corner. Hold up one or both hands to see them tracked. Press **q** to quit.

The MediaPipe hand model (`hand_landmarker.task`) is already in `gesture_click/data`, so you don't need to download anything else.


## Details for first update:
1. i have created almost half of the project.
2. the program is now able to recognise hands ,give landmarks , normalise them .
3. next step is to figure out a way to extract feature from the numbers and assign gestures to specific features.

## Disclosure
1. AI has played an important yet passive and a teaching role in my project. Claude Code has been my choice.
2. Ai guides me on different steps ,debugs code and tells me places where i can make it more efficient and a better version of itself.
3. i have tried to ensure that the final say remains on my hand and it is i who writes the code and whos thinking has been implemented.
4. I Have provided many of The ai generated lessons and documents in the lessons folder.

# GestureCLick

* the place where photos have never been more easier . this extension plans to capture your gestures into commands for clicking photos and taking videos even from a range.

## What sets it apart
* this idea in its entire isnt that novel . there are many app hithro which have already undertaken this trail
* what sets is appart is that it :-
    1. works on any laptop/webcam (not phone-only)
    2. it allows user-personalised gestures that the ai learns to recognise(not possible in anyother software)
    3. it can be used over an great range and is incredibily accurate

## Mission Statement:
* i will be submitting this software for stardance high with hopes for winning a price.

* at first i will built a basic one for website than build upon it.

* i am aiming to atleast work 30 mins a day for this project with minimal use of ai.

* i am planning on finishing this before 31 september

## Workings

*  it can be devided into 2 main systems running together.
1. The camera frame loop-
    * i will use opencv to create a camera loop which will be constanly capturing the frames
2. The CV Ai:
    * a specially trained ai will review each frame looking for the command gesture which when recieved will initialise the effects.



### this is not final but will be built upon with experince.

## flow:


1. camera flows- using open cv ;for now, i will create a camera frame loop which will form the basis for the functioning of the enitre app.
2. gesture-recog- integreting MediaPipe hand , i will use the ai to look for different landmarks
3. gesture-identification - then i will form the basis of identifications and the basic defaults
4. customise-config- i will then add the novel function of customisable gesture and actions relating with different commands
5. Ui- build a ui for the interface
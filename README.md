# telloDrone

## Introduction

This repository contains API calls to control a tello drone and a special functionally that uses kmeans clustering the have the droe automatically follow a color put in front of the drone.

## API Reference

This repository contains a drone class.

Inside the class there are three main functions and some other smaller ones.

## Drone.control()

This function allows for joystick control from keyboard input. Below is the key
mapping to a drone action.

space :takeoff  
'l'   :land  
'q'   :emergency kill  
left  :left  
right :right  
up'   :forward  
down  :backward  
'w'   :up  
's'   :down  
'a'   :rotate left  
'd'   :rotate right  
'z'   :flip left  
'x'   :flip forward  
'c'   :flip right  
'v'   :flip backward

```python
from drone import Drone
drone = Drone()
drone.control()
```

## Drone.stream()
Before calling this function make sure to call Drone.connect_video(), this
will make sure that video starts updating the varible Drone.frame.
This added function limits the lag in video if Drone.stream begins to slow
down.

Drone.stream() will then diplay the video feed.

```python
from drone import Drone
drone = Drone()
drone.connect_video()
drone.stream()
```

## Drone.follow_color()
Again make sure to call Drone.connect_video() to start uploading video data
for Drone.follow_color() to start analyzing.

Put an object in front of the drone camera so that it can calibrate the color
you want it to follow.  This should take 5 seconds for the video feed to start
and calibrate the color.

The drone will then rotate to look at the object with the calibrated color.

```python
from drone import Drone
drone = Drone()
drone.video_connect()
drone.follow_color()
```

# AIFit
This application is an exercise counter using pose estimation technique with MediaPipe. However, the counter only works if the movement is done correctly.
Currently it works only with three exercises:

1. Bicep curl side view

2. Triceps rope push-down side view

3. Pull-up back view

![output](https://user-images.githubusercontent.com/124637937/221441302-8d9a34e7-9e6e-4c2b-90f0-c36feb91d071.gif)

We will be adding more exercises and different view angles, along with an automatic detection of which exercise is being done.

# Installation
Clone the repo: git clone https://github.com/visionale/AIFit.git

Create virtual environment:  python<version> -m venv <virtual-environment-name>


Install packages: pip install -r requirements.txt

# Usage
You need to pass a required argument, that is the exercise that you woll be doing.
Inside your env, use the command:

pyhton main.py --exercise "Name of exercise"

Currently possible arguments:

. "Bicep curl"

. "Tricep"

. "Pull up"

### Example:
- python main.py --exercise "Bicep curl"


# Project Reference
https://google.github.io/mediapipe/solutions/pose.html


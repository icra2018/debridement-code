# davinci-skeleton
The base directory structure for da Vinci utilities. This repository defines the basic structure and utilities
for the Da Vinci surgical robot in the AUTOLAB at UC Berkeley.

## Starting up the robot
Move the robot arms so they have at least a 1cm box of clearance around the tool tip, make sure that the tool tip is out of the cannula. Open a terminal and run
```
roscore
```
Create a new tab and run
```
./teleop
```
A teleop interface should load. In the telop interface, click the radio button for **Home**. You will hear a nasty fan sound from the PSM1 controller, don't worry about this (Sanjay is being negligent right now). Wait until the messages stop and then run **Teleop**. The robot is now engaged. Do not move the arms unless the clutch is engaged.

## Setting up your development environment
If this your first time on davinci0, create a directory for yourself in the home directory. Open a terminal and type
```
mkdir awesome_autolab_grad
cd awesome_autolab_grad
```

Then, create a virtual environment inside this directory
```
virtualenv my-new-project
```
This creates a new sub directory that will contain your project. Then, run following command:
```
cd my-new-project && source bin/activate
```
You know you are successful when your terminal prompt changes to something like *(my-new-project)davinci0@davinci0*.

Inside the project directory clone the *bare* skeleton repository:
```
git clone --bare https://github.com/BerkeleyAutomation/davinci-skeleton.git
```

Go to your own github and create a new repository, don't initialize it with anything. For example
*https://github.com/sjyk/my-new-project.git*. Then, run the following commands:
```
cd davinci-skeleton.git
git push --mirror https://github.com/sjyk/my-new-project.git
```
Then, delete the skeleton repository:
```
cd ..
rm -rf davinci-skeleton.git/
```
You can now clone your own repository:
```
git clone https://github.com/sjyk/my-new-project.git
cd my-new-project
```
Commit and push whatever you want to this personal repository.


## Robot API
There are basically three modules that are important (for now) *dvrk.robot*, *config.constants*, and *autolab.data_collector*:
```
from config.constants import *
from dvrk.robot import *
from autolab.data_collector import *
```

First, create a robot object:
```
psm1 = robot("PSM1")
```

To move the robot to a home position:
```
psm1.home()
```

To move the robot's tooltip to a new position:
```
import tfx

#A new position
post,rott = ((0.05, 0.02, -0.15), (0.0, 0.0,-160.0))

#creating the proper data structures
pos = [post[0], post[1], post[2]]
rot = tfx.tb_angles(rott[0], rott[1], rott[2])

#execute move with a SLERP motion planner
psm1.move_cartesian_frame_linear_interpolation(tfx.pose(pos, rot), 0.03)
```

Talk to Sanjay before using more advanced features of the API (all of which are in dvrk.robot).












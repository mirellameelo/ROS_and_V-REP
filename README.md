# Publishing images

```bash
cd $HOME
git clone https://github.com/mirellameelo/ROS_and_V-REP.git
```

## V-Rep and ROS 1


* Terminal 1:
```bash
source /opt/ros/<DISTRO>/setup.bash
roscore
```
* Terminal 2:

```bash
source /opt/ros/<DISTRO>/setup.bash
cd path/to/v-rep
./coppeliaSim.sh
```

### Monocular camera
1) Open ~/ROS_and_V-REP/scenes/rosInterfaceTopicPublisherAndSubscriber.ttt

2) Play the scene. The image from V-Rep is now being published in the /image topic.

### Stereo camera
1) Open ~/ROS_and_V-REP/scenes/rosInterfaceTopicPublisherAndSubscriber.ttt

2) Play the scene. Both images from V-Rep are now being published in the /left/image_raw and right/image_raw topics.

## V-Rep and ROS 2

```bash
source /opt/ros/<DISTRO>/setup.bash
cd path/to/v-rep
./coppeliaSim.sh
```

1) Open ~/ROS_and_V-REP/scenes/maze.ttt

2) Play the scene. The image from V-Rep is now being published in the /image topic.


## V-Rep and external ROS 2

1) Open ~/ROS_and_V-REP/scenes/maze_external_ros.ttt
2) Play the scene

```bash
# ROS 2
source /opt/ros/<DISTRO>/setup.bash
cd $HOME/ROS_and_V-REP
colcon build --symlink-install
source install/setup.bash

# running the ROS 2 package
ros2 run publisher publishing
```

3) Both images from V-Rep are now being published in the /left/image_raw and right/image_raw topics.

#### From scratch: 
* `ros2 pkg create --build-type ament_python <package_name>`
* Inside package.xml, add dependencies from ROS 
```hl
<export>
<exec_depend>std_msgs</exec_depend>
<exec_depend>sensor_msgs</exec_depend>
</export>
```
* Inside setup.py, add the executable
```hl
entry_points={
        'console_scripts': [
                '<executable_name> = <package_name>.<python_file_name>:main',
        ],
},
```

* Inside <python_file>, copy `sim.py`, `simConst.py`, `remoteApi.so`  
* Remove `from simConst import *` from `sim.py`
* Develop <python_file>
* `colcon build --symlink-install`

# Generating EuRoC dataset using V-Rep

* Terminal 1:

```bash
cd path/to/v-rep
./coppeliaSim.sh
```

1) Open /ROS_and_V-REP/scenes/generate_dataset_maze.ttt
2) Play the scene

* Terminal 2:

```bash
cd /ROS_and_V-REP
# USAGE: python3 src/generate_dataset.py <path>
python3 src/generate_dataset.py .
```

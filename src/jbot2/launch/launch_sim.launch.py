import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from glob import glob
from setuptools import setup 
from launch_ros.actions import Node

#path to current dir
cur_directory_path = os.path.abspath(os.path.dirname(__file__))

def generate_launch_description():
    package_name = 'jbot2'  # <--- CHANGE ME

    name=package_name
    version='0.0.0'
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # Path to the launch file      
        (os.path.join('share', package_name,'launch'), glob('launch/*.launch.py')),
      
        # Path to the mobile robot urdf file
        (os.path.join('share', package_name,'description/'), glob('./robot_core.xacro/*')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # bashCommand = "gazebo libgazebo_gazebo_factory.so"

    # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #            PythonLaunchDescriptionSource([os.path.join(
    #                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')])
    #             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'jbot2'],
                        output='screen')

    # Launch them all!
    return LaunchDescription([
        rsp,
        ExecuteProcess(cmd=['gazebo', '--verbose', '-s',
                       'libgazebo_ros_factory.so'], output='screen'),
        spawn_entity,



    ])

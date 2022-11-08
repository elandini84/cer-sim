import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():


    package_path = Path(get_package_share_directory("cer_rviz2"))
    urdf = os.path.abspath(str(package_path / "urdf/cer.urdf"))

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    rviz_config = LaunchConfiguration('rviz_config', default='false')

    ld = LaunchDescription()

    ld.add_action(DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'))
    ld.add_action(
        DeclareLaunchArgument(
            "rviz_config",
            default_value=str(package_path / "rviz2/cer.rviz"),
        )
    )

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    # RobotStatePublisher node
    ld.add_action(
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf])
    )

    # Rviz2 node
    ld.add_action(
        Node(
            package="rviz2",
            executable="rviz2",
            output="log",
            respawn=False,
            arguments=["-d", LaunchConfiguration("rviz_config")]
        )
    )

    return ld

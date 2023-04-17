from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from launch.launch_description_sources import PythonLaunchDescriptionSource

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    """Launch file for robot state publisher (rsp)"""

    moveit_config = MoveItConfigsBuilder("SIM_CER_ROBOT", package_name="cer_moveit2_wizard").to_moveit_configs()
    ld = LaunchDescription()

    return ld

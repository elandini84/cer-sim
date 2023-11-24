#from moveit_configs_utils.launches import generate_demo_launch #TODO: si può rimuovere?
from moveit_configs_utils import MoveItConfigsBuilder
from launch.actions import DeclareLaunchArgument

#Per generate_demo_launch expansion
#from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from moveit_configs_utils.launch_utils import DeclareBooleanLaunchArg
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


from moveit_configs_utils.launches import generate_static_virtual_joint_tfs_launch
from moveit_configs_utils.launches import generate_rsp_launch
from moveit_configs_utils.launches import generate_move_group_launch
from moveit_configs_utils.launches import generate_moveit_rviz_launch
from moveit_configs_utils.launches import generate_warehouse_db_launch
from moveit_configs_utils.launches import generate_spawn_controllers_launch

from launch import LaunchContext



def generate_launch_description():
    ld = LaunchDescription()
    context=LaunchContext()
   #--------------------------------------- Creazione istanza di MoveItConfigsBuilder con argomenti ----------------------------------------
    #rob_name = DeclareLaunchArgument("nm",default_value="SIM_CER_ROBOT",description="By default, we pass SIM_CER_ROBOT",)
    #pkg_name = DeclareLaunchArgument("pkg",default_value="cer_moveit2_left_no_hand",description="By default, the package is cer_moveit2_left_no_hand",)
    ld.add_action(DeclareLaunchArgument("nm",default_value="SIM_CER_ROBOT",description="By default, we pass SIM_CER_ROBOT",))
    ld.add_action(DeclareLaunchArgument("pkg",default_value="cer_moveit2_left_no_hand",description="By default, the package is cer_moveit2_left_no_hand",))

    launch_args = context.launch_configurations
    robot_name = launch_args.get('nm', 'SIM_CER_ROBOT')
    package_name = launch_args.get('pkg', 'cer_moveit2_left_no_hand')
    moveit_config = MoveItConfigsBuilder(robot_name=robot_name, package_name=package_name).to_moveit_configs()

    #---------------------------------------- Espansione di "generate_demo_launch(moveit_config)" ------------------------------------------
    #ld = LaunchDescription()

    #Argomenti con valori di default
    ld.add_action(DeclareBooleanLaunchArg("rsp",default_value=False))
    ld.add_action(DeclareBooleanLaunchArg("use_rviz", default_value=False))
    ld.add_action(DeclareBooleanLaunchArg("db",default_value=False,description="By default, we do not start a database (it can be large)",))
    ld.add_action(DeclareBooleanLaunchArg("debug",default_value=False,description="By default, we are not in debug mode",))
    ld.add_action(DeclareBooleanLaunchArg("spawn_contr",default_value=True))

    #--------------------------------------------------------- Virtual Joints --------------------------------------------------------------
    ld.add_action(generate_static_virtual_joint_tfs_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------ Robot State Publisher ----------------------------------------------------------
    #Aggiunta azione per includere rsp se richiesto tramite args
    if IfCondition(LaunchConfiguration("rsp")):
        ld.add_action(generate_rsp_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------- Move group launch -------------------------------------------------------------
        ld.add_action(generate_move_group_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------ Moveit rviz launch -------------------------------------------------------------
    #Aggiunta azione per lanciare rviz se richiesto tramite args
        ld.add_action(generate_moveit_rviz_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------- Data Base launch --------------------------------------------------------------
    #Aggiunta azione per lanciare database se richiesto tramite args
    #if IfCondition(LaunchConfiguration("db")):
        #ld.add_action(generate_warehouse_db_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------ Fake joint driver --------------------------------------------------------------
    #Aggiunge nodo "ros2_control_node" del pacchetto "controller_manager"
    ld.add_action(
        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[
                moveit_config.robot_description,
                str(moveit_config.package_path / "config/ros2_controllers.yaml"),
            ],
        )
    )
    #---------------------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------ Spawn Controllers --------------------------------------------------------------
    if IfCondition(LaunchConfiguration("spawn_contr")):
        ld.add_action(generate_spawn_controllers_launch(moveit_config))
    #---------------------------------------------------------------------------------------------------------------------------------------

    return ld

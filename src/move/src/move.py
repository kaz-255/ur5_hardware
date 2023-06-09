#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, SRI International
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of SRI International nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Acorn Pooley, Mike Lautman

## BEGIN_SUB_TUTORIAL imports
##
## To use the Python MoveIt! interfaces, we will import the `moveit_commander`_ namespace.
## This namespace provides us with a `MoveGroupCommander`_ class, a `PlanningSceneInterface`_ class,
## and a `RobotCommander`_ class. (More on these below)
##
## We also import `rospy`_ and some messages that we will use:
##
import typing
import time
import math
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
## END_SUB_TUTORIAL

def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True

class MoveGroupPythonIntefaceTutorial(object):
  """MoveGroupPythonIntefaceTutorial"""
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()

    ## BEGIN_SUB_TUTORIAL setup
    ##
    ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial',
                    anonymous=True)

    ## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
    ## the robot:
    robot = moveit_commander.RobotCommander()

    ## Instantiate a `PlanningSceneInterface`_ object.  This object is an interface
    ## to the world surrounding the robot:
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to one group of joints.  In this case the group is the joints in the Panda
    ## arm so we set ``group_name = panda_arm``. If you are using a different robot,
    ## you should change this value to the name of your robot arm planning group.
    ## This interface can be used to plan and execute motions on the Panda:
    group_name = "manipulator"
    group = moveit_commander.MoveGroupCommander(group_name)

    ## We create a `DisplayTrajectory`_ publisher which is used later to publish
    ## trajectories for RViz to visualize:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    ## END_SUB_TUTORIAL

    ## BEGIN_SUB_TUTORIAL basic_info
    ##
    ## Getting Basic Information
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^
    # We can get the name of the reference frame for this robot:
    planning_frame = group.get_planning_frame()
    print "============ Reference frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = group.get_end_effector_link()
    print "============ End effector: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Robot Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    ## END_SUB_TUTORIAL

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names

  def go_to_joint_state(self,a,b,c,d,e,f):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL plan_to_joint_state
    ##
    ## Planning to a Joint Goal
    ## ^^^^^^^^^^^^^^^^^^^^^^^^
    ## The Panda's zero configuration is at a `singularity <https://www.quora.com/Robotics-What-is-meant-by-kinematic-singularity>`_ so the first
    ## thing we want to do is move it to a slightly better configuration.
    # We can get the joint values from the group and adjust some of the values:
    joint_goal = group.get_current_joint_values()
    #joint_goal[0] = 1.385
    #joint_goal[1] = -0.295
    #joint_goal[2] = 1.925
    #joint_goal[3] = -1.239
    #joint_goal[4] = -1.59
    #joint_goal[5] = 0.653
    #joint_goal[6] = 0.0110

    joint_goal[0] = a*3.14/180
    joint_goal[1] = b*3.14/180
    joint_goal[2] = c*3.14/180
    joint_goal[3] = d*3.14/180
    joint_goal[4] = e*3.14/180
    joint_goal[5] = f*3.14/180

    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    group.stop()

    ## END_SUB_TUTORIAL

    # For testing:
    # Note that since this section of code will not be included in the tutorials
    # we use the class variable rather than the copied state variable
    current_joints = self.group.get_current_joint_values()
    return all_close(joint_goal, current_joints, 0.01)
  def go_to_pose_goal(self,x,y,z):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL plan_to_pose
    ##
    ## Planning to a Pose Goal
    ## ^^^^^^^^^^^^^^^^^^^^^^^
    ## We can plan a motion for this group to a desired pose for the
    ## end-effector:
    #line = raw_input("Please input goal position(x,y,z):")
    #goal_x, goal_y, goal_z = (float(x) for x in line.split(' '))
    goal_x, goal_y, goal_z = x,y,z

    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = -1.0
    pose_goal.position.x = goal_x
    pose_goal.position.y = goal_y
    pose_goal.position.z = goal_z
    group.set_pose_target(pose_goal)

    ## Now, we call the planner to compute the plan and execute it.
    plan = group.go(wait=True)
    # Calling `stop()` ensures that there is no residual movement
    group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    group.clear_pose_targets()

    ## END_SUB_TUTORIAL

    # For testing:
    # Note that since this section of code will not be included in the tutorials
    # we use the class variable rather than the copied state variable
    current_pose = self.group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.01)



  def go_to_pose_goal(self,x,y,z):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL plan_to_pose
    ##
    ## Planning to a Pose Goal
    ## ^^^^^^^^^^^^^^^^^^^^^^^
    ## We can plan a motion for this group to a desired pose for the
    ## end-effector:
    #line = raw_input("Please input goal position(x,y,z):")
    #goal_x, goal_y, goal_z = (float(x) for x in line.split(' '))
    goal_x, goal_y, goal_z = x,y,z

    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = -1.0
    pose_goal.position.x = goal_x
    pose_goal.position.y = goal_y
    pose_goal.position.z = goal_z
    group.set_pose_target(pose_goal)

    ## Now, we call the planner to compute the plan and execute it.
    plan = group.go(wait=True)
    # Calling `stop()` ensures that there is no residual movement
    group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    group.clear_pose_targets()

    ## END_SUB_TUTORIAL

    # For testing:
    # Note that since this section of code will not be included in the tutorials
    # we use the class variable rather than the copied state variable
    current_pose = self.group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.01)
  
  def plan_cartesian_path_mod(self, scale=1, x=0, y=0, z=0):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL plan_cartesian_path
    ##
    ## Cartesian Paths
    ## ^^^^^^^^^^^^^^^
    ## You can plan a Cartesian path directly by specifying a list of waypoints
    ## for the end-effector to go through:
    ##
    waypoints = []

    wpose = group.get_current_pose().pose
    wpose.position.z += z* 0.1  # First move up (z)
    wpose.position.x += x* 0.1  # Second move forward/backwards in (x)
    wpose.position.y += y* 0.1  # Third move sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction

    ## END_SUB_TUTORIAL

  def plan_cartesian_path(self, scale=1):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL plan_cartesian_path
    ##
    ## Cartesian Paths
    ## ^^^^^^^^^^^^^^^
    ## You can plan a Cartesian path directly by specifying a list of waypoints
    ## for the end-effector to go through:
    ##
    waypoints = []

    wpose = group.get_current_pose().pose
    wpose.position.z += scale * 0.1  # First move up (z)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -= scale * 0.1  # Third move sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    return plan, fraction

    ## END_SUB_TUTORIAL

  def display_trajectory(self, plan):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    robot = self.robot
    display_trajectory_publisher = self.display_trajectory_publisher

    ## BEGIN_SUB_TUTORIAL display_trajectory
    ##
    ## Displaying a Trajectory
    ## ^^^^^^^^^^^^^^^^^^^^^^^
    ## You can ask RViz to visualize a plan (aka trajectory) for you. But the
    ## group.plan() method does this automatically so this is not that useful
    ## here (it just displays the same trajectory again):
    ##
    ## A `DisplayTrajectory`_ msg has two primary fields, trajectory_start and trajectory.
    ## We populate the trajectory_start with our current robot state to copy over
    ## any AttachedCollisionObjects and add our plan to the trajectory.
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory)

    ## END_SUB_TUTORIAL

  def execute_plan(self, plan):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    group = self.group

    ## BEGIN_SUB_TUTORIAL execute_plan
    ##
    ## Executing a Plan
    ## ^^^^^^^^^^^^^^^^
    ## Use execute if you would like the robot to follow
    ## the plan that has already been computed:
    group.execute(plan, wait=True)

    ## **Note:** The robot's current joint state must be within some tolerance of the
    ## first waypoint in the `RobotTrajectory`_ or ``execute()`` will fail
    ## END_SUB_TUTORIAL

  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    box_name = self.box_name
    scene = self.scene

    ## BEGIN_SUB_TUTORIAL wait_for_scene_update
    ##
    ## Ensuring Collision Updates Are Receieved
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ## If the Python node dies before publishing a collision object update message, the message
    ## could get lost and the box will not appear. To ensure that the updates are
    ## made, we wait until we see the changes reflected in the
    ## ``get_known_object_names()`` and ``get_known_object_names()`` lists.
    ## For the purpose of this tutorial, we call this function after adding,
    ## removing, attaching or detaching an object in the planning scene. We then wait
    ## until the updates have been made or ``timeout`` seconds have passed
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      # Test if the box is in attached objects
      attached_objects = scene.get_attached_objects([box_name])
      is_attached = len(attached_objects.keys()) > 0

      # Test if the box is in the scene.
      # Note that attaching the box will remove it from known_objects
      is_known = box_name in scene.get_known_object_names()

      # Test if we are in the expected state
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True

      # Sleep so that we give other threads time on the processor
      rospy.sleep(0.1)
      seconds = rospy.get_time()

    # If we exited the while loop without returning then we timed out
    return False
    ## END_SUB_TUTORIAL
tutorial = MoveGroupPythonIntefaceTutorial()

def coordlist_to_movement(coord):
    x_0, y_0, z_0 = 0, 0, 0
    for id, item in enumerate(coord):
      x_goal, y_goal, z_goal = item[0],item[1], item[2]
      x_delta, y_delta, z_delta = x_goal-x_0, y_goal-y_0, z_goal-z_0
      print('ID:', id)     
      print('next movement:',  x_delta, y_delta, z_delta)    
      master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= x_delta, y= y_delta, z =z_delta)
      tutorial.execute_plan(master_plan)
      x_0, y_0, z_0 = x_goal, y_goal, z_goal
    return None

def main():
  try:
    print "============ Press `Enter` to begin the tutorial by setting up the moveit_commander (press ctrl-d to exit) ..."
    tutorial = MoveGroupPythonIntefaceTutorial()

    #forward control
    # input range: (-180,180)
    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # time.sleep(1)
    # # raw_input()
    # tutorial.go_to_joint_state(30,-30,30,0,0,0)

    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # raw_input()
    # tutorial.go_to_joint_state(-90,0,0,0,0,0)

    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # raw_input()
    # tutorial.go_to_joint_state(-90,-60,0,0,0,0)

    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # raw_input()
    # tutorial.go_to_joint_state(-90,-60, 20,0,0,0)

    # print "============ Press `Enter` to execute a movement using a joint state goal ..."
    # raw_input()
    #inverse  control
    #end-effector origin (0,0,0.98)
    # print "============ Press `Enter` to execute a movement using a pose goal ..."
    # time.sleep(1)
    # # raw_input()
    # tutorial.go_to_pose_goal(0.7,0.7,0.5)

    print "============ Press `Enter` to execute a movement using a pose goal ..."
    # raw_input()
    # raw_input()
    # tutorial.go_to_pose_goal(0.0, 0.5 ,0.5)
    print("Position 1")
    tutorial.go_to_joint_state(270, -60,120,-57,90,0)
    

    print "============ Press `Enter` to Go to start position of the Motion path."
    # raw_input()
    raw_input()
    tutorial.go_to_pose_goal(-0.3,-0.5,0.6)
    # p = 1
    # z = 0.5
    distance_cm = 15
    resolution_per_cm = 0.01
    # for l in range(1):
    #   for i in range(int(distance_cm*100*resolution_per_cm)):
    #     z = z+p*resolution_per_cm
    #     tutorial.go_to_pose_goal(0.1,-0.5, z)
    #     print(z)
    #   print("Step" ,l , "completed!")
    #   p = p*-1
    print('motion successful')
    time.sleep(1)
    print("Start Position")
    

    print "============ Press `Enter` to execute a movement using a cartesian ..."
    # raw_input()
    raw_input()
    # master_plan, fraction= tutorial.plan_cartesian_path(scale=-1)
    print('drawing H')
    coordinates_H = [[0, 0, 0], 
                   [0, 0, 2], 
                   [0, 0, 1], 
                   [2, 0, 1], 
                   [2, 0, 2],
                   [2, 0, 0]]
    coordlist_to_movement(coordinates_H)
    coordlist_to_movement([[0.5, 0, 0]])
    print('drawing K')
    coordinates_K = [[0, 0, 0], 
                   [0, 0, 2], 
                   [0, 0, 1], 
                   [1, 0, 1], 
                   [2, 0, 0],
                   [1, 0, 1], 
                   [2, 0, 2]] 
    coordlist_to_movement([[0.5, 0, 0]])
    coordlist_to_movement(coordinates_K)
    print('drawing U')
    coordinates_U = [[0, 0, 0],
                   [0, 0, -1], 
                   [(1+math.cos(math.radians(202.5))),       0, (-1 +math.sin(math.radians(202.5)))],   
                   [1+math.cos(math.radians(225)),         0, -1 +math.sin(math.radians(225))],   
                   [1+math.cos(math.radians(247.5)),    0, -1 +math.sin(math.radians(247.5))], 
                   [1, 0, -2], 
                   [1+math.cos(math.radians(292.5)),     0, -1 +math.sin(math.radians(292.5))], 
                   [1+math.cos(math.radians(315)),       0, -1 + math.sin(math.radians(315))], 
                   [1+math.cos(math.radians(337.5)),       0, -1 + math.sin(math.radians(337.5))], 
                   [2, 0, -1], 
                   [2, 0, 0]] 
    coordlist_to_movement([[0.5, 0, 0]])
    coordlist_to_movement(coordinates_U)
    
    print "============ Press `Enter` to go back to start position ..."
 
    raw_input()
    tutorial.go_to_joint_state(270, -60,120,-57,90,0)

    



    # for id, item in enumerate(coordinates_):
    #   x_goal, y_goal, z_goal = item[0],item[1], item[2]
    #   x_delta, y_delta, z_delta = x_goal-x_0, y_goal-y_0, z_goal-z_0
    #   print('next movement:', x_delta, y_delta, z_delta)    
    #   raw_input()

    #   master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= x_delta, y= y_delta, z =z_delta)
    #   tutorial.execute_plan(master_plan)
    #   x_0, y_0, z_0 = x_goal, y_goal, z_goal
      

    # master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= 1, y= 0, z =0)
    # print("Draw square")
    # tutorial.execute_plan(master_plan)

    # master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= 0, y= 0, z =1)
    # tutorial.execute_plan(master_plan)
    # master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= -1, y= 0, z =0)
    # tutorial.execute_plan(master_plan)
    # master_plan, fraction= tutorial.plan_cartesian_path_mod(scale=-1, x= 0, y= 0, z =-1)
    # tutorial.execute_plan(master_plan)

    # print "============ Press `Enter` to execute a movement using a pose goal ..."
    # # raw_input()
    # tutorial.go_to_pose_goal(0.5,0.5, 0 )
    # print("Position 2")
    # raw_input()
    
    print "============ Press `Enter` to reset"
    raw_input()
    # tutorial.go_to_joint_state(30,-30,0,0,0,0)

  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()

## BEGIN_TUTORIAL
## .. _moveit_commander:
##    http://docs.ros.org/kinetic/api/moveit_commander/html/namespacemoveit__commander.html
##
## .. _MoveGroupCommander:
##    http://docs.ros.org/kinetic/api/moveit_commander/html/classmoveit__commander_1_1move__group_1_1MoveGroupCommander.html
##
## .. _RobotCommander:
##    http://docs.ros.org/kinetic/api/moveit_commander/html/classmoveit__commander_1_1robot_1_1RobotCommander.html
##
## .. _PlanningSceneInterface:
##    http://docs.ros.org/kinetic/api/moveit_commander/html/classmoveit__commander_1_1planning__scene__interface_1_1PlanningSceneInterface.html
##
## .. _DisplayTrajectory:
##    http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/DisplayTrajectory.html
##
## .. _RobotTrajectory:
##    http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/RobotTrajectory.html
##
## .. _rospy:
##    http://docs.ros.org/kinetic/api/rospy/html/
## CALL_SUB_TUTORIAL imports
## CALL_SUB_TUTORIAL setup
## CALL_SUB_TUTORIAL basic_info
## CALL_SUB_TUTORIAL plan_to_joint_state
## CALL_SUB_TUTORIAL plan_to_pose
## CALL_SUB_TUTORIAL plan_cartesian_path
## CALL_SUB_TUTORIAL display_trajectory
## CALL_SUB_TUTORIAL execute_plan
## CALL_SUB_TUTORIAL add_box
## CALL_SUB_TUTORIAL wait_for_scene_update
## CALL_SUB_TUTORIAL attach_object
## CALL_SUB_TUTORIAL detach_object
## CALL_SUB_TUTORIAL remove_object
## END_TUTORIAL

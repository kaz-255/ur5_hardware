;; Auto-generated. Do not edit!


(when (boundp 'ur_dashboard_msgs::SetModeGoal)
  (if (not (find-package "UR_DASHBOARD_MSGS"))
    (make-package "UR_DASHBOARD_MSGS"))
  (shadow 'SetModeGoal (find-package "UR_DASHBOARD_MSGS")))
(unless (find-package "UR_DASHBOARD_MSGS::SETMODEGOAL")
  (make-package "UR_DASHBOARD_MSGS::SETMODEGOAL"))

(in-package "ROS")
;;//! \htmlinclude SetModeGoal.msg.html


(defclass ur_dashboard_msgs::SetModeGoal
  :super ros::object
  :slots (_target_robot_mode _stop_program _play_program ))

(defmethod ur_dashboard_msgs::SetModeGoal
  (:init
   (&key
    ((:target_robot_mode __target_robot_mode) (instance ur_dashboard_msgs::RobotMode :init))
    ((:stop_program __stop_program) nil)
    ((:play_program __play_program) nil)
    )
   (send-super :init)
   (setq _target_robot_mode __target_robot_mode)
   (setq _stop_program __stop_program)
   (setq _play_program __play_program)
   self)
  (:target_robot_mode
   (&rest __target_robot_mode)
   (if (keywordp (car __target_robot_mode))
       (send* _target_robot_mode __target_robot_mode)
     (progn
       (if __target_robot_mode (setq _target_robot_mode (car __target_robot_mode)))
       _target_robot_mode)))
  (:stop_program
   (&optional __stop_program)
   (if __stop_program (setq _stop_program __stop_program)) _stop_program)
  (:play_program
   (&optional __play_program)
   (if __play_program (setq _play_program __play_program)) _play_program)
  (:serialization-length
   ()
   (+
    ;; ur_dashboard_msgs/RobotMode _target_robot_mode
    (send _target_robot_mode :serialization-length)
    ;; bool _stop_program
    1
    ;; bool _play_program
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; ur_dashboard_msgs/RobotMode _target_robot_mode
       (send _target_robot_mode :serialize s)
     ;; bool _stop_program
       (if _stop_program (write-byte -1 s) (write-byte 0 s))
     ;; bool _play_program
       (if _play_program (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; ur_dashboard_msgs/RobotMode _target_robot_mode
     (send _target_robot_mode :deserialize buf ptr-) (incf ptr- (send _target_robot_mode :serialization-length))
   ;; bool _stop_program
     (setq _stop_program (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _play_program
     (setq _play_program (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get ur_dashboard_msgs::SetModeGoal :md5sum-) "a32b63f0e8a660b2b96916617d699c39")
(setf (get ur_dashboard_msgs::SetModeGoal :datatype-) "ur_dashboard_msgs/SetModeGoal")
(setf (get ur_dashboard_msgs::SetModeGoal :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
# This action is for setting the robot into a desired mode (e.g. RUNNING) and safety mode into a
# non-critical state (e.g. NORMAL or REDUCED), for example after a safety incident happened.

# goal
ur_dashboard_msgs/RobotMode target_robot_mode

# Stop program execution before restoring the target mode. Can be used together with 'play_program'.
bool stop_program

# Play the currently loaded program after target mode is reached.#
# NOTE: Requesting mode RUNNING in combination with this will make the robot continue the motion it
# was doing before. This might probably lead into the same problem (protective stop, EM-Stop due to
# faulty motion, etc.) If you want to be safe, set the 'stop_program' flag below and manually play
# the program after robot state is returned to normal.
# This flag will only be used when requesting mode RUNNING
bool play_program


================================================================================
MSG: ur_dashboard_msgs/RobotMode
int8 NO_CONTROLLER=-1
int8 DISCONNECTED=0
int8 CONFIRM_SAFETY=1
int8 BOOTING=2
int8 POWER_OFF=3
int8 POWER_ON=4
int8 IDLE=5
int8 BACKDRIVE=6
int8 RUNNING=7
int8 UPDATING_FIRMWARE=8

int8 mode


")



(provide :ur_dashboard_msgs/SetModeGoal "a32b63f0e8a660b2b96916617d699c39")



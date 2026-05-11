#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped, PoseStamped
from std_msgs.msg import String
from nav_msgs.msg import Odometry, Path
from sensor_msgs.msg import JointState

import tf_transformations
import tf2_ros
from builtin_interfaces.msg import Time

import sys
import time
import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, AXIS_STATE_IDLE
import fibre
import math

class OdriveMotorControl(Node):
    def __init__(self):
        super().__init__('odrive_odom_pub')

        #---------------------------------------------
        # Connect to Odrive
        self.find_odrive()
        
        # setup parameter
        self.tire_tread         = 0.55                                       #[m] distance between wheel centres
        self.target_linear_vel  = 0.0                                          #[m/s]
        self.target_angular_vel = 0.0                                          #[rad/s]
        self.tire_diameter      = 0.168                                        #[m]
        self.right_wheel_radius = self.tire_diameter                           #[m]
        self.left_wheel_radius  = self.tire_diameter                           #[m]
        self.encoder_cpr        = 90.0                                         #[count]
        self.tire_circumference = math.pi * self.tire_diameter                 #[m]
        self.m_t_to_value       = 1.0 / (self.tire_circumference)              #[turns/s]
        self.m_s_to_value       = self.encoder_cpr / (self.tire_circumference) #[count/s]
        self.vel_l = 0.0     #[count/s]
        self.vel_r = 0.0     #[count/s]
        self.new_pos_l = 0.0 #[count]
        self.new_pos_r = 0.0 #[count]
        self.old_pos_l = 0.0 #[count]
        self.old_pos_r = 0.0 #[count]
        self.wheel_offset = 0.195

        self.x = 0.0     #[m]
        self.y = 0.0     #[m]
        self.theta = 0.0 #[rad]

        
        self.poses_list = []


        self.odom_frame = "map"
        self.base_frame = "base_footprint"
        self.joint_state_pub = self.create_publisher(JointState, "/joint_states", 10)

        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = self.odom_frame
        self.odom_msg.child_frame_id  = self.base_frame
        self.odom_msg.pose.pose.position.x = 0.0
        self.odom_msg.pose.pose.position.y = 0.0
        self.odom_msg.pose.pose.position.z = 0.0    # always on the ground, we hope
        self.odom_msg.pose.pose.orientation.x = 0.0 # always vertical
        self.odom_msg.pose.pose.orientation.y = 0.0 # always vertical
        self.odom_msg.pose.pose.orientation.z = 0.0
        self.odom_msg.pose.pose.orientation.w = 1.0
        self.odom_msg.twist.twist.linear.x = 0.0
        self.odom_msg.twist.twist.linear.y = 0.0  # no sideways
        self.odom_msg.twist.twist.linear.z = 0.0  # or upwards... only forward
        self.odom_msg.twist.twist.angular.x = 0.0 # or roll
        self.odom_msg.twist.twist.angular.y = 0.0 # or pitch... only yaw
        self.odom_msg.twist.twist.angular.z = 0.0

        # subscriber cmd_vel
        self.create_subscription(Twist, '/cmd_vel_mux', self.callback_vel, 50)

        self.timer = self.create_timer(0.05, self.update) 

        # publish odom
        self.odom_publisher = self.create_publisher(Odometry, "/odrive_odom", 50)

    def callback_vel(self, msg):
        #self.get_logger().info('Callback received a velocity message.')
        #self.get_logger().info('I heard: "%s"' % msg.linear.x)
        self.target_linear_vel = msg.linear.x
        self.target_angular_vel = msg.angular.z

    def find_odrive(self):
        while True:
            self.get_logger().info("Connect to Odrive...")
            self.odrv0 = odrive.find_any()
            if self.odrv0 is not None:
                self.get_logger().info("Connect to Odrive Success!!!")
                break
            else:
                self.get_logger().info("Disconnect to Odrive...")

    def odrive_setup(self):
        self.get_logger().info("start setup...")
        self.get_logger().info("%s" % self.odrv0.vbus_voltage)
        self.initial_pos_r = 0.0
        self.initial_pos_l = 0.0
        self.odrv0.axis1.controller.config.control_mode = 2
        self.odrv0.axis0.controller.config.control_mode = 2
        self.odrv0.axis0.encoder.set_linear_count(self.initial_pos_r)
        self.odrv0.axis1.encoder.set_linear_count(self.initial_pos_l)

        self.get_logger().info("self.odrv0.axis0.encoder.pos_estimate : %s" % self.odrv0.axis0.encoder.pos_estimate)
        self.get_logger().info("self.odrv0.axis1.encoder.pos_estimate : %s" % self.odrv0.axis1.encoder.pos_estimate)

        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.input_vel = 0
        self.odrv0.axis1.controller.input_vel = 0
    
    def update(self):
        current_time = self.get_clock().now().to_msg()
        right_vel, left_vel = self.calc_relative_vel(self.target_linear_vel, self.target_angular_vel)
        self.calcodom(current_time)
        self.odrv0.axis0.controller.input_vel = right_vel
        self.odrv0.axis1.controller.input_vel = -left_vel
        #self.get_logger().info("right_vel : {} Left vel : {}".format(right_vel,left_vel))

        motor_current_0 = self.odrv0.axis0.motor.current_control.Iq_measured
        motor_current_1 = self.odrv0.axis1.motor.current_control.Iq_measured

        torque_constant_0 = self.odrv0.axis0.motor.config.torque_constant
        torque_constant_1 = self.odrv0.axis1.motor.config.torque_constant

        torque_0 = motor_current_0 * torque_constant_0
        torque_1 = motor_current_1 * torque_constant_1
        
    def calc_relative_vel(self, target_linear_vel, target_angular_vel):
        
        d_x = self.wheel_offset    
        d_y = self.tire_tread / 2.0
        
        # right_vel = (target_linear_vel + target_angular_vel * d_y) / self.tire_circumference
        # left_vel  = (target_linear_vel - target_angular_vel * d_y) / self.tire_circumference

        right_speed = math.sqrt((target_linear_vel + target_angular_vel * d_y)**2 + (target_angular_vel * d_x)**2)
        left_speed  = math.sqrt((target_linear_vel - target_angular_vel * d_y)**2 + (target_angular_vel * d_x)**2)
        right_vel = right_speed / self.tire_circumference
        left_vel  = left_speed  / self.tire_circumference

        return right_vel, left_vel
    
    def calcodom(self, current_time):

        self.new_pos_r = self.encoder_cpr * self.odrv0.axis0.encoder.pos_estimate #[count]
        self.new_pos_l = self.encoder_cpr * self.odrv0.axis1.encoder.pos_estimate #[count]
        
        delta_pos_r = self.new_pos_r - self.old_pos_r #[count]
        delta_pos_l = self.new_pos_l - self.old_pos_l #[count]
        
        self.old_pos_r = self.new_pos_r #[count]
        self.old_pos_l = self.new_pos_l #[count]
        
        half_cpr = self.encoder_cpr / 2.0
        if delta_pos_r >  half_cpr: 
            delta_pos_r = delta_pos_r - self.encoder_cpr
        elif delta_pos_r < -half_cpr: 
            delta_pos_r = delta_pos_r + self.encoder_cpr
        if delta_pos_l >  half_cpr: 
            delta_pos_l = delta_pos_l - self.encoder_cpr
        elif delta_pos_l < -half_cpr: 
            delta_pos_l = delta_pos_l + self.encoder_cpr

        self.joint_state = JointState()
        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        self.joint_state.name = ['base_left_back_wheel_joint', 'base_right_back_wheel_joint']
        self.joint_state.position = [self.new_pos_l, self.new_pos_r]
        self.joint_state.velocity = [self.vel_l, self.vel_r]
        self.joint_state.effort = [0.0,0.0,0.0,0.0]
        self.joint_state_pub.publish(self.joint_state)
        
        # convert [turns] into [m]
        delta_pos_r_m = delta_pos_r / self.m_s_to_value
        delta_pos_l_m = delta_pos_l / self.m_s_to_value * (-1)
        
        # Distance travelled
        d = (delta_pos_r_m + delta_pos_l_m) / 2.0  # delta_ps
        th = (delta_pos_r_m - delta_pos_l_m) / self.tire_tread # works for small angles
    
        xd = math.cos(th)*d
        yd = -math.sin(th)*d

        self.x += math.cos(self.theta)*xd - math.sin(self.theta)*yd
        self.y += math.sin(self.theta)*xd + math.cos(self.theta)*yd
        self.theta = (self.theta + th) % (2*math.pi)

        self.vel_r = self.encoder_cpr * self.odrv0.axis0.encoder.vel_estimate
        self.vel_l = self.encoder_cpr * self.odrv0.axis1.encoder.vel_estimate * (-1)
        v = self.tire_circumference * (self.vel_r + self.vel_l) / (2.0*self.encoder_cpr)
        w = self.tire_circumference * (self.vel_r - self.vel_l) / (self.tire_tread * self.encoder_cpr) # angle: vel_r*tyre_radius - vel_l*tyre_radius

        x_center = self.x + self.wheel_offset * math.cos(self.theta)
        y_center = self.y + self.wheel_offset * math.sin(self.theta)

        vx_center = v * math.cos(self.theta) - self.wheel_offset * math.sin(self.theta) * w
        vy_center = v * math.sin(self.theta) + self.wheel_offset * math.cos(self.theta) * w
        
        v_center = math.sqrt(vx_center**2 + vy_center**2)
        
        #v_center = v  # for lower precission

        self.odom_msg.header.stamp = current_time
        self.odom_msg.pose.pose.position.x = x_center
        self.odom_msg.pose.pose.position.y = y_center
        q = tf_transformations.quaternion_from_euler(0.0, 0.0, self.theta)
        self.odom_msg.pose.pose.orientation.z = q[2] # math.sin(self.theta)/2
        self.odom_msg.pose.pose.orientation.w = q[3] # math.cos(self.theta)/2
        self.odom_msg.twist.twist.linear.x  = v_center
        self.odom_msg.twist.twist.angular.z = w
        self.odom_publisher.publish(self.odom_msg)
    
    def fini(self):
        self.get_logger().info("shutdown...")
        self.odrv0.axis0.controller.input_vel = 0
        self.odrv0.axis1.controller.input_vel = 0
        self.odrv0.axis0.requested_state = AXIS_STATE_IDLE
        self.odrv0.axis1.requested_state = AXIS_STATE_IDLE

def main(args=None):
    rclpy.init(args=args)
    Odrive_motor_control = OdriveMotorControl()
    Odrive_motor_control.odrive_setup()
    try:
        rclpy.spin(Odrive_motor_control)
    finally:
        Odrive_motor_control.fini()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

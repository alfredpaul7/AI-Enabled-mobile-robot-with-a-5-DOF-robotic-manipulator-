import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class mux(Node):
    def __init__(self):
        super().__init__('mux')
        self.get_logger().info('mux node has been started')
        self.cmd1 = self.create_subscription(Twist, '/joy_cmd_vel', self.cmd1_callback, 10)
        self.cmd2 = self.create_subscription(Twist, '/cmd_vel_nav', self.cmd2_callback, 10)
        # self.lock = False
        self.pub = self.create_publisher(Twist, '/cmd_vel_mux', 10)

    def cmd1_callback(self, msg):
        msg.linear.x = msg.linear.x * 5.0
        msg.angular.z = msg.angular.z * 5.0
        self.pub.publish(msg)
        # self.lock = False

    def cmd2_callback(self, msg):
        msg.linear.x = msg.linear.x * 5.0
        msg.angular.z = msg.angular.z * 5.0
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    mux_node = mux()
    rclpy.spin(mux_node)
    mux_node.destroy_node()
    rclpy.shutdown()

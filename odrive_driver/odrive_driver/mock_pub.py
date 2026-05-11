import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class publishVel(Node):
    def __init__(self):
        super().__init__('publishVel')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5
        msg.angular.z = 0.1
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    publish_vel = publishVel()

    rclpy.spin(publish_vel)

    publish_vel.destroy_node()
    rclpy.shutdown()
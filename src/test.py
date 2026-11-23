import sys
import math
import rclpy
import random
from ros_gz_interfaces.srv import SpawnEntity, DeleteEntity
import subprocess
import os
import signal


def main():
    rclpy.init()
    node = rclpy.create_node('simple_spawner')


    if sys.argv[1] == 'gen':
        client = node.create_client(SpawnEntity, '/world/clover2_aruco/create')

        bridge = None

        if not client.wait_for_service(timeout_sec=1.0):
            bridge = subprocess.Popen(
                [
                    "ros2", "run", "ros_gz_bridge", "parameter_bridge",
                    "/world/clover2_aruco/create@ros_gz_interfaces/srv/SpawnEntity"
                ],
                start_new_session=True
            )

        client.wait_for_service()

        req = SpawnEntity.Request()
        req.entity_factory.name = f'lep_{i}'
        req.entity_factory.sdf_filename = '/home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/isol_red/model.sdf'
        req.entity_factory.pose.position.x = 3
        req.entity_factory.pose.position.y = 3
        req.entity_factory.pose.position.z = 1.2

        #req.entity_factory.pose.orientation.x = 0.0
        #req.entity_factory.pose.orientation.y = 0.0
        #req.entity_factory.pose.orientation.z = math.sin(dat[2] / 2.0)
        #req.entity_factory.pose.orientation.w = math.cos(dat[2] / 2.0)

    if bridge is not None:
        os.killpg(os.getpgid(bridge.pid), signal.SIGTERM)
       

if __name__ == '__main__':
    main()

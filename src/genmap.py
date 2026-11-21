import sys
import math
import rclpy
import random
from ros_gz_interfaces.srv import SpawnEntity, DeleteEntity
import subprocess
import os
import signal

x_min = 0
x_max = 8

y_min = 1
y_max = 8

map_x_cent = 4.5
map_y_cent = 4.5



def get_dist(cords) -> float:    # cords = [[x1, y1], [x2, y2]]
    x1, y1 = cords[0]
    x2, y2 = cords[1]

    dx = x1 - x2
    dy = y1 - y2

    return math.sqrt(dx**2 + dy**2)



def gen_lep_cords() -> list:
    cords = []

    x1 = round(random.uniform(x_min, x_max), 2)
    y1 = round(random.uniform(y_min, y_max), 2)

    cords.append((x1, y1))

    while len(cords) < 2:
        r = random.randint(5, 10)
        theta = random.uniform(0, 2 * math.pi)
        x = round(x1 + r * math.cos(theta), 2)
        y = round(y1 + r * math.sin(theta), 2)

        if x > x_min and x < x_max and y > y_min and y < y_max and get_dist(((x, y), (x1, y1))) < 10 and get_dist(((x, y), (x1, y1))) > 5:
            cords.append((x,y))

    cent_x = round((x + x1)/2, 2)
    cent_y = round((y + y1)/2, 2)

    while len(cords) < 3:
        r = random.randint(1, 4)
        theta = random.uniform(0, 2 * math.pi)
        x = round(cent_x + r * math.cos(theta), 2)
        y = round(cent_y + r * math.sin(theta), 2)

        if x > x_min and x < x_max and y > y_min and y < y_max and get_dist(((x, y), (cords[0][0], cords[0][1]))) > 1 and get_dist(((x, y), (cords[1][0], cords[1][1]))) > 1:
            cords.append((x, y))

    return cords



def is_ros_node_running(node_name: str) -> bool:
    result = subprocess.run(['ros2', 'node', 'list'], capture_output=True, text=True)
    active_nodes = result.stdout.splitlines()
    for name in active_nodes:
        if name == node_name:
            return True

    return False



def main():
    rclpy.init()
    node = rclpy.create_node('simple_spawner')

    if len(sys.argv) < 2:
        print('No args ???')
        return        

    elif sys.argv[1] == 'gen':

        bridge = subprocess.Popen(
            [
                "ros2", "run", "ros_gz_bridge", "parameter_bridge",
                "/world/clover2_aruco/create@ros_gz_interfaces/srv/SpawnEntity"
            ],
            start_new_session=True
        )


        client = node.create_client(SpawnEntity, '/world/clover2_aruco/create')
        client.wait_for_service()


        cords = gen_lep_cords()


        for i, cord in enumerate(cords, 1):
            req = SpawnEntity.Request()
            req.entity_factory.name = f'lep_{i}'
            req.entity_factory.sdf_filename = '/home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/lep_model/model.sdf'
            req.entity_factory.pose.position.x = cord[0]
            req.entity_factory.pose.position.y = cord[1]
            req.entity_factory.pose.position.z = 0.0

            req.entity_factory.pose.orientation.z = 0.0
            req.entity_factory.pose.orientation.y = math.pi/2
            req.entity_factory.pose.orientation.w = 0.0

                    # 3. Отправляем запрос и ждём результат
            future = client.call_async(req)
            rclpy.spin_until_future_complete(node, future)
            print(f'Результат спавна ЛЭП {i}:', future.result().success)



    elif sys.argv[1] == 'clear':

        bridge = subprocess.Popen(
            [
                'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
                '/world/clover2_aruco/remove@ros_gz_interfaces/srv/DeleteEntity'
            ],
            start_new_session=True
        )


        client = node.create_client(DeleteEntity, '/world/clover2_aruco/remove')
        client.wait_for_service()


        for i in range(1, 4):
            req = DeleteEntity.Request()
            req.entity.name = f'lep_{i}'
            req.entity.type = 2  # 2 = MODEL (тип сущности в Gazebo)

            future = client.call_async(req)
            rclpy.spin_until_future_complete(node, future)
            print(f'Результат удаления ЛЭП {i}:', future.result().success)



    os.killpg(os.getpgid(bridge.pid), signal.SIGTERM)


    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()

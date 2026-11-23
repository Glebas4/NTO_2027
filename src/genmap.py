import sys
import math
import rclpy
import random
from ros_gz_interfaces.srv import SpawnEntity, DeleteEntity
import subprocess
import os
import signal

x_min = 0
x_max = 9

y_min = 1
y_max = 9

map_x_cent = 4.5
map_y_cent = 4.5


def get_dist(cords) -> float:    # cords = [[x1, y1], [x2, y2]]
    x1, y1 = cords[0]
    x2, y2 = cords[1]

    dx = x1 - x2
    dy = y1 - y2

    return math.sqrt(dx**2 + dy**2)



def gen_lep_cords() -> list:
    global x_min, x_max, y_min, y_max
    cords = []

    x1 = round(random.uniform(x_min, x_max), 2)
    y1 = round(random.uniform(y_min, y_max), 2)

    cords.append((x1, y1))

    dx = x1 - map_x_cent
    dy = y1 - map_y_cent

    if dx < 0:
        x_min = x1 + 2
        x_max -= 3

    else:
        x_max = x1 - 2
        x_min += 3

    if dy > 0:
        y_max = y1 - 2
        y_min += 3

    else:
        y_min = y1 + 2
        y_max -= 3


    #while len(cords) < 2:
    x2 = round(random.uniform(x_min, x_max), 2)
    y2 = round(random.uniform(y_min, y_max), 2)

    cords.append((x2, y2))


    if dx < 0:
        x_min = x1 + 4
        x_max = 8
    else:
        x_max = x1 - 4
        x_min = 0

    if dy > 0:
        y_max = y1 - 4
        y_min = 1
    else:
        y_min = y1 + 4
        y_max = 8


    while len(cords) < 3:
        x3 = round(random.uniform(x_min, x_max), 2)
        y3 = round(random.uniform(y_min, y_max), 2)

        d_1_3 = get_dist(((x3, y3), (x1, y1)))

        if d_1_3 > 5 and d_1_3 < 10 and get_dist(((x2, y2), (x3, y3))) > 1:
            cords.append((x3, y3))



    return cords



def gen_rots(cords: list) -> list:
    x1, y1 = cords[0]
    x2, y2 = cords[1]
    x3, y3 = cords[2]
    
    dx = x1-x2
    dy = y1-y2
    ang1 = math.atan((abs(dx)/abs(dy))) + math.pi/2


    if dx > 0:
        if dy < 0:
            ang1 = math.pi/2 + ang1
        else:
            ang1 = 3*math.pi/2 - ang1

    else:
        if dy > 0:
            ang1 = 3*math.pi/2 + ang1
        else:
            ang1 = math.pi/2 - ang1

    dx = x3 - x2
    dy = y3 - y2

    ang3 = math.atan((abs(dx)/abs(dy))) + math.pi/2

    if dx > 0:
        if dy < 0:
            ang3 = math.pi/2 + ang3
        else:
            ang3 = 3*math.pi/2 - ang3

    else:
        if dy > 0:
            ang3 = 3*math.pi/2 + ang3
        else:
            ang3 = math.pi/2 - ang3

    ang1 = random.choice([ang1, ang1 + math.pi])
    ang2 = random.choice([ang1, ang1 + math.pi])
    ang3 = random.choice([ang3, ang3 + math.pi])

    return [ang1, ang2, ang3]





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


        cords = gen_lep_cords()
        rots = gen_rots(cords)

        data = []

        for i in range(3):
            data.append((cords[i][0], cords[i][1], rots[i]))


        for i, dat in enumerate(data, 1):
            req = SpawnEntity.Request()
            req.entity_factory.name = f'lep_{i}'
            req.entity_factory.sdf_filename = '/home/pi/clover2-dev/src/clover2-sim/clover2_gz_sim/models/lep_model/model.sdf'
            req.entity_factory.pose.position.x = dat[0]
            req.entity_factory.pose.position.y = dat[1]
            req.entity_factory.pose.position.z = 0.0

            req.entity_factory.pose.orientation.x = 0.0
            req.entity_factory.pose.orientation.y = 0.0
            req.entity_factory.pose.orientation.z = math.sin(dat[2] / 2.0)
            req.entity_factory.pose.orientation.w = math.cos(dat[2] / 2.0)

                    # 3. Отправляем запрос и ждём результат
            future = client.call_async(req)
            rclpy.spin_until_future_complete(node, future)
            print(f'Результат спавна ЛЭП {i}:', future.result().success)



    elif sys.argv[1] == 'clear':
        client = node.create_client(DeleteEntity, '/world/clover2_aruco/remove')

        bridge = None

        if not client.wait_for_service(timeout_sec=1.0):
            bridge = subprocess.Popen(
                [
                    'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
                    '/world/clover2_aruco/remove@ros_gz_interfaces/srv/DeleteEntity'
                ],
                start_new_session=True
            )

        client.wait_for_service()


        for i in range(1, 4):
            req = DeleteEntity.Request()
            req.entity.name = f'lep_{i}'
            req.entity.type = 2  # 2 = MODEL (тип сущности в Gazebo)

            future = client.call_async(req)
            rclpy.spin_until_future_complete(node, future)
            print(f'Результат удаления ЛЭП {i}:', future.result().success)


    if bridge is not None:
        os.killpg(os.getpgid(bridge.pid), signal.SIGTERM)


    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()

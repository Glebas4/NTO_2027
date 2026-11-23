import time
from clover2 import Clover2

#drone = Clover2()
# или с именем ноды:
drone = Clover2("my_drone")
print('Жди')
time.sleep(5)


drone.arm()

drone.navigate_wait(frame_id="base_link", x=0.0, y=0.0, z=1.5, speed=1.0, yaw=0.0)
drone.navigate_wait(frame_id="map", x=0.0, y=3.0, z=1.5, speed=1.0, yaw=0.0)
drone.land()
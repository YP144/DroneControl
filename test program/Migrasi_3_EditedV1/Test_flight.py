import time
from pyardrone import ARDrone
drone = ARDrone()
drone.navdata_ready.wait()  # wait until NavData is ready
while not drone.state.fly_mask:
    drone.takeoff()
time.sleep(5)  # hover for a while
while drone.state.fly_mask:
    drone.land()

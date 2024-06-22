from pyardrone import ARDrone, at

drone_1 = ARDrone(host='192.168.1.11')
drone_2 = ARDrone(host='192.168.1.12')
drone_3 = ARDrone(host='192.168.1.13')
# drone = ARDrone()
drones = [drone_1, drone_2, drone_3]
for drone in drones:
    drone.land()
    drone.close()

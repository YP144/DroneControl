from pyardrone import ARDrone, at

drone = ARDrone(host='192.168.1.1')
# drone = ARDrone()
drone.send(at.CONFIG("video:video_channel", "3"))
drone.close()

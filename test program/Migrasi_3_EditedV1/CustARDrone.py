from pyardrone import ARDrone, at
from time import sleep
from Aruco import ArucoMarker
import numpy as np

class CustomArdrone:
    def __init__(self, id, ip, camera_ip=None):
        self.id = id
        self.ip = ip
        self.camera_ip = camera_ip
        self.drone = None
        self.battery = None
        self.vx = None
        self.vy = None
        self.vz = None
        self.yaw = None
        self.pitch = None
        self.roll = None
        self.altitude = None
        self.flying_state = None
        self.navdemo = None
        self.camera_condition = "2"
        self.aruco_detector = ArucoMarker(
            url=self.ip if self.camera_ip is None else 0)
        self.sending_state = False
        # self.aruco_detector = None
        self.aruco_data = {"ArUco Data": " ",
                           "Camera Active": False,
                           "Detector Active": False,
                           "Total Id": 0,
                           "Detected Id": " "}
        pass

    def connect(self):
        if self.drone is None:
            try:
                self.drone = ARDrone(host=self.ip)
                self.drone.send(at.CONFIG('general:navdata_demo', True))
            except:
                print("can not connected")
                self.drone = None
        else:
            if self.drone.state.navdata_bootstrap is not True:
                self.navdemo = self.drone.navdata.demo
                print("connected")
            else:
                print("navdata demo is problem")
                self.drone.send(at.CONFIG('general:navdata_demo', True))
                sleep(1.5)
                self.navdemo = self.drone.navdata.demo
            # print("connected")
            # try:
            #     self.navdemo = self.drone.navdata.demo
            # except:
            #     print("navdata demo is problem")
            #     self.drone.send(at.CONFIG('general:navdata_demo', True))
        sleep(0.5)

    def disconnect(self):
        self.drone.close()

    def get_battery(self):
        if self.drone is not None:
            if self.drone.navdata_ready.is_set():
                if self.navdemo is not None:
                    self.battery = self.navdemo.vbat_flying_percentage
        else:
            self.battery = "Not connected"
        return self.battery

    def get_navdata(self):
        if self.sending_state is False:
            if self.drone is not None:
                if self.navdemo is not None:
                    if self.drone.state.navdata_bootstrap is not True:
                        self.navdemo = self.drone.navdata.demo
                        self.vx = self.navdemo.vx/1000
                        self.vy = self.navdemo.vy/1000
                        self.vz = self.navdemo.vz/1000
                        self.yaw = self.navdemo.psi/1000
                        self.pitch = self.navdemo.theta/1000
                        self.roll = self.navdemo.phi/1000
                        self.altitude = self.navdemo.altitude
                        self.flying_state = self.drone.state.fly_mask
                else:
                    if self.drone.state.navdata_bootstrap is not True:
                        self.navdemo = self.drone.navdata.demo
                    else:
                        print("navdata demo is problem")
                        self.drone.send(
                            at.CONFIG('general:navdata_demo', True))

    def move(self,
             forward=0.0,
             backward=0.0,
             right=0.0,
             left=0.0,
             up=0.0,
             down=0.0,
             cw=0.0,
             ccw=0.0,
             **dir_speed):
        if self.drone != None:
            self.drone.move(forward=forward, backward=backward,
                            right=right, left=left, up=up, down=down, cw=cw, ccw=ccw)

    def takeoff(self):
        print('takeoff')
        self.drone.takeoff()

    def land(self):
        print('landing')
        self.drone.land()

    def read_config(self):
        pass

    def trim(self):
        self.drone.send(at.FTRIM())
        sleep(1)
        # self.drone.send(
        #     at.CONFIG('video:bitrate_control_mode', '1'))
        # sleep(1)
        # self.drone.send(
        #     at.CONFIG('video:video_fps', '30'))
        # sleep(1)
        # self.drone.send(
        #     at.CONFIG('video:video_codec', '129'))
        # sleep(1)
        # self.drone.send(
        #     at.CONFIG('video:max_bitrate', '4000'))

    def calib(self):
        self.drone.send(at.CALIB(0))

    def change_camera(self):
        self.sending_state = True
        if self.camera_condition == "2":
            self.camera_condition = "3"
            # sleep(0.5)
            self.drone.send(
                at.CONFIG("video:video_channel", self.camera_condition))
        else:
            self.camera_condition = "2"
            # sleep(0.5)
            self.drone.send(
                at.CONFIG("video:video_channel", self.camera_condition))
        self.sending_state = False
        pass

    def marker_process(self):
        if self.aruco_data['Camera Active'] is True or self.aruco_data['Detector Active'] is True:
            if self.aruco_detector is None:
                self.aruco_detector = ArucoMarker(
                    url=self.ip if self.camera_ip is None else 0)
            else:
                self.aruco_detector.active_camera = self.aruco_data['Camera Active']
                self.aruco_detector.active_detector = self.aruco_data['Detector Active']
                self.aruco_detector.run()
                if self.aruco_data['Detector Active'] == True:
                    if self.aruco_detector.get_ids() is not None:
                        self.aruco_data['Total Id'] = len(
                            self.aruco_detector.get_ids())
                        if self.aruco_data['Total Id'] == 1:
                            self.aruco_data['Detected Id'] = self.aruco_detector.get_ids()[
                                0][0]
                        else:
                            self.aruco_data['Detected Id'] = " "
                            for id in self.aruco_detector.get_ids():
                                self.aruco_data[f'{np.where(self.aruco_detector.get_ids()==id)[0]}'] = id
                    else:
                        self.aruco_data['Detected Id'] = "None"
        else:
            pass
import pygame as py
import cv2 as cv

class ArucoMarker:
    def __init__(self, url=0):
        self.url = url
        self.camera_url = 'tcp://'+self.url+':5555' if self.url != 0 else 0
        self.camera = cv.VideoCapture(self.camera_url)
        # self.camera = cv.VideoCapture(self.url)
        # self.camera.set(cv.CAP_PROP_BUFFERSIZE, 1)
        self.active_camera = False
        self.active_detector = False
        self.ids = None
        self.draw = False
        self.brightness = 1
        self.contrast = 0.75
        self.ret = False
        self.frame = None
        self.image_scale = 1

    def init_pygame(self):
        self.default_surface = py.Surface((200, 200)).convert_alpha()
        self.rotated_surface = self.default_surface
        self.stpwtch = Stopwatch()

    def read(self):
        self.ret, self.raw_frame = self.camera.read()
        self.raw_frame = self.raw_frame[0:200, 240:400]
        # self.raw_frame = self.camera.read()
        # self.raw_frame = cv.resize(
        #             self.raw_frame, (480, 360), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
        # cv.waitKey(0)

    def run(self):
        # if self.camera is None:
        #     self.camera = cv.VideoCapture(self.ardrone_url)
        # self.img = imutils.resize(self.raw_frame, width=700, height=500)
        self.read()
        if self.active_camera == True:

            # self.final_frame = cv.cvtColor(self.raw_frame, cv.COLOR_BGR2HSV)
            # self.final_frame[:, :, 2] = np.clip(
            # self.contrast * self.final_frame[:, :, 2] + self.brightness, 0, 255)
            # self.final_frame_end = cv.cvtColor(self.final_frame, cv.COLOR_HSV2BGR)
            # time.sleep(0.001)
            # cv.waitKey(1)
            if self.ret:
                self.frame = cv.cvtColor(
                    self.raw_frame, cv.COLOR_BGR2RGB)

                if self.active_detector == True:
                    if self.draw:
                        cv.aruco.drawDetectedMarkers(self.frame, self.bboxs)
                # self.surface = py.surfarray.make_surface(self.frame)
                # self.surface.convert_alpha()
                # self.rotated_surface = py.transform.rotozoom(
                #     self.surface, -90, 0.5).convert_alpha()

        if self.active_detector == True:
            if self.ret:
                self.findArucoMarkers()
        # self.camera.release()
        #     cv.destroyAllWindows()
        # self.read()

    def draw_pygame(self):
        if self.ret:
            if self.frame is not None:
                self.surface = py.surfarray.make_surface(self.frame)
                self.surface.convert_alpha()
                self.rotated_surface = py.transform.rotozoom(
                    self.surface, -90, self.image_scale).convert_alpha()

    def findArucoMarkers(self, markerSize=6, totalMarkers=100, draw=True):
        imgGray = cv.cvtColor(self.raw_frame, cv.COLOR_BGR2GRAY)
        key = getattr(
            cv.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
        arucoDict = cv.aruco.Dictionary_get(key)
        arucoParam = cv.aruco.DetectorParameters_create()
        self.bboxs, self.ids, _ = cv.aruco.detectMarkers(
            imgGray, arucoDict, parameters=arucoParam)
        self.draw = draw
        # print(ids)

    def get_image(self):
        return self.rotated_surface

    def get_ids(self):
        return self.ids

    def done(self):
        self.camera.release()
        cv.destroyAllWindows()
        print("done")

class Stopwatch:
    def __init__(self):
        self.init_time = 0
        self.current_time = 0
        self.delta_time = 0
        self.starting = True

    def start(self):
        if self.init_time == 0:
            self.init_time = py.time.get_ticks()
        self.current_time = py.time.get_ticks()
        self.delta_time = (self.current_time - self.init_time)

    def stop(self):
        self.starting = False
        pass

    def reset(self):
        self.init_time = 0
        self.current_time = 0
        self.delta_time = 0
        pass
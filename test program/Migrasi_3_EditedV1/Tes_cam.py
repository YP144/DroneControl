import cv2 as cv
import time
import threading

# class VideoCapture:
#     def __init__(self, name):
#         self.cap = cv.VideoCapture(name)
#         self.lock = threading.Lock()
#         self.t = threading.Thread(target=self._reader)
#         self.t.daemon = True
#         self.t.start()

#     # grab frames as soon as they are available
#     def _reader(self):
#         while True:
#             with self.lock:
#                 ret = self.cap.grab()
#             if not ret:
#                 break

#     # retrieve latest frame
#     def read(self):
#         with self.lock:
#             _, frame = self.cap.read()
#         return frame

ardrone_url = 'tcp://192.168.1.1:5555'
# camera = VideoCapture(ardrone_url)

camera = cv.VideoCapture(ardrone_url)
# width = camera.get(3)
# height = camera.get(4)
# print(width, height)
# camera.set(cv.CAP_PROP_BUFFERSIZE, 0)
while True:
    ret,frame = camera.read()
    if ret == True:
        # fps = camera.get(cv.CAP_PROP_FPS)
        # print(fps)
        cv.imshow('test', frame)
        # test = camera.get(cv.CAP_PROP_BUFFERSIZE)
        # print("buffersize = ",test)

    elif ret == False:
        cv.imshow('test', frame)
        print("tidak ada gambar tertangkap")
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv.destroyAllWindows()

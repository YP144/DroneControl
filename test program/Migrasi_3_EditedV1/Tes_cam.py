import cv2 as cv
import time
ardrone_url = 'tcp://192.168.1.1:5555'
camera = cv.VideoCapture(ardrone_url)
# width = camera.get(3)
# height = camera.get(4)
# print(width, height)
# test = camera.get(cv.CAP_PROP_BUFFERSIZE)
# print(test)
while True:
    ret, frame = camera.read()
    if ret:
        # fps = camera.get(cv.CAP_PROP_FPS)
        # print(fps)
        cv.imshow('test', frame)
    elif ret == False:
        print("tidak ada gambar tertangkap")
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv.destroyAllWindows()

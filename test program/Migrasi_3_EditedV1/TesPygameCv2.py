from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import threading
ardrone_url = 'tcp://192.168.1.1:5555'
tes_android = 'http://192.168.1.100:8080/video'
camera = cv2.VideoCapture(0)
dict_img = {"ret": None,
            "frame": None}


def pygame_funct():
    pygame.init()
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    screen = pygame.display.set_mode([640, 480])
    clock = pygame.time.Clock()
    try:
        while 1:
            screen.fill([0, 0, 0])
            if dict_img["ret"] is not None:
                if dict_img["ret"]:

                    # frame = cv2.resize(frame, (480, 320), fx=0, fy=0,
                    #                    interpolation=cv2.INTER_CUBIC)
                    # frame = frame.swapaxes(0, 1)
                    # pygame.surfarray.blit_array(screen, frame)

                    surface_tes = pygame.surfarray.make_surface(
                        dict_img["frame"])
                    surface_tes.convert_alpha()
                    rot_surf = pygame.transform.rotozoom(
                        surface_tes, -90, 1).convert_alpha()
                    screen.blit(rot_surf, (0, 0))
                print(int(clock.get_fps()), end='\r')
                clock.tick(60)
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        pygame.quit()


def image_funct():
    try:
        while 1:
            dict_img["ret"], frame = camera.read()
            dict_img["frame"] = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB)
    except (KeyboardInterrupt, SystemExit):
        camera.release()
        cv2.destroyAllWindows()


def main():
    thread1 = threading.Thread(target=pygame_funct)
    thread2 = threading.Thread(target=image_funct)
    # thread1.setDaemon(True)
    # thread2.setDaemon(True)
    thread1.start()
    thread2.start()


if __name__ == '__main__':
    main()

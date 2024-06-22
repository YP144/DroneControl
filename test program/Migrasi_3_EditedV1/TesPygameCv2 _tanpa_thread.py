from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import threading
ardrone_url = 'tcp://192.168.1.1:5555'
tes_android = 'http://192.168.1.100:8080/video'
camera = cv2.VideoCapture(ardrone_url)
dict_img = {"ret": None,
            "frame": None}


def pygame_funct():
    pygame.init()
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    screen = pygame.display.set_mode([640, 480])
    try:
        while True:
            screen.fill([0, 0, 0])
            dict_img["ret"], dict_img["frame"] = camera.read()

            if dict_img["ret"]:
                dict_img["frame"] = cv2.cvtColor(
                    dict_img["frame"], cv2.COLOR_BGR2RGB)
                # frame = cv2.resize(frame, (480, 320), fx=0, fy=0,
                #                    interpolation=cv2.INTER_CUBIC)
                # frame = frame.swapaxes(0, 1)
                # pygame.surfarray.blit_array(screen, frame)
                surface_tes = pygame.surfarray.make_surface(
                    dict_img["frame"])
                surface_tes.convert_alpha()
                rot_surf = pygame.transform.rotozoom(surface_tes, -90, 1)
                screen.blit(rot_surf, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        pygame.quit()


if __name__ == '__main__':
    pygame_funct()

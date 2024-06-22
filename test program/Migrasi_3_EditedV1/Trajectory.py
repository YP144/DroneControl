import pygame as py


class Trajectory:
    def __init__(self, drone, track_points):
        self.drone = drone
        self.track_points = track_points
        self.store_track = []
        self.track_delay = 5
        self.time = 0
        self.font = py.font.SysFont('timesnewroman', 20)
        self.scale = 0.5
        self.current_target = py.Vector2(track_points[0])
        self.passed_type = "Point"
        self.base_pos = "real"
        self.error = 30
        self.track_distance = 0
        self.state = 'standby'

    def run(self, time):
        self.time = time
        if self.base_pos == "pixel":
            self.pixel_frame()
        elif self.base_pos == "real":
            self.real_frame()

    def pixel_frame(self):
        c = 0
        while c < len(self.track_points):
            if c-1 < len(self.store_track) < c+1:
                if self.drone.pos != self.track_points[c]:
                    if self.track_points[c] not in self.store_track:
                        self.current_target = py.Vector2(self.track_points[c])
                        rad, _ = (self.current_target -
                                  self.drone.pos).as_polar()
                        self.track_distance = rad
            if self.passed_type == "Time":
                if self.time == (self.track_delay*(c+1)):
                    if self.track_points[c] not in self.store_track:
                        self.store_track.append(self.track_points[c])
            elif self.passed_type == "Point":
                if self.track_distance < self.error:
                    if self.track_points[c] not in self.store_track:
                        self.store_track.append(self.track_points[c])
            # if self.track_delay != 0:
            #     if self.time == (self.track_delay*(c+1)):
            #         if self.track_points[c] not in self.store_track:
            #             self.store_track.append(self.track_points[c])
            # else:
            #     if tuple(self.drone.pos) == self.track_points[c]:
            #         if self.track_points[c] not in self.store_track:
            #             self.store_track.append(self.track_points[c])
            c += 1
        if len(self.store_track) == len(self.track_points):

            self.current_target = py.Vector2(0, 0)
        else:
            if self.current_target != py.Vector2(0, 0):

                self.drone.set_target(self.current_target)

    def real_frame(self):
        c = 0
        while c < len(self.track_points):
            if c-1 < len(self.store_track) < c+1:
                if self.drone.est_pos != self.track_points[c]:
                    if self.track_points[c] not in self.store_track:
                        self.current_target = py.Vector2(self.track_points[c])
                        rad, _ = (self.current_target -
                                  self.drone.est_pos).as_polar()
                        self.track_distance = rad
            if self.passed_type == "Time":
                if self.time == (self.track_delay*(c+1)):
                    if self.track_points[c] not in self.store_track:
                        self.store_track.append(self.track_points[c])
            elif self.passed_type == "Point":
                if self.track_distance < self.error:
                    if self.track_points[c] not in self.store_track:
                        self.store_track.append(self.track_points[c])
            c += 1
        if len(self.store_track) == len(self.track_points):
            # self.current_target = py.Vector2(0, 0)
            self.state = 'finish'
            pass
        else:
            self.state = 'process'
            self.drone.est_set_target(self.current_target)

    def draw_points(self, surface):
        self.surface = surface
        if self.base_pos == "pixel":
            # self.font = py.font.SysFont('timesnewroman', int(20*self.scale))
            for track_point in self.track_points:
                track_index = self.track_points.index(track_point)
                # pixel_point = py.Vector2((track_point[0]/1.2)+105,
                #                          (track_point[1]/1.8)+175)
                textsurface = self.font.render(
                    str(f'{track_index+1} {track_point}'), False, (255, 0, 0)).convert_alpha()
                self.surface.blit(
                    textsurface, (track_point[0], track_point[1]+10))
                py.draw.circle(self.surface, (255, 0, 0),
                               track_point, int(10*self.scale), int(5*self.scale))
        elif self.base_pos == "real":
            # self.font = py.font.SysFont('timesnewroman', int(20*self.scale))
            for track_point in self.track_points:
                track_index = self.track_points.index(track_point)
                # pixel_point = py.Vector2((track_point[0]/1.2)+105,
                #                          (track_point[1]/1.8)+175)
                textsurface = self.font.render(
                    str(f'{track_index+1} {track_point}'), False, (255, 0, 0)).convert_alpha()
                self.surface.blit(
                    textsurface, ((track_point[0]/1.2)+105, (track_point[1]/1.2)+185))
                py.draw.circle(self.surface, (255, 0, 0),
                               ((track_point[0]/1.2)+105, (track_point[1]/1.2)+175), int(10*self.scale), int(5*self.scale))

    def draw_target_line(self):
        if len(self.store_track) != len(self.track_points) and self.current_target != py.Vector2(0, 0):
            py.draw.line(self.surface, (255, 0, 0),
                         self.drone.pos, self.current_target, 3)

    def reset(self):
        self.store_track = []
        self.state = 'standby'

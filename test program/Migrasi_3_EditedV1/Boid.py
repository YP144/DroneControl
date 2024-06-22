import numpy as np


class Boid:
    def __init__(self, Drones, exceptionId=0):
        self.drones = Drones
        self.exceptionId = exceptionId
        self.alignment_angle = 0
        self.base_pos = "real"
        self.drone_close = False
        self.drone_far = False
        self.all_angle = []
        for drone in self.drones:
            if drone.base_pos != self.base_pos:
                drone.base_pos = self.base_pos

    def run(self):
        self.separation(200)
        self.cohesion(400)
        self.alignment()

    def separation(self, radius):
        check_close_drone = []
        for drone in self.drones:
            if drone.flying_state == True:
                s_pos = []
                counter_avr_pos = ()
                s_drones = []
                if self.base_pos == "pixel":
                    s_pos.append(drone.pos)
                    s_drones = drone.nearby(self.drones, radius)
                    self.s_drones = s_drones
                    if s_drones != 0:
                        for s_drone in s_drones:
                            s_pos.append(s_drone.pos)
                    avr_pos = tuple(np.average(s_pos, axis=0))
                    avr_pos_relative = tuple(avr_pos - drone.pos)
                    counter_avr_pos = tuple([(x*(-1)) + drone.pos[avr_pos_relative.index(x)]
                                            for x in avr_pos_relative])
                    if len(s_drones) != 0:  # check ada drone atau tidak
                        if self.exceptionId == 0 or self.exceptionId != drone.id:  # check ada pengecualian atau tidak
                            drone.set_target(counter_avr_pos)
                elif self.base_pos == "real":
                    if drone.base_pos != self.base_pos:
                        drone.base_pos = self.base_pos
                    s_pos.append(drone.est_pos)
                    s_drones = drone.nearby(self.drones, radius)
                    self.s_drones = s_drones
                    if len(s_drones) != 0:
                        check_close_drone.append(True)
                        for s_drone in s_drones:
                            s_pos.append(s_drone.est_pos)
                    else:
                        check_close_drone.append(False)
                    avr_pos = tuple(np.average(s_pos, axis=0))
                    avr_pos_relative = tuple(avr_pos - drone.est_pos)
                    counter_avr_pos = tuple([(x*(-1)) + drone.est_pos[avr_pos_relative.index(x)]
                                            for x in avr_pos_relative])
                    if len(s_drones) != 0:  # check ada drone atau tidak
                        if self.exceptionId == 0 or self.exceptionId != drone.id:  # check ada pengecualian atau tidak
                            drone.est_set_target(counter_avr_pos)
            else:
                self.drones.remove(drone)
            if any(close_drone is True for close_drone in check_close_drone):
                self.drone_close = True
            else:
                self.drone_close = False

    def cohesion(self, radius):
        check_far_drone = []
        for drone in self.drones:
            if drone.flying_state == True:
                c_pos = []
                avr_pos = ()
                c_drones = []
                if self.base_pos == "pixel":
                    c_pos.append(drone.pos)
                    c_drones = drone.outside(self.drones, radius)
                    if c_drones != 0:
                        for c_drone in c_drones:
                            c_pos.append(c_drone.pos)
                    avr_pos = tuple(np.average(c_pos, axis=0))
                    if len(c_drones) != 0:  # check ada drone atau tidak
                        if self.exceptionId == 0 or self.exceptionId != drone.id:  # check ada pengecualian atau tidak
                            drone.set_target(avr_pos)

                elif self.base_pos == "real":

                    c_pos.append(drone.est_pos)
                    c_drones = drone.outside(self.drones, radius)
                    if len(c_drones) != 0:
                        check_far_drone.append(True)
                        for c_drone in c_drones:
                            c_pos.append(c_drone.est_pos)
                    else:
                        check_far_drone.append(False)
                    avr_pos = tuple(np.average(c_pos, axis=0))
                    if len(c_drones) != 0:  # check ada drone atau tidak
                        if self.exceptionId == 0 or self.exceptionId != drone.id:  # check ada pengecualian atau tidak
                            drone.est_set_target(avr_pos)
            else:
                self.drones.remove(drone)
            if any(far_drone is True for far_drone in check_far_drone):
                self.drone_far = True
            else:
                self.drone_far = False

    def alignment(self):
        self.all_angle = []
        for drone in self.drones:
            self.all_angle.append(drone.angle)
            if self.exceptionId == 0 or self.exceptionId != drone.id:  # check ada pengecualian atau tidak
                if abs(drone.angle - self.alignment_angle) < 10:
                    drone.angle = self.alignment_angle
        if len(self.all_angle) != 0:
            self.alignment_angle = sum(self.all_angle)/len(self.all_angle)

from random import randint
import pygame as py
import numpy as np
from CustARDrone import CustomArdrone
import csv
from math import fsum
from time import sleep, perf_counter


class Drone(py.sprite.Sprite):
    def __init__(self, id, pos, *groups):
        super().__init__(*groups)
        # A transparent image.
        self.image = py.Surface((50, 50), py.SRCALPHA)
        self.clock = py.time.Clock()
        # Draw a triangle onto the image.
        if id == 1:
            self.default_color = (30, 144, 255)
        elif id == 2:
            self.default_color = (119, 221, 119)
        elif id == 3:
            self.default_color = (177, 156, 217)
        else:
            self.default_color = (
                randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = self.default_color
        py.draw.polygon(self.image, py.Color(self.color),
                        ((0, 0), (50, 15), (0, 30)))

        # A reference to the original image to preserve the quality.
        self.id = id
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.vel = py.Vector2(0, 0)
        self.default_pos = pos
        self.pos = py.Vector2(self.default_pos)
        self.est_pos = py.Vector2((self.pos.x-105)*1.2, (self.pos.y-175)*1.2)
        # py.Vector2((self.pos.x/1.2)+105,
        #                           (self.pos.y/1.8)+175)
        self.set_point = py.Vector2(0, 0)
        self.input_signal = py.Vector2()
        self.speed_input = py.Vector2(0, 0)
        self.polar_error = py.Vector2(0, 0)
        self.error_pos = py.Vector2(0, 0)
        self.error_distance = 0
        self.default_nearby_rad = 0
        self.default_outside_rad = 0
        self.nearby_radius = self.default_nearby_rad
        self.outside_radius = self.default_outside_rad
        self.base_pos = "real"
        self.control_sys_type = "cartesius"
        self.error_type = 'polar'
        self.polar_limiter = True
        self.speed_limit = 0.2
        self.test_movement_state = False
        self.angle = 0
        self.rad_act = False
        self.path_act = False
        self.time = 0
        self.scale = 0.7
        self.dynamic_state = True
        self.flying_state = False
        self.relative_move = False
        self.another_dist = []
        self.default_values()
        self.battery = 100
        self.stopwth = Stopwatch()
        self.test_timer = Stopwatch()
        self.aruco_data = None
        self.test_random = 0
        self.carried_pos = None
        self.store_data = {"Time": [],
                           "Delta Time F": [],
                           "Delta Time B": [],
                           "Delta Time R": [],
                           "Delta Time L": [],
                           "Vx": [],
                           "Vy": [],
                           "Position x": [],
                           "Position y": [],
                           "Set Point x": [],
                           "Set Point y": [],
                           "ex": [],
                           "ey": [],
                           "Control Signal x": [],
                           "Control Signal y": [],
                           "Input vx": [],
                           "Input vy": [],
                           "Distance to target": [],
                           "Virtual Battery": [],
                           "Flying State": [],
                           }
        self.store_error = {"Time": [],
                            "Error Distance": []}
        self.store_path = {"Position x": [],
                           "Position y": [],
                           "Pos Hist": [],
                           "Init Pos": py.Vector2(self.pos.x, self.pos.y),
                           "Dist": 0}
        self.ar_drone_store_data = {"Second": [],
                                    "Battery": [],
                                    "Virtual Battery": [],
                                    "Yaw": [],
                                    "Pitch": [],
                                    "Roll": [],
                                    "Vx": [],
                                    "Vy": [],
                                    "Vz": [],
                                    "Altitude": [],
                                    "Flying State": [],
                                    "Vx+ Input": [],
                                    "Vx- Input": [],
                                    "Vy+ Input": [],
                                    "Vy- Input": [],
                                    "Vz+ Input": [],
                                    "Vz- Input": [],
                                    "Flying Input": [],
                                    "Cw Input": [],
                                    "Ccw Input": [],
                                    "Milisecond": [],
                                    "Position x": [],
                                    "Position y": [],
                                    "Control Signal x": [],
                                    "Control Signal y": [],
                                    "Set Point x": [],
                                    "Set Point y": [],
                                    "ex": [],
                                    "ey": [],
                                    "Error Dist": [],
                                    "Marker Pos": []
                                    }
        self.movement_input = {"forward": 0,
                               "backward": 0,
                               "right": 0,
                               "left": 0,
                               "up": 0,
                               "down": 0,
                               "cw": 0,
                               "ccw": 0,
                               "flying_input": False}

    def default_values(self):
        self.init_time = 0
        self.init_value_time = 0
        self.init_pos = 0
        self.init_time_fw = 0
        self.init_time_bw = 0
        self.init_time_rw = 0
        self.init_time_lw = 0
        self.init_value_fw = 0
        self.init_value_bw = 0
        self.init_value_rw = 0
        self.init_value_lw = 0
        self.delta_time = 0
        self.delta_time_fw = 0
        self.delta_time_bw = 0
        self.delta_time_rw = 0
        self.delta_time_lw = 0
        self.vx_plus = 0
        self.vx_neg = 0
        self.vy_plus = 0
        self.vy_neg = 0
        self.vx = 0
        self.vy = 0
        self.speed_measure = 0
        self.max_speed = 1
        self.default_foptd_fw()
        self.default_foptd_bw()
        self.default_foptd_rw()
        self.default_foptd_lw()
        self.default_set_movement()
        self.default_pid()
        self.init_ar_drone_data()

    def default_foptd_fw(self, k=4.618, tau=2.330, td=0.217, denom=1000):
        self.k_fw = k
        self.tau_fw = tau
        self.td_fw = td
        self.fw_time_denom = denom

    def default_foptd_bw(self, k=1.462, tau=0.245, td=0.281, denom=1000):
        self.k_bw = k
        self.tau_bw = tau
        self.td_bw = td
        self.bw_time_denom = denom

    def default_foptd_rw(self, k=2.656, tau=0.280, td=0.356, denom=1000):
        self.k_rw = k
        self.tau_rw = tau
        self.td_rw = td
        self.rw_time_denom = denom

    def default_foptd_lw(self, k=3.129, tau=1.986, td=0, denom=1000):
        self.k_lw = k
        self.tau_lw = tau
        self.td_lw = td
        self.lw_time_denom = denom

    def default_set_movement(self):
        self.forward = 0
        self.backward = 0
        self.right = 0
        self.left = 0

    def default_pid(self, forward_gain=[0], backward_gain=[0], right_gain=[0], left_gain=[0]):
        self.PID = PID(Kp=1, Td=1, control_type='p')
        # self.f_pd = PID(Kp=0.5581, Td=1, control_type='pd')
        # self.b_pd = PID(Kp=0.4186, Td=1, control_type='pd')
        # self.r_pd = PID(Kp=0.6981, Td=1, control_type='pd')
        # self.l_pd = PID(Kp=0.757, Td=1, control_type='pd')
        if len(forward_gain) == 1:
            self.f_pd = PID(Kp=0.371, Td=1.053, control_type='pd')
        else:
            self.f_pd = PID(
                Kp=forward_gain[0], Td=forward_gain[1], control_type='pd')

        if len(backward_gain) == 1:
            self.b_pd = PID(Kp=0.515, Td=0.794, control_type='pd')
        else:
            self.b_pd = PID(
                Kp=backward_gain[0], Td=backward_gain[1], control_type='pd')

        if len(right_gain) == 1:
            self.r_pd = PID(Kp=0.449, Td=0.286, control_type='pd')
        else:
            self.r_pd = PID(Kp=right_gain[0],
                            Td=right_gain[1], control_type='pd')

        if len(left_gain) == 1:
            self.l_pd = PID(Kp=1, Td=1, control_type='pd')
        else:
            self.l_pd = PID(Kp=left_gain[0],
                            Td=left_gain[1], control_type='pd')
        self.error = 0

        self.u = py.Vector2(0, 0)
        self.loop_type = "closed"
        self.loop_time = 0
        self.loop_time_init = 0
        self.loop_time_rec = True
        pass

    def init_ar_drone_data(self):
        self.ar_drone_connected = False
        self.ar_drone_vx = 0
        self.ar_drone_vy = 0
        self.ar_drone_battery = 0
        self.ar_drone_class = None
        self.ar_drone_flying_state = False
        pass

    def record_data(self):
        if self.ar_drone_connected is not True:
            self.simulation_record()
        else:
            self.ar_drone_record()
        if self.error_distance > 0:
            self.store_error['Time'].append(round(self.time/1000, 2))
            self.store_error['Error Distance'].append(
                round(self.error_distance, 1)**2)

    def simulation_record(self):
        self.store_data['Time'].append(round(self.time/1000, 3))
        self.store_data['Delta Time F'].append(self.delta_time_fw)
        self.store_data['Delta Time B'].append(self.delta_time_bw)
        self.store_data['Delta Time R'].append(self.delta_time_rw)
        self.store_data['Delta Time L'].append(self.delta_time_lw)
        self.store_data['Vx'].append(self.vx)
        self.store_data['Vy'].append(self.vy)
        self.store_data['Position x'].append(self.est_pos.x)
        self.store_data['Position y'].append(self.est_pos.y)
        self.store_data['Set Point x'].append(self.set_point.x)
        self.store_data['Set Point y'].append(self.set_point.y)
        self.store_data['ex'].append(self.error_pos.x)
        self.store_data['ey'].append(self.error_pos.y)
        self.store_data['Control Signal x'].append(self.u.x)
        self.store_data['Control Signal y'].append(self.u.y)
        self.store_data['Input vx'].append(self.speed_input.x)
        self.store_data['Input vy'].append(self.speed_input.y)
        self.store_data['Distance to target'].append(self.error_distance)
        self.store_data['Virtual Battery'].append(self.battery)
        self.store_data['Flying State'].append(
            self.flying_state)
        pass

    def ar_drone_record(self):
        self.ar_drone_store_data['Second'].append(round(self.time/1000, 3))
        self.ar_drone_store_data['Battery'].append(self.ar_drone_battery)
        self.ar_drone_store_data['Virtual Battery'].append(self.battery)
        self.ar_drone_store_data['Yaw'].append(self.ar_drone_class.yaw)
        self.ar_drone_store_data['Pitch'].append(self.ar_drone_class.pitch)
        self.ar_drone_store_data['Roll'].append(self.ar_drone_class.roll)
        self.ar_drone_store_data['Vx'].append(self.ar_drone_class.vx)
        self.ar_drone_store_data['Vy'].append(self.ar_drone_class.vy)
        self.ar_drone_store_data['Vz'].append(self.ar_drone_class.vz)
        self.ar_drone_store_data['Altitude'].append(
            self.ar_drone_class.altitude)
        self.ar_drone_store_data['Flying State'].append(
            self.ar_drone_class.flying_state)
        self.ar_drone_store_data['Vx+ Input'].append(
            self.movement_input['forward'])
        self.ar_drone_store_data['Vx- Input'].append(
            self.movement_input['backward'])
        self.ar_drone_store_data['Vy+ Input'].append(
            self.movement_input['right'])
        self.ar_drone_store_data['Vy- Input'].append(
            self.movement_input['left'])
        self.ar_drone_store_data['Vz+ Input'].append(self.movement_input['up'])
        self.ar_drone_store_data['Vz- Input'].append(
            self.movement_input['down'])
        self.ar_drone_store_data['Flying Input'].append(
            self.movement_input['flying_input'])
        self.ar_drone_store_data['Cw Input'].append(self.movement_input['cw'])
        self.ar_drone_store_data['Ccw Input'].append(
            self.movement_input['ccw'])
        self.ar_drone_store_data['Milisecond'].append(self.time)
        self.ar_drone_store_data['Position x'].append(self.est_pos.x)
        self.ar_drone_store_data['Position y'].append(self.est_pos.y)
        self.ar_drone_store_data['Control Signal x'].append(self.u.x)
        self.ar_drone_store_data['Control Signal y'].append(self.u.y)
        self.ar_drone_store_data['Set Point x'].append(self.set_point.x)
        self.ar_drone_store_data['Set Point y'].append(self.set_point.y)
        self.ar_drone_store_data['ex'].append(self.error_pos.x)
        self.ar_drone_store_data['ey'].append(self.error_pos.y)
        self.ar_drone_store_data['Error Dist'].append(self.error_distance)
        self.ar_drone_store_data['Marker Pos'].append(self.carried_pos)
        pass

    def update(self):
        self.rect.center = self.pos
        py.draw.polygon(self.orig_image, self.color,
                        ((0, 0), (50, 15), (0, 30)))
        self.image = py.transform.rotozoom(
            self.orig_image, -self.angle, 0.75*self.scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.nearby_radius = self.default_nearby_rad * self.scale
        # self.outside_radius = self.default_outside_rad * self.scale
        if self.flying_state:
            self.color = self.default_color
        else:
            self.color = (255, 0, 0)
        # if self.test_movement_state is not True:
        #     self.test_speed_force()

    def test_speed_force(self):
        if self.vx != 0:
            test_speed_x = self.vx
        else:
            test_speed_x = 0
        if self.vy != 0:
            test_speed_y = self.vy
        else:
            test_speed_y = 0

        self.pos += py.Vector2(test_speed_x, test_speed_y)/1.2
        self.est_pos += py.Vector2(test_speed_x, test_speed_y)

    def draw_radius(self, WIN):
        # self.circ_image = py.Surface((400, 300), py.SRCALPHA)
        # tes, _ = py.Vector2(1/1.2, 1/1.8).as_polar()
        # print(tes)
        if self.rad_act:
            py.draw.circle(WIN, (255, 0, 0), self.pos,
                           self.nearby_radius/1.2, 1)
            py.draw.circle(WIN, (0, 255, 0), self.pos,
                           self.outside_radius/1.2, 1)
        # self.orig_circ_image = self.circ_image
        # self.circ_rect = self.circ_image.get_rect(center=self.pos)

    def set_target(self, pos):
        self.set_point = py.Vector2(pos)
        error = self.set_point - self.pos
        r_er, _ = error.as_polar()
        if error.x != 0 or error.y != 0:
            # if abs(error_angle) > 5:
            #     if error_angle > 0:
            #         cw = 2
            #         ccw = 0
            #     elif error_angle < 0:
            #         ccw = 2
            #         cw = 0
            #     else:
            #         cw, ccw = 0, 0
            #     # self.move(cw=cw, ccw=ccw)
            # else:
            #     cw, ccw = 0, 0
            if r_er > 5:
                speed = (error).normalize()*self.max_speed
                # v_set_target.from_polar((speed, self.angle))
                if speed.x > 0:
                    self.forward = round(speed.x, 2)
                    self.backward = 0
                elif speed.x < 0:
                    self.backward = -1*round(speed.x, 2)
                    self.forward = 0
                if speed.y > 0:
                    self.right = round(speed.y, 2)
                    self.left = 0
                elif speed.y < 0:
                    self.left = -1*round(speed.y, 2)
                    self.right = 0
        self.move(self.forward, self.backward, self.right, self.left)
        if self.relative_move is not True:
            _, theta = self.vel.as_polar()
            self.angle = theta

    def est_set_target(self, pos):
        # timering = self.stopwth.delta_time
        # if self.stopwth.delta_time <= 2:
        #     self.stopwth.start()
        #     print(self.stopwth.delta_time)
        # else:
        #     print("resetting")
        #     self.stopwth.reset()
        self.stopwth.start()
        self.set_point = py.Vector2(pos)
        """Error calculation"""
        error = self.set_point - self.est_pos
        # if self.id == 1:
        #     if error.x != 0 or error.y != 0:
        #         if self.loop_time_rec is True:
        #             if self.loop_time_init == 0:
        #                 self.loop_time_init = self.time/1000
        #             else:
        #                 self.loop_time = self.time/1000 - self.loop_time_init
        #     if self.loop_time != 0 and int(error.x) == 0 and int(error.y) == 0:
        #         self.loop_time_rec = False

        # if error != 0 and self.loop_time_init != 0:
        #     self.loop_time = (self.time/1000)-self.loop_time_init

        """Distance error calculation with polar coordinate"""
        e_rad, _ = error.as_polar()

        """Initiate variable to record data"""
        self.error_pos = error
        self.error_distance = e_rad
        # print(self.error_distance)
        "controller input"
        if self.loop_type == "open":
            controller_input = self.set_point
        else:
            controller_input = self.error_pos
        """Initiate variable control output and speed"""
        vx_plus, vx_negatif, vy_plus, vy_negatif = 0, 0, 0, 0
        ux_plus, ux_negatif, uy_plus, uy_negatif = 0, 0, 0, 0

        """Controller"""
        if controller_input.x > 0:
            ux_plus = self.f_pd.run(round(controller_input.x, 3), self.time)
        elif controller_input.x < 0:
            ux_negatif = self.b_pd.run(round(controller_input.x, 3), self.time)
        else:
            ux_plus, ux_negatif = 0, 0
        if controller_input.y > 0:
            uy_plus = self.r_pd.run(round(controller_input.y, 3), self.time)
        elif controller_input.y < 0:
            uy_negatif = self.l_pd.run(round(controller_input.y, 3), self.time)
        else:
            uy_plus, uy_negatif = 0, 0
        self.u = py.Vector2(ux_plus+ux_negatif, uy_plus+uy_negatif)

        """Limiter for movement angle"""
        if self.polar_limiter == True:
            u_rad, u_angle = py.Vector2(
                ux_plus+ux_negatif, uy_plus+uy_negatif).as_polar()
            limit_rad = max(-3, min(3, u_rad))
            self.polar_error.from_polar((limit_rad, u_angle))
            self.speed_input = self.polar_error
        else:
            self.speed_input = py.Vector2(
                ux_plus+ux_negatif, uy_plus+uy_negatif)

        """Limiter for movement input"""
        if self.speed_input.x > 0:
            vx_plus = max(-self.speed_limit,
                          min(self.speed_limit, self.speed_input.x))
        elif self.speed_input.x < 0:
            vx_negatif = max(-self.speed_limit,
                             min(self.speed_limit, self.speed_input.x))
        if self.speed_input.y > 0:
            vy_plus = max(-self.speed_limit,
                          min(self.speed_limit, self.speed_input.y))
        elif self.speed_input.y < 0:
            vy_negatif = max(-self.speed_limit,
                             min(self.speed_limit, self.speed_input.y))

        """Input mechanism to drone"""
        self.forward = round(vx_plus, 3)
        self.backward = -1*round(vx_negatif, 3)
        self.right = round(vy_plus, 3)
        self.left = -1*round(vy_negatif, 3)
        # pause_time = self.stopwth.delta_time
        if self.error_distance > 30:
            self.move(self.forward, self.backward, self.right, self.left)
        else:
            self.move(0, 0, 0, 0)
        # if pause_time >= 500:
        #     self.stopwth.reset()
        # if pause_time >= 20:
        #     self.move(self.forward, self.backward, self.right, self.left)
        # else:
        #     self.move(0, 0, 0, 0)
        """Angle relative to speed angle"""
        # if self.relative_move is not True:
        #     _, theta = self.speed_input.as_polar()
        #     self.angle = theta

    def test_est_set_target(self, pos):
        self.set_point = py.Vector2(pos)
        error_pos = self.set_point - self.est_pos

        if self.control_sys_type == "polar":
            r_er, a_er = error_pos.as_polar()
            d_sp, a_sp = self.set_point.as_polar()
            # u_value = self.PID.run(r_er, self.time/1000)
            u_value = max(-1, min(1, r_er))
            open_loop_val = max(-1, min(1, d_sp))
            self.error = r_er
            if self.loop_type == "closed":
                self.input_signal.from_polar((self.u, a_er))
                self.u = u_value
            else:
                self.input_signal.from_polar((open_loop_val, a_sp))
                self.u = 0
        else:
            print(error_pos.x, error_pos.y, end='\r')
            vx = max(-1, min(1, error_pos.x))
            vy = max(-1, min(1, error_pos.y))
            self.input_signal = py.Vector2(vx, vy)
            pass
        # if error_pos.x != 0 or error_pos.y != 0:
            # if abs(error_angle) > 5:
            #     if error_angle > 0:
            #         cw = 2
            #         ccw = 0
            #     elif error_angle < 0:
            #         ccw = 2
            #         cw = 0
            #     else:
            #         cw, ccw = 0, 0
            #     # self.move(cw=cw, ccw=ccw)
            # else:
            #     cw, ccw = 0, 0
            # if r_er>5:
            # speed = (error_pos).normalize()*self.max_speed
        # v_set_target.from_polar((speed, self.angle))

        speed = self.input_signal
        if speed.x > 0:
            self.forward = round(speed.x, 2)
            self.backward = 0
        elif speed.x < 0:
            self.backward = -1*round(speed.x, 2)
            self.forward = 0
        if speed.y > 0:
            self.right = round(speed.y, 2)
            self.left = 0
        elif speed.y < 0:
            self.left = -1*round(speed.y, 2)
            self.right = 0
        self.move(self.forward, self.backward, self.right, self.left)
        # if self.relative_move is not True:
        #     _, theta = self.vel.as_polar()
        #     self.angle = theta

    def draw_target_line(self, screen):
        py.draw.line(screen, (255, 0, 0), self.pos,
                     self.pos + (self.polar_error*10), 5)
        pass

    def set_angle(self, angle):
        error_angle = angle-self.angle
        if abs(error_angle) > 5:
            if error_angle > 0:
                cw = 2
                ccw = 0
            elif error_angle < 0:
                ccw = 2
                cw = 0
            else:
                cw, ccw = 0, 0
            # self.move(cw=cw, ccw=ccw)
        else:
            cw, ccw = 0, 0
        self.move(cw=cw, ccw=ccw)

    def nearby(self, Drones, radius):
        nearby_drones = []
        if self.base_pos == "pixel":
            self.nearby_radius = radius*self.scale
            for drone in Drones:
                if self != drone:
                    relatif_pos = drone.pos-self.pos
                    rad, _ = relatif_pos.as_polar()
                    if rad - radius*self.scale < 0:
                        nearby_drones.append(drone)
        elif self.base_pos == "real":
            self.nearby_radius = radius
            for drone in Drones:
                if self != drone:
                    relatif_pos = drone.est_pos-self.est_pos
                    rad, _ = relatif_pos.as_polar()
                    if rad - radius < 0:
                        nearby_drones.append(drone)
        return nearby_drones

    def outside(self, Drones, radius):
        outside_drones = []
        if self.base_pos == "pixel":
            self.outside_radius = radius*self.scale
            for drone in Drones:
                if self != drone:
                    relatif_pos = drone.pos-self.pos
                    rad, _ = relatif_pos.as_polar()
                    if rad - radius*self.scale > 0:
                        outside_drones.append(drone)
        elif self.base_pos == "real":
            self.outside_radius = radius
            for drone in Drones:
                if self != drone:
                    relatif_pos = drone.est_pos-self.est_pos
                    rad, _ = relatif_pos.as_polar()
                    if rad - radius > 0:
                        outside_drones.append(drone)
        return outside_drones

    def distance_check(self, Drones):
        another_drone_dist = {}

        for drone in Drones:
            if drone != self:
                relatif_pos = drone.est_pos - self.est_pos
                dist, _ = relatif_pos.as_polar()
                if self.id < drone.id:
                    another_drone_dist.update(
                        {f'{self.id} to {drone.id}': dist})
                else:
                    another_drone_dist.update(
                        {f'{drone.id} to {self.id}': dist})
        return another_drone_dist

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
        if self.ar_drone_connected is not True:
            # self.test_timer.start()
            # print(self.test_timer.delta_time)
            """Movement simulation"""
            self.speed_input = py.Vector2(forward-backward, right-left)
            if self.flying_state == True:
                if self.dynamic_state:
                    """Forward movement"""
                    if forward > 0:
                        if self.init_value_fw < 1:
                            self.init_time_fw = self.time/self.fw_time_denom
                            self.init_value_fw += 1
                        self.delta_time_fw = self.time/self.fw_time_denom - self.init_time_fw
                        self.vx_plus = min(5, max(0, self.foptd(self.delta_time_fw, forward,
                                                                self.k_fw, self.tau_fw, self.td_fw)))
                    elif forward == 0 and self.init_value_fw > 0:
                        self.init_time_fw = 0
                        self.init_value_fw = 0
                        self.vx_plus = 0

                    """Backward movement"""
                    if backward > 0:
                        if self.init_value_bw < 1:
                            self.init_time_bw = self.time/self.bw_time_denom
                            self.init_value_bw += 1
                        self.delta_time_bw = self.time/self.bw_time_denom - self.init_time_bw
                        self.vx_neg = min(0, self.foptd(self.delta_time_bw, (-1*backward),
                                                        self.k_bw, self.tau_bw, self.td_bw))
                    elif backward == 0 and self.init_value_bw > 0:
                        self.init_time_bw = 0
                        self.init_value_bw = 0
                        self.vx_neg = 0

                    """Right movement"""
                    if right > 0:
                        if self.init_value_rw < 1:
                            self.init_time_rw = self.time/self.rw_time_denom
                            self.init_value_rw += 1
                        self.delta_time_rw = self.time/self.rw_time_denom - self.init_time_rw
                        self.vy_plus = max(0, self.foptd(self.delta_time_rw, right,
                                                         self.k_rw, self.tau_rw, self.td_rw))
                    elif right == 0 and self.init_value_rw > 0:
                        self.init_time_rw = 0
                        self.init_value_rw = 0
                        self.vy_plus = 0
                    """Left movement"""
                    if left > 0:
                        if self.init_value_lw < 1:
                            self.init_time_lw = self.time/self.lw_time_denom
                            self.init_value_lw += 1
                        self.delta_time_lw = self.time/self.lw_time_denom - self.init_time_lw
                        self.vy_neg = min(0, self.foptd(self.delta_time_lw, (-1*left),
                                                        self.k_lw, self.tau_lw, self.td_lw))
                    elif left == 0 and self.init_value_lw > 0:
                        self.init_time_lw = 0
                        self.init_value_lw = 0
                        self.vy_neg = 0

                    if forward == 0 and backward == 0:
                        self.vx = 0
                    if right == 0 and left == 0:
                        self.vy = 0
                    self.vx = self.vx_plus + self.vx_neg
                    self.vy = self.vy_plus + self.vy_neg
                    if cw != 0:
                        if self.angle <= 180:
                            self.angle += cw
                        else:
                            self.angle = -180
                            self.angle += cw
                    if ccw != 0:
                        if self.angle >= -180:
                            self.angle -= ccw
                        else:
                            self.angle = 180
                            self.angle -= ccw

                else:
                    self.vx = forward + (-1*backward)
                    self.vy = right + (-1*left)
                    self.angle += cw
                    self.angle -= ccw

                if self.vx != 0 or self.vy != 0:
                    if self.init_value_time == 0:
                        self.init_time = py.time.get_ticks()
                        self.init_pos = py.Vector2(self.pos.x, self.pos.y)
                        self.init_value_time += 1
                    if self.relative_move == True:
                        v_dist, v_rot = py.Vector2(self.vx, self.vy).as_polar()
                        self.vel.from_polar((v_dist, self.angle+v_rot))
                    else:
                        self.vel = py.Vector2(self.vx, self.vy)*100
                    self.delta_time = (self.time - self.init_time)/1000
                    self.vel_pix = py.Vector2(self.vel.x, self.vel.y)/1.2
                    # if self.fps > 0:
                    #     self.pix_pos += ((self.vel/0.85)/self.fps)
                    # print(self.vel*(self.delta_time_fw/1000))
                    # self.pos += self.vel

                    # if self.fps > 0:
                    #     self.pos += self.vel_pix/self.fps
                    #     self.est_pos += self.vel/self.fps

                    if self.flying_state == True:
                        self.test_timer.start()
                        waktu = self.test_timer.delta_time
                        self.pos += self.vel_pix * waktu
                        self.est_pos += self.vel * waktu
                        if waktu > 0:
                            self.test_timer.reset()
                        self.test_timer.start()

                else:
                    if self.init_value_time > 0:
                        self.init_time = 0
                        self.init_pos = 0
                        self.init_value_time = 0
        else:

            self.ar_drone_class.move(forward=forward,
                                     backward=backward,
                                     right=right,
                                     left=left,
                                     up=up,
                                     down=down,
                                     cw=cw,
                                     ccw=ccw)
            self.movement_input['forward'] = forward
            self.movement_input['backward'] = backward*(-1)
            self.movement_input['right'] = right
            self.movement_input['left'] = left*(-1)
            self.movement_input['up'] = up
            self.movement_input['down'] = down
            self.movement_input['cw'] = cw
            self.movement_input['ccw'] = ccw

            pass
            # else:
            #     self.vel = py.Vector2(0, 0)

    def get_state(self):
        if len(self.store_error['Error Distance']) > 0:
            rmse = (fsum(self.store_error['Error Distance']) /
                    len(self.store_error['Error Distance']))**0.5
            elapsed_time = self.store_error['Time'][0] - \
                self.store_error['Time'][-1]
        else:
            rmse = 0
            elapsed_time = 0
        state = {'Drone': self.id,
                 'Flying State': self.flying_state,
                 'Position': np.round(self.pos, 1),
                 'Velocity': np.round(self.vel, 1),
                 'Battery ': self.battery,
                 'Set Point': np.round(self.set_point, 1),
                 }
        state.update({
            'Vx':  round(self.vx, 2),
            'Vy':  round(self.vy, 2),
            'V Input': np.round(self.speed_input, 2),
            'Est Pos': tuple(np.round(self.est_pos)),
            'Error Distance': self.error_distance,
            'RMSE': rmse,
            'RMSE Time': elapsed_time

        }
        )
        return state

    def setNavdata(self, fps, drones):
        # self.time = py.time.get_ticks()
        self.time = perf_counter()*1000
        self.fps = fps
        self.distance_check(drones)

    def synchronize_position(self, pos_sys):
        if self.aruco_data is not None:
            for point in pos_sys.all_rect:
                if self.aruco_data['Detector Active'] == True:
                    if self.aruco_data['Detected Id'] != "None":
                        if point.id == self.aruco_data['Detected Id']:
                            self.carried_pos = point.carried_pos
                            dif_pos = self.est_pos - self.carried_pos
                            dist_car, _ = dif_pos.as_polar()
                            if dist_car > 30:
                                self.est_pos = point.carried_pos
                                self.pos = point.pos+pos_sys.pos
                    else:
                        self.carried_pos = None
        pass

    def foptd(self, t, input, K=1.0, tau=1.0, tau_d=0.0):
        tau_d = max(0, tau_d)
        tau = max(0, tau)
        if (t - tau_d) >= 0:
            output = K*input*(1-np.exp((-1)*(t-tau_d)/tau))
        else:
            output = 0
        return output

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def is_health(self):
        if self.battery > 30:
            health_state = True
        else:
            health_state = False
        return health_state

    def reset_record_data(self):
        if self.ar_drone_connected is not True:
            self.store_data = {"Time": [],
                               "Delta Time F": [],
                               "Delta Time B": [],
                               "Delta Time R": [],
                               "Delta Time L": [],
                               "Vx": [],
                               "Vy": [],
                               "Position x": [],
                               "Position y": [],
                               "Set Point x": [],
                               "Set Point y": [],
                               "ex": [],
                               "ey": [],
                               "Control Signal x": [],
                               "Control Signal y": [],
                               "Input vx": [],
                               "Input vy": [],
                               "Distance to target": []}
            self.loop_time = 0.0
            self.loop_time_init = 0.0
            self.loop_time_rec = True
            self.pos = py.Vector2(self.default_pos)
            self.est_pos = py.Vector2(
                (self.pos.x-105)*1.2, (self.pos.y-175)*1.2)
        else:
            self.ar_drone_store_data = {"Second": [],
                                        "Battery": [],
                                        "Yaw": [],
                                        "Pitch": [],
                                        "Roll": [],
                                        "Vx": [],
                                        "Vy": [],
                                        "Vz": [],
                                        "Altitude": [],
                                        "Flying State": [],
                                        "Vx+ Input": [],
                                        "Vx- Input": [],
                                        "Vy+ Input": [],
                                        "Vy- Input": [],
                                        "Vz+ Input": [],
                                        "Vz- Input": [],
                                        "Flying Input": [],
                                        "Cw Input": [],
                                        "Ccw Input": [],
                                        "Milisecond": []
                                        }
            self.movement_input = {"forward": 0,
                                   "backward": 0,
                                   "right": 0,
                                   "left": 0,
                                   "up": 0,
                                   "down": 0,
                                   "cw": 0,
                                   "ccw": 0,
                                   "flying_input": False}

    def draw_path(self, surface):
        pt = round(self.pos.x), round(self.pos.y)
        if len(self.store_path['Pos Hist']) != 0:
            if pt != self.store_path['Pos Hist'][-1]:
                self.store_path['Pos Hist'].append(pt)
        else:
            self.store_path['Pos Hist'].append(pt)
        if self.path_act:
            for pos in self.store_path['Pos Hist']:
                py.draw.circle(surface, self.default_color, pos, 2)
        pass

    def reset_path(self):
        self.store_path['Pos Hist'] = []

    def takeoff(self):
        self.movement_input['flying_input'] = True
        if self.ar_drone_connected is not True:
            self.flying_state = True
        else:
            self.ar_drone_class.takeoff()
            self.flying_state = self.ar_drone_flying_state

    def land(self):
        self.movement_input['flying_input'] = False
        if self.ar_drone_connected is not True:
            self.flying_state = False
        else:
            self.ar_drone_class.land()
            self.flying_state = self.ar_drone_flying_state

    def ar_drone_sync(self, ar_drone_data):
        """Data synchronize"""
        if self.ar_drone_class is None:
            """Class initiate"""
            if isinstance(ar_drone_data, CustomArdrone):
                self.ar_drone_class = ar_drone_data
            else:
                self.ar_drone_class = None
        else:
            if self.aruco_data is None:
                self.aruco_data = self.ar_drone_class.aruco_data
            if self.ar_drone_class.navdemo is not None:
                self.ar_drone_connected = True
                self.ar_drone_vx = self.ar_drone_class.vx if self.ar_drone_class.vx is not None else 0
                self.ar_drone_vy = self.ar_drone_class.vy if self.ar_drone_class.vy is not None else 0
                self.ar_drone_flying_state = self.ar_drone_class.flying_state
                self.flying_state = self.ar_drone_flying_state
                self.ar_drone_battery = self.ar_drone_class.battery
                self.vel = py.Vector2(
                    self.ar_drone_vx*100, self.ar_drone_vy*100)
                self.vel_pix = py.Vector2(self.vel.x, self.vel.y)/1.2
                # if self.fps > 0:
                #     if self.flying_state == True:
                #         self.pos += self.vel_pix/self.fps
                #         self.est_pos += self.vel/self.fps
                if self.flying_state == True:
                    self.test_timer.start()
                    waktu = self.test_timer.delta_time
                    self.pos += self.vel_pix * waktu
                    self.est_pos += self.vel * waktu
                    if waktu > 0:
                        self.test_timer.reset()
                    self.test_timer.start()
            else:
                self.ar_drone_connected = False

        pass

    def printcsv(self):
        f = open(f'drone {self.id} data.csv', "w", newline='')
        if self.ar_drone_connected is not True:
            with f as outfile:
                writerfile = csv.writer(outfile, delimiter=",")
                writerfile.writerow(self.store_data.keys())
                writerfile.writerows(zip(*self.store_data.values()))
        else:
            with f as outfile:
                writerfile = csv.writer(outfile, delimiter=",")
                writerfile.writerow(self.ar_drone_store_data.keys())
                writerfile.writerows(zip(*self.ar_drone_store_data.values()))
        f.close()

    def test_stopwatch(self):
        self.stopwth.start()
        print(self.stopwth.delta_time)

    def test_reset_stopwatch(self):
        self.stopwth.reset()


class PID:
    def __init__(self, Kp=1.0, Ti=1.0, Td=0.0, t_init=0.0, control_type='pid'):
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
        self.t_init = t_init
        self.control_type = control_type
        self.e_prev = 0
        self.t_prev = 0
        self.u = 0
        self.I = 0
        pass

    def run(self, error, t):
        self.e = error
        self.t = t
        self.de = self.e - self.e_prev
        self.dt = self.t - self.t_prev
        # self.dt = 30

        self.P = self.Kp*self.e
        self.I = self.I + (self.e*self.dt)
        if self.de != 0 and self.dt != 0:
            self.D = self.de/self.dt
        else:
            self.D = 0

        if self.control_type == 'p':
            self.u = self.P
        elif self.control_type == 'pi':
            self.u = (self.Kp*(self.e+(1/self.Ti)*self.I))
        elif self.control_type == 'pd':
            self.u = (self.Kp*(self.e + (self.Td*self.D)))
        else:
            self.u = (self.Kp*(self.e + (1/self.Ti)*self.I+self.Td*self.D))
        self.e_prev = self.e
        self.t_prev = self.t
        return self.u


class Stopwatch:
    def __init__(self):
        self.init_time = 0
        self.current_time = 0
        self.delta_time = 0
        self.starting = True

    def start(self):

        if self.init_time == 0:
            self.init_time = perf_counter()
        self.current_time = perf_counter()
        self.delta_time = round((self.current_time - self.init_time), 5)

    def stop(self):
        self.starting = False
        pass

    def reset(self):
        self.init_time = 0
        self.current_time = 0
        self.delta_time = 0
        pass

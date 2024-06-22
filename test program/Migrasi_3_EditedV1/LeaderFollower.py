import pygame as py
import time as tm
import csv


class LeaderFollower:
    def __init__(self, Drones, leader_id, trajectory):
        self.drones = Drones
        self.all_drones_data = Drones
        self.leader_id = leader_id
        self.leader_drone = None
        self.trajectory = trajectory
        self.limit_dist = 200
        self.limit_far = 400
        self.time = 0
        self.time_init = None
        self.time_rec = False
        self.follower_drone = []
        self.follower_distance = []
        self.dist_between_foll = 0
        self.cyclic_active = False
        self.lf_data = {"Leader Id": self.leader_id,
                        "Foll Id": [],
                        "Foll Dist": 0,
                        " ": 0,
                        "Foll Angle": [],
                        "Next Target": py.Vector2(0, 0),
                        "Track Dist": " "
                        }
        self.lf_store_data = {"Time": [],
                              "Leader id": [],
                              "Leader pos x": [],
                              "Leader pos y": [],
                              "Trajectory point x": [],
                              "Trajectory point y": [],
                              "L dist to foll 1": [],
                              "L dist to foll 2": [],
                              "Between followers": [],
                              "Limit distance": []
                              }

        for drone in self.drones:
            if drone.id == self.leader_id:
                self.leader_drone = drone
            else:
                self.follower_drone.append(drone)
            self.lf_store_data[f'Drone {drone.id} battery'] = []
        for drone in self.follower_drone:
            self.lf_store_data[f'Follower {drone.id-1} pos x'] = []
            self.lf_store_data[f'Follower {drone.id-1} pos y'] = []
            rad, theta = (drone.est_pos - self.leader_drone.est_pos).as_polar()
            self.follower_distance.append(round(rad, 2))
            radf, _ = (self.follower_drone[0].est_pos -
                       self.follower_drone[1].est_pos).as_polar()
            self.dist_between_foll = radf

    def run(self):
        # print(self.cyclic_condition)
        self.leader()
        self.follower()
        self.calculate_times()
        # if self.cyclic_active is not True:
        #     self.error_check()
        # print(self.follower_distance)
        # if len(self.follower_drone) != 0:
        if all(self.limit_dist <= i <= self.limit_far for i in self.follower_distance):
            # print("in range")
            self.trajectory.run(self.time)
            for drone, pos in zip(self.follower_drone, self.follower_set_point):
                # if self.cyclic_condition is not True:
                drone.est_set_target(pos)
        elif any(i < self.limit_dist for i in self.follower_distance):
            # print("near range")
            self.trajectory.run(self.time)
        else:
            for drone, pos in zip(self.follower_drone, self.follower_set_point):
                # if self.cyclic_condition is not True:
                drone.est_set_target(pos)
        # else:
        #     print("ini jalan")
        #     self.trajectory.run(self.time)

        # if len(self.trajectory.track_points) == len(self.trajectory.store_track):
        #     self.leader_drone.land()
        #     for drone in self.follower_drone:
        #         drone.land()
        # if self.leader_drone.flying_state is not True:
        #     for drone in self.follower_drone:
        #         if drone.flying_state is True:
        #             drone.land()

    def calculate_times(self):
        time = tm.perf_counter()/1000
        if self.time_init is None:
            self.time_init = time
        else:
            self.time = time - self.time_init
        pass

    def leader(self):
        self.track_dist = []
        """Set leader"""
        if self.trajectory.drone != self.leader_drone:
            self.trajectory.drone = self.leader_drone
        """Record data"""
        for track in self.trajectory.track_points:
            self.lf_data[f'{self.trajectory.track_points.index(track)}'] = track
        self.lf_data['Next Target'], _ = (
            self.trajectory.current_target - self.leader_drone.est_pos).as_polar()
        pass

    def follower(self):
        self.follower_id = []
        self.follower_distance = []
        self.follower_angle = []
        self.follower_set_point = []

        """define follower (relative to leader)"""
        for drone in self.follower_drone:
            self.follower_id.append(drone.id)
            rad, theta = (drone.est_pos - self.leader_drone.est_pos).as_polar()
            self.follower_distance.append(round(rad, 2))
            self.follower_angle.append(round(theta, 2))
        self.lf_data['Foll Id'] = self.follower_id

        """Set position for follower if dist < limit"""
        if len(self.follower_drone) == 2:
            for i in range(len(self.follower_drone)):
                set_point = py.Vector2()
                set_point.from_polar((
                    self.limit_dist, -135*(1 if i == 0 else -1)))
                self.follower_set_point.append(
                    set_point+self.leader_drone.est_pos)
        else:
            set_point = py.Vector2()
            set_point.from_polar((
                self.limit_dist, 180))
            self.follower_set_point.append(set_point+self.leader_drone.est_pos)

        """Follower display data"""
        if len(self.follower_drone) == 2:
            self.lf_data['Foll Dist'] = self.follower_distance[0]
            self.lf_data[' '] = self.follower_distance[1]
            radf, _ = (self.follower_drone[0].est_pos -
                       self.follower_drone[1].est_pos).as_polar()
            self.dist_between_foll = radf
        elif len(self.follower_drone) == 1:
            self.lf_data['Foll Dist'] = self.follower_distance[0]
        else:
            self.lf_data['Foll Dist'] = None
        self.lf_data['Foll Angle'] = self.follower_angle
        self.lf_data['Foll SP X'] = self.follower_set_point
        pass

    def error_check(self):
        for drone in self.drones:
            if drone.is_health() is not True:
                if drone in self.follower_drone:
                    drone.land()
                    self.follower_drone.remove(drone)
                if drone == self.leader_drone:
                    if len(self.follower_drone) != 0:
                        if drone in self.follower_drone:
                            drone.land()
                            self.follower_drone.remove(drone)

    def cyclic(self):
        self.health_drones = []
        if self.cyclic_active is not True:
            self.cyclic_active = True
        for drone in self.drones:
            if drone.is_health() == True:
                self.health_drones.append(drone)
                if drone.id == self.leader_id:
                    if drone in self.follower_drone:
                        if len(self.follower_drone) != 0:
                            self.follower_drone.remove(drone)
        if any(drone.is_health() != True for drone in self.drones):
            # print("drone problem")

            self.cyclic_condition = True
            for drone in self.drones:
                if drone.is_health() != True:
                    drone.land()
                    if drone.id == self.leader_id:
                        self.leader_drone = self.health_drones[0]
                        self.leader_id = self.health_drones[0].id
                    else:
                        if drone in self.follower_drone and len(self.follower_drone) != 0:
                            self.follower_drone.remove(drone)
                    self.lf_data['Leader Id'] = self.leader_id
            self.drones = self.health_drones
            # else:
            #     if drone.id == self.leader_id:
            #         if drone in self.follower_drone:
            #             if len(self.follower_drone) != 0:
            #                 self.follower_drone.remove(drone)
            # print(len(self.health_drones))
        else:

            self.cyclic_condition = False
            # print("all drones are health")
        return self.cyclic_condition

    def record(self):
        if self.leader_drone is not None:
            self.lf_store_data['Time'].append(self.time)
            self.lf_store_data['Leader id'].append(self.leader_id)
            self.lf_store_data['Leader pos x'].append(
                self.leader_drone.est_pos.x)
            self.lf_store_data['Leader pos y'].append(
                self.leader_drone.est_pos.y)
            self.lf_store_data['Trajectory point x'].append(
                self.trajectory.current_target.x)
            self.lf_store_data['Trajectory point y'].append(
                self.trajectory.current_target.y)
            for drone in self.all_drones_data:
                self.lf_store_data[f'Drone {drone.id} battery'].append(
                    drone.battery)
        if len(self.follower_drone) > 1:
            for drone in self.follower_drone:
                self.lf_store_data[f'Follower {drone.id-1} pos x'].append(
                    drone.est_pos.x)
                self.lf_store_data[f'Follower {drone.id-1} pos y'].append(
                    drone.est_pos.y)
            self.lf_store_data['L dist to foll 1'].append(
                self.follower_distance[0])
            self.lf_store_data['L dist to foll 2'].append(
                self.follower_distance[1])
            self.lf_store_data['Between followers'].append(
                self.dist_between_foll)
            self.lf_store_data['Limit distance'].append(self.limit_dist)
        elif len(self.follower_drone) == 1:
            for drone in self.follower_drone:
                self.lf_store_data[f'Follower {drone.id-2} pos x'].append(
                    drone.est_pos.x)
                self.lf_store_data[f'Follower {drone.id-2} pos y'].append(
                    drone.est_pos.y)
                self.lf_store_data[f'Follower {drone.id-1} pos x'].append(0)
                self.lf_store_data[f'Follower {drone.id-1} pos y'].append(0)
            self.lf_store_data['L dist to foll 1'].append(
                self.follower_distance[0])
            self.lf_store_data['L dist to foll 2'].append(0)
            self.lf_store_data['Between followers'].append(0)
            self.lf_store_data['Limit distance'].append(self.limit_dist)
        else:
            self.lf_store_data[f'Follower {2} pos x'].append(0)
            self.lf_store_data[f'Follower {2} pos y'].append(0)
            self.lf_store_data[f'Follower {1} pos x'].append(0)
            self.lf_store_data[f'Follower {1} pos y'].append(0)
            self.lf_store_data['L dist to foll 1'].append(0)
            self.lf_store_data['L dist to foll 2'].append(0)
            self.lf_store_data['Between followers'].append(0)
            self.lf_store_data['Limit distance'].append(self.limit_dist)

    def printcsv(self):
        f = open(f'LF Data.csv', "w", newline='')

        with f as outfile:
            writerfile = csv.writer(outfile, delimiter=",")
            writerfile.writerow(self.lf_store_data.keys())
            writerfile.writerows(zip(*self.lf_store_data.values()))

        f.close()

triggering = {"main_trigger": False,
              "preparing": False,
              "plotgraph": False,
              "config_display": True,
              "config_page_value": 0,
              "aruco_display": False,
              "mode_screen": 1,
              "reset_trajectory": False,
              "individu_plot": False,
              "individu_type_plot": None,
              "plot_all_data": False,
              "ardrone_connect": False,
              "lf_plot_data": False,
              "keyboard_ctrl": True,
              "write_csv": False,
              "Acquisition": False}
screen_active = {"SCREEN CONFIG": " ", }
set_value = {"Set Speed": 0.2}
configuration = {"Common Config": " ",
                 "Boid Start": False,
                 "Trajectory Start": False,
                 "Draw Radius": False,
                 "Mouse Follow": False,
                 "Moving Drone": False,
                 "Choosen Drone Id": 0,
                 "Record Data": False,
                 "FPS": 0,
                 "Set Speed": round(set_value['Set Speed'], 1),
                 "Relative Move": False,
                 "Boid has run": False,
                 "Algorithm start": False,
                 "Record LF": False
                 }
trajectory_data = {"Traject Config": " ", "ID Drone": 1,
                   "Total Track Point": 0, "Track Point Passed": 0,
                   "Draw Point": False, "Draw Line": False, "Draw Path": False}
boid_data = {"Boid Config": " ",
             "Separation Radius": 100, "Cohesion Radius": 300}
aruco_data = {"ArUco Data": " ",
              "Camera Active": False,
              "Detector Active": False,
              "Drone Camera": 0,
              "Total Id": 0,
              "Detected Id": " "}
pos_sys_data = {"Draw Coord.": False,
                "Sync Coord.": False,
                "Pos Rect": False}
ar_drone_data = {"AR Drone Data": " ",
                 "Connected": False,
                 "Battery": 0,
                 "Flying State": False,
                 "Vx": 0,
                 "Vy": 0,
                 "Altitude": 0,
                 "Takeoff": False,
                 "Landing": False,
                 "Change camera": False,
                 "Trim": False,
                 "Calibration": False
                 }
ar_drone_movement = {"forward": 0,
                     "backward": 0,
                     "right": 0,
                     "left": 0,
                     "cw": 0,
                     "ccw": 0,
                     "up": 0,
                     "down": 0}
configuration_display = []
storing = {"init_track_time": 0, "Drone 1": []}
surface_data = {"Left Scroll": 0,
                "Main Screen": None,
                "Bottom Screen": []}
lf_data = {"LF Data": " ",
           "Run": False}
movement = {"forward": 0,
            "backward": 0,
            "right": 0,
            "left": 0,
            "cw": 0,
            "ccw": 0,
            "up": 0,
            "down": 0}
distance_data = {}
general_data = {"Drones": [],
                "AR Drones": [],
                "All Markers": []}

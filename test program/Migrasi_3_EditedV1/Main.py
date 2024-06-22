import pygame as py
import sys
import win32gui
import win32con
import threading
from Aruco import ArucoMarker
from GUI import *
from buttons_lib import set_up_buttons
from Drone import Drone
from Trajectory import Trajectory
from Boid import Boid
from LeaderFollower import LeaderFollower
from Position import PositionSystem
from dict_library import *
from PlotData import plot_drone_data, plotting_all, signal_plot, lf_plot
from CustARDrone import CustomArdrone

# 'Aruco.py'
# 'GUI.py'
# 'buttons_lib.py'
# 'Drone.py'
# 'Trajectory.py'
# 'Boid.py'
# 'LeaderFollower.py'
# 'Position.py'
# 'dict_library.py'
# 'PlotData.py'
# 'CustARDrone.py'

WIDTH, HEIGHT = 1000, 700
flags = py.DOUBLEBUF | py.RESIZABLE
FPS = 60
WHITE = (255, 255, 255)
storingData_event = py.USEREVENT + 0

# ---------------------------------------------------------------------------- #
#                                SET UP FUNCTION                               #
# ---------------------------------------------------------------------------- #


def set_up_drones(total_drones):
    """set all drones with numbers of drones"""
    drones = []
    for i in range(1, total_drones+1):
        if i == 1:
            drone = Drone(i, (105, 175))
        else:
            drone = Drone(i, (105, 175+(75*i)))
        # drone.set_target(drone.pos)
        drones.append(drone)

    drone_group = py.sprite.Group()
    drone_group.add(drones)
    for drone in drones:
        """Parameter Rafifandi drone A"""
        drone.default_foptd_fw(k=2.674, tau=1.039, td=0.387)
        drone.default_foptd_bw(k=2.257, tau=0.79, td=0.332)
        drone.default_foptd_rw(k=1.875, tau=0.333, td=0.388)
        drone.default_foptd_lw(k=1.937, tau=0.859, td=0)
        """Parameter Rafifandi drone B"""
        # drone.default_foptd_fw(k=1.358, tau=1.358, td=0.708)
        # drone.default_foptd_bw(k=2.121, tau=0.776, td=0.583)
        # drone.default_foptd_rw(k=0.832, tau=0.493, td=0.671)
        # drone.default_foptd_lw(k=1.446, tau=3.390, td=0.784)

        """PID"""
        if isinstance(drone, Drone):
            if drone.id == 1:
                # drone A
                f_1 = [0.0007, 0.0037]
                b_1 = [0.0005, 0.0040]
                r_1 = [0.0008, 0.0017]
                l_1 = [0.0005, 0.0055]
                drone.default_pid(f_1, b_1, r_1, l_1)

            if drone.id == 2:
                # drone B
                f_3 = [0.0005, 0.0016]
                b_3 = [0.0007, 0.0025]
                r_3 = [0.0005, 0.0057]
                l_3 = [0.0005, 0.0056]
                drone.default_pid(f_3, b_3, r_3, l_3)

            if drone.id == 3:
                # drone C
                f_2 = [0.0009, 0.0260]
                b_2 = [0.0017, 0.0130]
                r_2 = [0.0006, 0.0040]
                l_2 = [0.0009, 0.0046]
                drone.default_pid(f_2, b_2, r_2, l_2)

        pass
    for drone in drones:
        general_data['Drones'].append(drone)
    drones_source = (drones, drone_group)
    return drones_source


def set_up_screen():
    main_s = MainScreen("main_s", "Main Screen")
    state_s = LeftSideScreen("state_s", "Status")
    config_s = RightSideScreen("config_s", "Configuration")
    control_s = BottomScreen("control_s", "Main Control")
    manual_s = BottomScreen("manual_s", "Manual Control", active=False)
    ardrone_s = BottomScreen("ardrone_s", "AR Drone Control", active=False)
    boid_conf_s = BottomScreen(
        "boid_conf_s", "Boid Configuration", active=False)
    lf_s = BottomScreen("lf_s", "Leader Follower Configuration", active=False)
    aruco_conf_s = BottomScreen(
        "aruco_conf_s", "ArUco Marker Configuration", active=False)
    traject_s = BottomScreen(
        "traject_s", "Trajectory Configuration", active=False)
    pos_s = BottomScreen(
        "pos_s", "Positon System Configuration", active=False)
    plots_s = PlotScreen(
        "plots_s", "Plotting Screen", active=False)
    aruco_main_s = ArucoScreen(
        "aruco_main_s", "ArUco Main Screen", active=False)

    all_screen = [main_s,
                  state_s,
                  config_s,
                  control_s,
                  manual_s,
                  ardrone_s,
                  boid_conf_s,
                  plots_s,
                  lf_s,
                  aruco_conf_s,
                  traject_s,
                  aruco_main_s,
                  pos_s]
    all_screen_id = []
    all_screen_active = []
    for screen in all_screen:
        all_screen_id.append(screen.id)
        all_screen_active.append(screen.active)
        if isinstance(screen, BottomScreen):
            surface_data['Bottom Screen'].append(screen)
        if screen.id == 'main_s':
            surface_data['Main Screen'] = screen
    for x in range(len(all_screen_id)):
        screen_active[all_screen_id[x]] = all_screen_active[x]
    # configuration_display.append(configuration)
    # configuration_display.append(aruco_data)
    return all_screen


def set_up_trajectory(drone):
    forward_x = [(300, 160), (400, 160), (500, 160), (600, 160), (700, 160)]
    forward_x_lf = [(400, 135),
                    (600, 135), (800, 135)]
    backward_x = [(500, 90), (400, 90), (250, 90), (120, 90), (60, 90)]
    # forward_x = [(0, 90), (20, 90), (30, 90), (40, 90), (50, 90),(60, 90),(70, 90),(80, 90),(90, 90),(100, 90),(110, 90), (120, 90), (130, 90), (140, 90), (150, 90),(160, 90),(170, 90),(180, 90),(190, 90),(200, 90)]
    rightward_y = [(120, 90), (120, 120), (120, 160), (120, 250)]
    leftward_y = [(120, 160), (120, 120), (120, 90)]
    diagonal = [(120, 90), (240, 180), (360, 270)]
    rev_diagonal = [(300, 210), (180, 120), (60, 60)]
    s_letter = [(180, 270), (360, 270),
                (360, 90), (540, 90), (540, 270)]
    s_letter_lf = [(240, 270), (540, 270),
                   (540, 135), (840, 135), (840, 270)]
    # one_point = [(210, 90), (210, 180)]
    one_point = [(210, 90)]
    set_trajectory = Trajectory(
        drone, forward_x)
    configuration_display.append(trajectory_data)
    configuration_display.append(boid_data)
    return set_trajectory


def set_up_ardrones():
    ardrone_a = CustomArdrone(1, '192.168.1.11')
    ardrone_b = CustomArdrone(2, '192.168.1.12')
    ardrone_c = CustomArdrone(3, '192.168.1.13')
    ardrones = [ardrone_a, ardrone_b, ardrone_c]
    for drone in ardrones:
        general_data['AR Drones'].append(drone)
    configuration_display.append(configuration)
    configuration_display.append(ar_drone_data)
    # ardrones = []
    return ardrones
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                ACTION FUNCTION                               #
# ---------------------------------------------------------------------------- #


def action(drones, set_trajectory, all_buttons, all_screen):
    main_buttons, manual_buttons, menu_buttons = all_buttons[:3]
    ardrone_buttons = all_buttons[6]
    aruco_buttons = all_buttons[10]
    trajectory_buttons = all_buttons[12]
    pos_sys_buttons = all_buttons[14]
    lf_buttons = all_buttons[16]
    screen_id = None
    for screen in all_screen:
        if screen.active:
            if isinstance(screen, BottomScreen):
                if screen.id == 'control_s':
                    mainControl_action(screen, main_buttons, drones)
                if screen.id == 'manual_s':
                    manualControl_action(drones, screen, manual_buttons)
                if screen.id == 'ardrone_s':
                    ardroneControl_action(screen, ardrone_buttons)
                if screen.id == 'aruco_conf_s':
                    arucoConfig_action(screen, aruco_buttons)
                if screen.id == 'traject_s':
                    trajectoryConfig_action(screen, trajectory_buttons)
                if screen.id == 'pos_s':
                    possysConfig_action(screen, pos_sys_buttons)
                if screen.id == 'lf_s':
                    lfConfig_action(screen, lf_buttons)
                for button in menu_buttons:
                    if button.isClicked(screen.position) == True:
                        if button.id == "maincontrol":
                            screen_id = 'control_s'
                        if button.id == "manualcontrol":
                            screen_id = 'manual_s'
                        if button.id == "ardronecomm.":
                            screen_id = 'ardrone_s'
                        if button.id == "boidconfig.":
                            screen_id = 'boid_conf_s'
                        if button.id == "lfconfig.":
                            screen_id = 'lf_s'
                        if button.id == "arucoconfig.":
                            screen_id = 'aruco_conf_s'
                            triggering['mode_screen'] = 3
                        if button.id == "trajectconfig.":
                            screen_id = 'traject_s'
                        if button.id == "positionconfig.":
                            screen_id = 'pos_s'
                        if screen_id != None:
                            screen_active[screen_id] = True
                            for key, _ in screen_active.items():
                                if key == screen.id:
                                    if key != screen_id:
                                        screen_active[key] = False
                        if button.id[0:5] == 'drone':
                            for drone in drones:
                                if int(button.id[-1]) == drone.id:
                                    configuration['Choosen Drone Id'] = drone.id
                    else:
                        if button.enable == True:
                            if button.id == "arucoconfig.":
                                if triggering['mode_screen'] == 3:
                                    triggering['mode_screen'] = 1
                    button.isClicked(screen.position)


def mainControl_action(control_screen, main_buttons, drones):
    """action or logic from main control screen"""
    if control_screen.active:
        mouse_pos = py.mouse.get_pos() - control_screen.position
        if control_screen.screen_image.get_rect().collidepoint(mouse_pos):
            for button in main_buttons:
                if button.id == 'boidstart':
                    configuration['Boid Start'] = button.isClicked(
                        control_screen.position)
                if button.id == 'trajectorystart':
                    configuration['Trajectory Start'] = button.isClicked(
                        control_screen.position)
                if button.id == 'drawradius':
                    configuration['Draw Radius'] = button.isClicked(
                        control_screen.position)
                if button.id == 'mousefollow':
                    configuration['Mouse Follow'] = button.isClicked(
                        control_screen.position)
                if button.id == 'movingdrone':
                    configuration['Moving Drone'] = button.isClicked(
                        control_screen.position)
                if button.id == 'plotscreen':
                    if button.isClicked(control_screen.position):
                        triggering['mode_screen'] = 2
                    elif not button.isClicked(control_screen.position) and triggering['mode_screen'] == 2:
                        triggering['mode_screen'] = 1
                if button.id == 'plotgraph':
                    triggering['plotgraph'] = button.isClicked(
                        control_screen.position)
                if button.id == 'recording':
                    configuration['Record Data'] = button.isClicked(
                        control_screen.position)
                if button.id == 'configdisplay':
                    pass
                    # triggering['config_display'] = not button.isClicked(
                    #     control_screen.position)
                if button.id == 'takeoffall':
                    if button.isClicked(control_screen.position):
                        for drone in drones:
                            drone.takeoff()
                if button.id == 'landingall':
                    if button.isClicked(control_screen.position):
                        for drone in drones:
                            drone.land()
                if button.id == 'startlf':
                    lf_data['Run'] = button.isClicked(control_screen.position)
                if button.id == 'startalgorithm':
                    configuration['Algorithm start'] = button.isClicked(
                        control_screen.position)
                if button.id == 'drawpath':
                    trajectory_data['Draw Path'] = button.isClicked(
                        control_screen.position)
                if button.id == 'setbattery25%':
                    if button.isClicked(control_screen.position):
                        for drone in drones:
                            if drone.id == configuration['Choosen Drone Id']:
                                drone.battery = 25
                if button.id == 'plotall':
                    triggering['plot_all_data'] = button.isClicked(
                        control_screen.position)
                if button.id == 'writecsv':
                    triggering['write_csv'] = button.isClicked(
                        control_screen.position)
                if button.id == 'selectalldrones':
                    if button.isClicked(control_screen.position):
                        configuration['Choosen Drone Id'] = len(drones)+1


def manualControl_action(drones, screen, manual_buttons):
    """action or logic from main control screen"""
    if screen.active:
        for button in manual_buttons:
            if button.id == 'increasespeed':
                if button.isClicked(screen.position):
                    if configuration['Set Speed'] < 1:
                        set_value['Set Speed'] += 0.1
            if button.id == 'decreasespeed':
                if button.isClicked(screen.position):
                    if configuration['Set Speed'] > 0:
                        set_value['Set Speed'] -= 0.1
            for drone in drones:
                if drone.id == configuration['Choosen Drone Id']:
                    # er_tes = drones[1].pos-drone.pos
                    # r_t, a_t = (er_tes).as_polar()
                    # tes_pos2 = py.Vector2()
                    # tes_pos2.from_polar((r_t, drone.angle))
                    # configuration['Angle to'] = er_tes.angle_to(tes_pos2)
                    # tes_pos = py.Vector2()
                    # tes_pos.from_polar(
                    #     (r_t, drone.angle))
                    # configuration['Tes rel pos'] = drone.pos + tes_pos
                    if button.id == 'forward':
                        if button.isClicked(screen.position):
                            movement['forward'] = configuration['Set Speed']
                            triggering['individu_type_plot'] = "forward"
                            configuration['Record Data'] = True
                        else:
                            if movement['forward'] != 0:
                                movement['forward'] = 0
                            # configuration['Record Data'] = False
                    if button.id == 'backward':
                        if button.isClicked(screen.position):
                            movement['backward'] = configuration['Set Speed']
                            triggering['individu_type_plot'] = "backward"
                            configuration['Record Data'] = True
                        else:
                            if movement['backward'] != 0:
                                movement['backward'] = 0
                            # configuration['Record Data'] = False
                    if button.id == 'rightward':
                        if button.isClicked(screen.position):
                            movement['right'] = configuration['Set Speed']
                            triggering['individu_type_plot'] = "right"
                            configuration['Record Data'] = True
                        else:
                            if movement['right'] != 0:
                                movement['right'] = 0
                            # configuration['Record Data'] = False
                    if button.id == 'leftward':
                        if button.isClicked(screen.position):
                            movement['left'] = configuration['Set Speed']
                            triggering['individu_type_plot'] = "left"
                            configuration['Record Data'] = True
                        else:
                            if movement['left'] != 0:
                                movement['left'] = 0
                            # configuration['Record Data'] = False
                    if all(i == 0 for i in (movement['forward'], movement['backward'], movement['right'], movement['left'])):
                        configuration['Record Data'] = False

                    if button.id == 'clockwise':
                        if button.isClicked(screen.position):
                            movement['cw'] = configuration['Set Speed']
                            # drone.test_stopwatch()
                        else:
                            # drone.test_reset_stopwatch()
                            movement['cw'] = 0
                    if button.id == 'countercw':
                        if button.isClicked(screen.position):
                            movement['ccw'] = configuration['Set Speed']
                        else:
                            movement['ccw'] = 0
                    if button.id == 'relativemove':
                        configuration['Relative Move'] = button.isClicked(
                            screen.position)
                    if button.id == 'resetstoredata':
                        if button.isClicked(screen.position):
                            drone.reset_record_data()
                            for dr in drones:
                                dr.reset_path()
                    if button.id == 'plotdata':
                        triggering['individu_plot'] = button.isClicked(
                            screen.position)
                    if button.id == 'takeofforland':
                        if button.isClicked(screen.position):
                            if drone.flying_state == False:
                                drone.takeoff()
                            else:
                                drone.land()
                    if any(i != 0 for i in movement.values()):
                        drone.move(forward=movement['forward'],
                                   backward=movement['backward'],
                                   right=movement['right'],
                                   left=movement['left'],
                                   cw=movement['cw'],
                                   ccw=movement['ccw'])


def arucoConfig_action(aruco_conf_screen, aruco_buttons):
    if aruco_conf_screen.active:
        for button in aruco_buttons:
            if button.id == 'activatearuco':
                if button.isClicked(aruco_conf_screen.position):
                    aruco_data['Detector Active'] = True
                else:
                    aruco_data['Detector Active'] = False
            if button.id == 'showcamera':
                aruco_data['Camera Active'] = button.isClicked(
                    aruco_conf_screen.position)
        pass


def trajectoryConfig_action(traject_conf_screen, trajectory_buttons):

    for button in trajectory_buttons:
        if button.id == 'drawpoints':
            trajectory_data['Draw Point'] = button.isClicked(
                traject_conf_screen.position)
        if button.id == 'drawline':
            trajectory_data['Draw Line'] = button.isClicked(
                traject_conf_screen.position)
        if button.id == 'restart':
            triggering['reset_trajectory'] = button.isClicked(
                traject_conf_screen.position)
    pass


def lfConfig_action(lf_conf_screen, lf_buttons):
    for button in lf_buttons:
        if button.id == 'recorddatalf':
            configuration['Record LF'] = button.isClicked(
                lf_conf_screen.position)
        if button.id == 'lfplot':
            triggering['lf_plot_data'] = button.isClicked(
                lf_conf_screen.position)
    pass


def ardroneControl_action(screen, ardrone_buttons):
    for button in ardrone_buttons:
        if button.id == 'connect':
            if not button.enable:
                button.enable = True
            if button.isClicked(screen.position):
                print("connecting...")
                triggering['ardrone_connect'] = True
            else:
                triggering['ardrone_connect'] = False
        else:
            if ar_drone_data['Connected'] == False:
                button.enable = False
            else:
                button.enable = True
        if ar_drone_data['Connected'] == True:
            if button.id == 'takeoff/land':
                if ar_drone_data['Flying State'] is not True:
                    if button.isClicked(screen.position):
                        ar_drone_data['Takeoff'] = True
                    else:
                        ar_drone_data['Takeoff'] = False
                else:
                    if button.isClicked(screen.position):
                        ar_drone_data['Landing'] = True
                    else:
                        ar_drone_data['Landing'] = False
            if button.id == 'switchcamera':
                if button.isClicked(screen.position):
                    ar_drone_data['Change camera'] = True
                else:
                    ar_drone_data['Change camera'] = False
            if button.id == 'trim':
                if button.isClicked(screen.position):
                    ar_drone_data['Trim'] = True
                else:
                    ar_drone_data['Trim'] = False
            if button.id == 'callibration':
                if button.isClicked(screen.position):
                    ar_drone_data['Calibration'] = True
                else:
                    ar_drone_data['Calibration'] = False
            if button.id == 'forward':
                if button.isClicked(screen.position):
                    ar_drone_movement['forward'] = configuration['Set Speed']
                else:
                    ar_drone_movement['forward'] = 0
                    # configuration['Record Data'] = False
            if button.id == 'backward':
                if button.isClicked(screen.position):
                    ar_drone_movement['backward'] = configuration['Set Speed']
                else:
                    ar_drone_movement['backward'] = 0
            if button.id == 'right':
                if button.isClicked(screen.position):
                    ar_drone_movement['right'] = configuration['Set Speed']
                else:
                    ar_drone_movement['right'] = 0
            if button.id == 'left':
                if button.isClicked(screen.position):
                    ar_drone_movement['left'] = configuration['Set Speed']
                else:
                    ar_drone_movement['left'] = 0
            if button.id == 'rotatecw':
                if button.isClicked(screen.position):
                    ar_drone_movement['cw'] = configuration['Set Speed']
                else:
                    ar_drone_movement['cw'] = 0
            if button.id == 'rotateccw':
                if button.isClicked(screen.position):
                    ar_drone_movement['ccw'] = configuration['Set Speed']
                else:
                    ar_drone_movement['ccw'] = 0
            if button.id == 'up':
                if button.isClicked(screen.position):
                    ar_drone_movement['up'] = configuration['Set Speed']
                else:
                    ar_drone_movement['up'] = 0
            if button.id == 'down':
                if button.isClicked(screen.position):
                    ar_drone_movement['down'] = configuration['Set Speed']
                else:
                    ar_drone_movement['down'] = 0
            if button.id == 'keycommand':
                if button.isClicked(screen.position):
                    triggering['keyboard_ctrl'] = True
                else:
                    triggering['keyboard_ctrl'] = False
    pass


def possysConfig_action(screen, buttons):
    if screen.active:
        for button in buttons:
            if button.id == 'drawcoord.':
                pos_sys_data['Draw Coord.'] = button.isClicked(screen.position)
            if button.id == 'synccoord.':
                pos_sys_data['Sync Coord.'] = button.isClicked(screen.position)
            if button.id == 'rectcoord.':
                pos_sys_data['Pos Rect'] = button.isClicked(screen.position)
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                           AR DRONE & MARKER PROCESS                          #
# ---------------------------------------------------------------------------- #


def ar_drone_process(ar_drones, drones):
    if configuration['Choosen Drone Id'] != 0:
        for ardrone in ar_drones:
            if isinstance(ardrone, CustomArdrone):
                if ardrone.id == configuration['Choosen Drone Id']:
                    ar_drone_cust = ardrone
    else:
        ar_drone_cust = None

    # """"AR Drone Process"""
    if configuration['Choosen Drone Id'] < 4:
        if ar_drone_cust is not None:
            if triggering['ardrone_connect']:
                if ar_drone_cust.drone is not None:
                    print("already connected")
                else:
                    ar_drone_cust.connect()
                    ar_drone_data['Connected'] = True
                    # ar_drone_cust.get_navdata()
            if ar_drone_cust.drone is None:
                ar_drone_data['Connected'] = False
            else:
                ar_drone_data['Connected'] = True

            if ar_drone_data['Connected'] == True:
                # ar_drone_cust.get_navdata()
                # for drone, ar_drone in zip(drones, ar_drones):
                #     if drone.id == ar_drone.id:
                #         drone.ar_drone_sync(ar_drone)
                # print(ar_drone_cust.navdemo)
                if ar_drone_cust.navdemo is not None:
                    """Navigation Data"""
                    ar_drone_data['Battery'] = ar_drone_cust.get_battery()
                    ar_drone_data['ID'] = ar_drone_cust.id
                    ar_drone_data['Vx'] = ar_drone_cust.vx
                    ar_drone_data['Vy'] = ar_drone_cust.vy
                    ar_drone_data['Altitude'] = ar_drone_cust.altitude
                    ar_drone_data['Flying State'] = ar_drone_cust.flying_state
                    ar_drone_data['Camera'] = (
                        "Front" if ar_drone_cust.camera_condition == "2" else "Bottom")

                    """AR Drone Input"""
                    if ar_drone_data['Takeoff'] == True:
                        ar_drone_cust.takeoff()
                    if ar_drone_data['Landing'] == True:
                        ar_drone_cust.land()
                    if ar_drone_data['Change camera'] == True:
                        ar_drone_cust.change_camera()
                    if ar_drone_data['Trim'] == True:
                        ar_drone_cust.trim()
                    if ar_drone_data['Calibration'] == True:
                        ar_drone_cust.calib()
                    if triggering['keyboard_ctrl'] is not True:
                        if any(i > 0 for i in ar_drone_movement.values()):
                            ar_drone_cust.move(forward=ar_drone_movement['forward'],
                                               backward=ar_drone_movement['backward'],
                                               right=ar_drone_movement['right'],
                                               left=ar_drone_movement['left'],
                                               cw=ar_drone_movement['cw'],
                                               ccw=ar_drone_movement['ccw'],
                                               up=ar_drone_movement['up'],
                                               down=ar_drone_movement['down'])

    for drone, ar_drone in zip(drones, ar_drones):
        if ar_drone.drone is not None:
            ar_drone.get_navdata()
            if drone.id == ar_drone.id:
                drone.ar_drone_sync(ar_drone)


def marker_process(ar_drones):

    if ar_drones is not None:
        total_ar_drones = len(ar_drones)

        for ardrone in ar_drones:
            # print(ardrone.id)

            if type(ardrone) is CustomArdrone:
                ardrone.marker_process()
                ardrone.aruco_data['Detector Active'] = aruco_data['Detector Active']
                if configuration['Choosen Drone Id'] != 0:
                    if configuration['Choosen Drone Id'] <= total_ar_drones:
                        if ardrone.id == configuration['Choosen Drone Id']:
                            aruco_data['Drone Camera'] = ardrone.id
                            ardrone.aruco_data['Camera Active'] = aruco_data['Camera Active']
                            aruco_data['Detected Id'] = ardrone.aruco_data['Detected Id']
                            aruco_data['Total Id'] = ardrone.aruco_data['Total Id']
            # else:


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                              BACKGROUND FUNCTION                             #
# ---------------------------------------------------------------------------- #

def background_process(all_init_data):
    "Processing Function"
    main_screen = surface_data['Main Screen']
    drones = all_init_data[2]
    # ardrones = all_init_data[10]
    main_time = py.time.get_ticks()
    for data in all_init_data:
        if isinstance(data, Trajectory):
            set_trajectory = data
        if isinstance(data, LeaderFollower):
            lead_foll = data
        if isinstance(data, Boid):
            boids = data
        if isinstance(data, PositionSystem):
            pos_sys = data

    if configuration['Set Speed'] != set_value['Set Speed']:
        configuration['Set Speed'] = round(set_value['Set Speed'], 1)
    for drone in drones:
        drone.setNavdata(configuration['FPS'], drones)
        drone.set_max_speed(configuration['Set Speed'])
    positioning_process(pos_sys, drones)
    trajectory_process(set_trajectory, drones)
    lf_process(lead_foll)
    if lf_data['Run'] == True:
        lead_foll.run()
    for key, value in configuration.items():
        if key == "Boid Start" and value:
            boids.run()
    #         pass
        if key == "Trajectory Start" and value:
            simple_algorithm(drones, main_time,
                             set_trajectory, boids, lead_foll)
        for drone in drones:
            if key == "Relative Move":
                drone.relative_move = value
            if key == "Draw Radius":
                drone.rad_act = value
            if key == "Mouse Follow" and value:
                mainS_mouse_pos = py.Vector2(
                    py.mouse.get_pos()-main_screen.position)
                est_mouse_pos = py.Vector2(
                    (mainS_mouse_pos.x-105)*1.2, (mainS_mouse_pos.y-175)*1.2)
                if py.mouse.get_pressed()[0] == True and main_screen.rect.collidepoint(mainS_mouse_pos):
                    if drone.id == configuration['Choosen Drone Id']:
                        # drone.set_target(mainS_mouse_pos)
                        drone.est_set_target(est_mouse_pos)
                    configuration['Record Data'] = True
                else:
                    if configuration['Record Data'] == True:
                        configuration['Record Data'] = False

            if key == "Moving Drone" and value:
                mainS_mouse_pos = py.Vector2(
                    py.mouse.get_pos()-main_screen.position)
                est_mouse_pos = py.Vector2(
                    (mainS_mouse_pos.x-105)*1.2, (mainS_mouse_pos.y-175)*1.2)
                if py.mouse.get_pressed()[0] and main_screen.rect.collidepoint(mainS_mouse_pos):
                    if drone.id == configuration['Choosen Drone Id']:
                        drone.pos = mainS_mouse_pos
                        drone.est_pos = est_mouse_pos
            if triggering['plotgraph'] == True:
                if drone.id == configuration['Choosen Drone Id']:
                    # plotting_windows(drone.store_data['Time'],
                    #                  drone.store_data['Vx'], drone.store_data['Vy'])
                    signal_plot(drone)
            if triggering['individu_plot'] == True:
                if drone.id == configuration['Choosen Drone Id']:
                    plot_drone_data(drone, triggering['individu_type_plot'])
            if configuration['Choosen Drone Id'] < 4:
                if drone.id == configuration['Choosen Drone Id']:
                    if triggering['write_csv'] == True:
                        drone.printcsv()
                        print('Printed')
            else:
                if triggering['write_csv'] == True:
                    drone.printcsv()
                    print('Printed')
        if triggering['write_csv'] == True:
            lead_foll.printcsv()
        triggering['plotgraph'] = False
        triggering['individu_plot'] = False
    if triggering['plot_all_data'] == True:
        plotting_all(drones)
        triggering['plot_all_data'] = False
    if configuration['Algorithm start'] == True:
        algorithm(drones, boids, lead_foll)
    # # time.sleep(0.001)
    pass


def simple_algorithm(drones, main_time, set_trajectory, boids, leadfoll):
    test_algorithm = "cyclic"

    if test_algorithm == "single":
        """Test Single Drone"""
        for drone in drones:
            if drone.id == configuration['Choosen Drone Id']:
                waktu = drone.stopwth.delta_time
                # drone.est_set_target(
                #     (100, 100))
                # drone.est_set_target((420, 135))
                if storing["init_track_time"] == 0:
                    storing["init_track_time"] = main_time
                if drone.flying_state is False:
                    if set_trajectory.state == 'standby':
                        drone.takeoff()
                    else:
                        drone.stopwth.reset()
                else:
                    drone.stopwth.start()
                    if waktu > 8:
                        set_trajectory.run(
                            main_time-storing["init_track_time"])
                        if set_trajectory.state == 'finish':
                            drone.stopwth.reset()
                    else:
                        if set_trajectory.state == 'finish' and waktu > 2:
                            drone.land()
        """Test Multi Drone"""
    elif test_algorithm == "boid":
        for drone in drones:
            if drone.id == 1:
                waktu = drone.stopwth.delta_time
            if drone.flying_state is False:
                if waktu < 1:
                    drone.takeoff()
            else:
                if drone.id == 1:
                    drone.stopwth.start()
                else:
                    pass
            if drone.flying_state is True and waktu > 14:
                drone.land()

        if all(drone.flying_state is True for drone in drones):
            if waktu > 8:
                boids.run()
    elif test_algorithm == "leadfoll":
        for drone in drones:
            if drone.id == 1:
                waktu = drone.stopwth.delta_time

            if drone.flying_state is False:
                if waktu < 1:
                    drone.takeoff()
            else:
                if drone.id == 1:
                    drone.stopwth.start()
                else:
                    pass
            if drone.flying_state is True and set_trajectory.state == 'finish':
                drone.land()

        if all(drone.flying_state is True for drone in drones):
            if 10 > waktu > 7:
                boids.run()
            elif waktu >= 10 and set_trajectory.state != 'finish':
                leadfoll.run()
    else:
        cyclic_condition = leadfoll.cyclic()
        for drone in drones:
            if drone.id == 1:
                drone.stopwth.start()
                waktu = drone.stopwth.delta_time
            if drone.id == 2:
                drone.stopwth.start()
                waktu_cyclic = drone.stopwth
            if drone.flying_state is False:
                if waktu < 1:
                    drone.takeoff()
            # else:
            #     if drone.id == 1 or drone.id == 2:
            #         drone.stopwth.start()
            #     else:
            #         pass
            if drone.flying_state is True and set_trajectory.state == 'finish':
                drone.land()

        if all(drone.flying_state is True for drone in drones):
            if 10 > waktu > 7:
                boids.run()
        if waktu >= 10 and set_trajectory.state != 'finish':
            # print(waktu_cyclic.delta_time)

            if not cyclic_condition:
                if waktu_cyclic.delta_time > 3:
                    leadfoll.run()
            else:
                waktu_cyclic.reset()


def algorithm(drones, boids, lead_foll):
    # pos_sys_data['Sync Coord.'] = True
    # aruco_data['Detector Active'] = True
    cyclic_condition = lead_foll.cyclic()
    # cyclic_condition = False
    just_boid_init = True
    if not cyclic_condition:
        for drone in drones:
            distance_data.update(drone.distance_check(drones))
        if all(100 < i <= 300 for i in distance_data.values()):
            configuration['Boid has run'] = True
        if any(i < 100 or i >= 300 for i in distance_data.values()) and not configuration['Boid has run']:
            for drone in drones:
                if drone.flying_state is not True:
                    if drone.is_health() is True:
                        drone.takeoff()
            boids.run()
        else:
            if just_boid_init is not True:
                if any(i < 100 or i >= 300 for i in distance_data.values()):
                    boids.run()
                else:
                    lead_foll.run()
            else:
                lead_foll.run()
    pass


def trajectory_process(trajectory, drones):
    trajectory_data['ID Drone'] = trajectory.drone.id
    trajectory_data['Total Track Point'] = len(trajectory.track_points)
    trajectory_data['Track Point Passed'] = len(trajectory.store_track)
    trajectory_data['Passed Type'] = trajectory.passed_type
    trajectory_data['Track Distance'] = round(trajectory.track_distance, 2)
    trajectory_data['State'] = trajectory.state
    if triggering['reset_trajectory']:
        trajectory.reset()
    if trajectory.passed_type == "Time":
        trajectory_data['Time'] = trajectory.time
    for drone in drones:
        drone.path_act = trajectory_data['Draw Path']


def positioning_process(pos_sys, drones):
    if pos_sys_data['Sync Coord.'] == True:
        for drone in drones:
            drone.synchronize_position(pos_sys)
            # for point in pos_sys.all_rect:
            # if point.rect.collidepoint(drone.pos-pos_sys.pos):
            #     drone.est_pos = py.Vector2(point.carried_pos)
            #     drone.pos = point.pos+pos_sys.pos
            # if drone.id == configuration['Choosen Drone Id']:
            #     if aruco_data['Detector Active'] == True:
            #         if aruco_data['Detected Id'] != "None":
            #             if point.id == aruco_data['Detected Id']:
            #                 drone.est_pos = point.carried_pos
            #                 drone.pos = point.pos+pos_sys.pos
    pos_sys.draw_rect_pos = pos_sys_data['Pos Rect']


def lf_process(lf_data):
    if triggering['lf_plot_data'] == True:
        lf_plot(lf_data)
        triggering['lf_plot_data'] = False
    pass
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                SCREEN FUNCTION                               #
# ---------------------------------------------------------------------------- #

def update_screen(all_init_data):
    "Refreshing screen"
    win = all_init_data[0]
    all_screen = all_init_data[1]
    drones = all_init_data[2]
    drone_group = all_init_data[3]
    set_trajectory = all_init_data[4]
    all_buttons = all_init_data[5]
    ar_drones = general_data['AR Drones']
    all_markers = general_data['All Markers']

    for data in all_init_data:
        if type(data) is PositionSystem:
            pos_sys = data

    if len(all_markers) > 0:
        for marker in all_markers:
            if isinstance(marker, ArucoMarker):
                marker.draw_pygame()
    if ar_drones is not None:
        if configuration['Choosen Drone Id'] != 0:
            for ar_drone in ar_drones:
                if type(ar_drone) is CustomArdrone:
                    if ar_drone.id == configuration['Choosen Drone Id']:
                        aruco_mark = ar_drone.aruco_detector
        else:
            aruco_mark = None
    else:
        aruco_mark = None
    "action"
    action(drones, set_trajectory, all_buttons, all_screen)
    "buttons"
    main_buttons, main_button_group = all_buttons[0], all_buttons[3]
    menu_buttons, menu_button_group = all_buttons[2], all_buttons[5]
    manual_buttons, manual_button_group = all_buttons[1], all_buttons[4]
    ardrone_buttons, ardrone_button_group = all_buttons[6], all_buttons[7]
    config_buttons, config_button_group = all_buttons[8], all_buttons[9]
    aruco_buttons, aruco_button_group = all_buttons[10], all_buttons[11]
    trajectory_buttons, trajectory_button_group = all_buttons[12], all_buttons[13]
    pos_sys_buttons, pos_sys_button_group = all_buttons[14], all_buttons[15]
    lf_buttons, lf_button_group = all_buttons[16], all_buttons[17]
    for screen in all_screen:
        screen.change_mode(triggering['mode_screen'])
        # if isinstance(screen, BottomScreen):
        #     bottom_screen.append(screen)
        if screen.active == True:
            screen.update_screen()
            if isinstance(screen, BottomScreen):
                menu_button_group.draw(screen.screen_image)
                # py.draw.rect(screen,(255,100,100), (2.5, 2.5, 15, 15), 1, border_radius=25) 
                menu_button_group.update(
                    screen.screen_image, screen.position, scale=0.8)
            if screen.id == "main_s":
                main_screen_update(screen, drones, drone_group,
                                   set_trajectory, pos_sys)
            if screen.id == "aruco_main_s":
                # default
                # aruco_main_screen_update(screen, aruco_mark)
                # ardrone
                if aruco_mark is not None:
                    aruco_main_screen_update(screen, aruco_mark)
                else:
                    pass
            if screen.id == "control_s":
                control_screen_update(screen, main_button_group, main_buttons)
            if screen.id == "aruco_conf_s":
                aruco_config_screen_update(
                    screen, aruco_button_group, aruco_buttons)
            if screen.id == "manual_s":
                manual_control_screen_update(
                    screen, manual_button_group, manual_buttons)
            # # if screen.id == "state_s":
            # #     state_screen_update(screen, drones)
            if screen.id == "config_s":
                config_screen_update(
                    screen, config_button_group, config_buttons)
            # if screen.id == "plots_s":
            #     # # plot1.update(
            #     # #     (Drone1_data['Time'], Drone1_data['Vx'], Drone1_data['Vy']))
            #     # if triggering['plotgraph']:
            #     #     plot1.run()
            #     # screen.screen_image.blit(plot1.screen, (10, 100))
            #     pass
            if screen.id == "ardrone_s":
                ardrone_control_screen_update(
                    screen, ardrone_button_group, ardrone_buttons)
            if screen.id == "traject_s":
                traject_control_screen_update(
                    screen, trajectory_button_group, trajectory_buttons)
            if screen.id == "lf_s":
                lf_config_screen_update(
                    screen, lf_button_group, lf_buttons)
            if screen.id == "pos_s":
                position_config_screen_update(
                    screen, pos_sys_button_group, pos_sys_buttons)
            win.blit(screen.screen_image, screen.position)

    for key, value in screen_active.items():
        for screen in all_screen:
            if screen.id == key:
                screen.active = value
    for button, screen in zip(menu_buttons, surface_data['Bottom Screen']):
        button.enable = not screen.active


def main_screen_update(main_screen, drones, drone_group, set_trajectory, pos_sys):
    """refreshing for main screen"""
    if pos_sys_data['Draw Coord.'] == True:
        pos_sys.draw(main_screen.screen_image)
    drone_group.draw(main_screen.screen_image)
    drone_group.update()
    for drone in drones:
        drone.draw_radius(main_screen.screen_image)
        # if trajectory_data['Track Point Passed'] != 0:
        drone.draw_path(main_screen.screen_image)
        # if drone.id == 1:
        #     drone.draw_target_line(main_screen.screen_image)
    set_trajectory.scale = main_screen.screen_scale
    if trajectory_data['Draw Point'] == True:
        set_trajectory.draw_points(main_screen.screen_image)
    if trajectory_data['Draw Line'] == True:
        set_trajectory.draw_target_line()
    pass


def state_screen_update(screen, drones):
    text_store = []
    for drone in drones:
        text_store.append(drone.get_state())
    screen.scroll = surface_data['Left Scroll']
    screen.draw_content(text_store)


def config_screen_update(screen, config_button_group, config_buttons):

    screen.draw_content(
        configuration_display[triggering['config_page_value']])
    config_button_group.draw(screen.screen_image)
    config_button_group.update(
        screen.screen_image, screen.position)
    for button in config_buttons:
        button.update_size(multiplier=0.8)
        if button.id == 'nextpage':
            if button.isClicked(screen.position):
                if triggering['config_page_value'] < (len(configuration_display)-1):
                    triggering['config_page_value'] += 1
                elif triggering['config_page_value'] == (len(configuration_display)-1):
                    triggering['config_page_value'] = 0
        if button.id == 'beforepage':
            if button.isClicked(screen.position):
                if triggering['config_page_value'] > 0:
                    triggering['config_page_value'] -= 1
                elif triggering['config_page_value'] == 0:
                    triggering['config_page_value'] = (
                        len(configuration_display)-1)


def control_screen_update(control_screen, main_button_group, main_buttons):
    """refreshing for main control screen"""
    """get surface size"""
    # cons_width, cons_height = control_screen.get_size()
    """describe buttons"""
    """>> main buttons"""
    # boid_button = main_buttons[0]
    """draw the buttons"""

    main_button_group.draw(control_screen.screen_image)
    main_button_group.update(control_screen.screen_image,
                             control_screen.position)
    """update position for windows change"""
    # boid_button.update_position((cons_width*0.17, cons_height*0.2))
    for button in main_buttons:
        button.update_size(multiplier=0.8)


def manual_control_screen_update(manual_screen, manual_button_group, manual_buttons):
    """refreshing for manual control screen"""
    """draw the buttons"""

    manual_button_group.draw(manual_screen.screen_image)
    manual_button_group.update(
        manual_screen.screen_image, manual_screen.position)
    """update position for windows change"""
    # forward_button.update_position((mans_width*0.17, mans_height*0.2))
    # backward_button.update_position((mans_width*0.17, mans_height*0.4))
    # right_button.update_position((mans_width*0.22, mans_height*0.4))
    # left_button.update_position((mans_width*0.12, mans_height*0.4))
    for button in manual_buttons:
        button.update_size(multiplier=0.8)


def ardrone_control_screen_update(ardrone_screen, ardrone_button_group, ardrone_buttons):

    ardrone_button_group.draw(ardrone_screen.screen_image)
    ardrone_button_group.update(
        ardrone_screen.screen_image, ardrone_screen.position)
    for button in ardrone_buttons:
        button.update_size(multiplier=0.8)


def traject_control_screen_update(traject_screen, trajectory_button_group, trajectory_buttons):
    trajectory_button_group.draw(traject_screen.screen_image)
    trajectory_button_group.update(
        traject_screen.screen_image, traject_screen.position)
    for button in trajectory_buttons:
        button.update_size(multiplier=0.8)


def lf_config_screen_update(screen, button_group, buttons):
    button_group.draw(screen.screen_image)
    button_group.update(
        screen.screen_image, screen.position)
    for button in buttons:
        button.update_size(multiplier=0.8)


def position_config_screen_update(screen, button_group, buttons):
    button_group.draw(screen.screen_image)
    button_group.update(
        screen.screen_image, screen.position)
    for button in buttons:
        button.update_size(multiplier=0.8)


def aruco_main_screen_update(aruco_screen, aruco_class):
    if aruco_data['Camera Active']:
        # aruco_screen.screen_image.blit(aruco_class.get_image(), (100, 100))
        aruco_screen.screen_image.blit(aruco_class.rotated_surface, (100, 100))
    else:
        aruco_screen.screen_image.blit(
            aruco_class.default_surface, (100, 100))


def aruco_config_screen_update(aruco_config_screen, aruco_button_group, aruco_buttons):
    aruco_button_group.draw(aruco_config_screen.screen_image)
    aruco_button_group.update(
        aruco_config_screen.screen_image, aruco_config_screen.position)
    for button in aruco_buttons:
        button.update_size(multiplier=0.8)
    pass

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                 MAIN FUNCTION                                #
# ---------------------------------------------------------------------------- #
def maximize_window():
    """maximizing windows at start"""
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def events(all_init_data):
    all_screen = all_init_data[1]
    drones = all_init_data[2]
    keys = py.key.get_pressed()

    for data in all_init_data:
        if isinstance(data, LeaderFollower):
            leadfoll = data
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit(0)
        for screen in all_screen:
            if screen.id == 'state_s':
                mouse_pos = (py.mouse.get_pos() - screen.position)
                screen_rect = screen.screen_image.get_rect()
                if screen_rect.collidepoint(mouse_pos):
                    if event.type == py.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            surface_data['Left Scroll'] = min(
                                100, surface_data['Left Scroll']+5)
                        if event.button == 5:
                            surface_data['Left Scroll'] = max(
                                -200, surface_data['Left Scroll']-5)
                    pass
                else:
                    surface_data['Left Scroll'] = 0
            if event.type == storingData_event:
                if configuration['Record Data']:
                    for drone in drones:
                        drone.record_data()
                if configuration['Record LF']:
                    leadfoll.record()
        for drone in drones:
            if configuration['Choosen Drone Id'] <= len(drones):
                if drone.id == configuration['Choosen Drone Id']:
                    if keys[py.K_w]:
                        drone.move(forward=configuration['Set Speed'])
                    if keys[py.K_s]:
                        drone.move(backward=configuration['Set Speed'])
                    if keys[py.K_d]:
                        drone.move(right=configuration['Set Speed'])
                    if keys[py.K_a]:
                        drone.move(left=configuration['Set Speed'])
                    # if keys[py.K_w]:
                    #     drone.move(forward=0.005)
                    # if keys[py.K_s]:
                    #     drone.move(backward=0.005)
                    # if keys[py.K_d]:
                    #     drone.move(right=0.005)
                    # if keys[py.K_a]:
                    #     drone.move(left=0.005)
                    if keys[py.K_RETURN]:
                        drone.takeoff()
                    if keys[py.K_SPACE]:
                        drone.land()
            else:

                if keys[py.K_w]:
                    drone.move(forward=configuration['Set Speed'])
                if keys[py.K_s]:
                    drone.move(backward=configuration['Set Speed'])
                if keys[py.K_d]:
                    drone.move(right=configuration['Set Speed'])
                if keys[py.K_a]:
                    drone.move(left=configuration['Set Speed'])
                if keys[py.K_RETURN]:
                    drone.takeoff()
                if keys[py.K_SPACE]:
                    drone.land()


def setup_pygame():
    """pygame option"""

    py.display.set_caption("Parrot AR Drone 2.0 Control and Simulation")
    py.time.set_timer(storingData_event, 30)
    py.event.set_allowed([py.QUIT, py.KEYDOWN, py.KEYUP])
    #--------------------------------------------------------------#

    """drone sprite"""
    drones, drone_group = set_up_drones(3)
    general_data['Drones'] = drones
    ardrones = general_data['AR Drones']

    #--------------------------------------------------------------#

    """set screen"""
    win = py.display.set_mode((WIDTH, HEIGHT), flags, 16)
    maximize_window()
    all_screen = set_up_screen()
    all_buttons = set_up_buttons(
        all_screen, drones)
    for ardrone in ardrones:
        if isinstance(ardrone, CustomArdrone):
            ardrone.aruco_detector.init_pygame()
            general_data['All Markers'].append(ardrone.aruco_detector)
    #--------------------------------------------------------------#

    """trajectory setup"""
    set_trajectory = set_up_trajectory(drones[0])
    leadfoll = LeaderFollower(drones, 1, set_trajectory)
    configuration_display.append(leadfoll.lf_data)
    #--------------------------------------------------------------#

    dummy = 0

    #--------------------------------------------------------------#

    """Boid set up"""
    boids = Boid(drones)
    #--------------------------------------------------------------#

    """positioning set up"""
    pos_sys = PositionSystem()
    #--------------------------------------------------------------#

    """display data"""
    configuration_display.append(pos_sys_data)
    configuration_display.append(aruco_data)
    #--------------------------------------------------------------#

    all_init_data = [win, all_screen, drones,
                     drone_group, set_trajectory, all_buttons, dummy, leadfoll, boids, pos_sys]
    return all_init_data


def pygame_funct():
    py.init()
    all_init_data = setup_pygame()
    win = all_init_data[0]
    clock = py.time.Clock()
    ar_drones = general_data['AR Drones']
    drones = general_data['Drones']
    try:
        while 1:
            win.fill(WHITE)
            events(all_init_data)
            ar_drone_process(ar_drones, drones)
            background_process(all_init_data)
            update_screen(all_init_data)
            configuration['FPS'] = int(clock.get_fps())
            # print(configuration['FPS'],end='\r')
            clock.tick(120)
            py.display.update()

    except (KeyboardInterrupt, SystemExit):
        py.quit()


def ardrone_funct():
    ar_drones = general_data['AR Drones']
    drones = general_data['Drones']

    try:
        while 1:
            ar_drone_process(ar_drones, drones)
            # marker_process(ar_drones)
    except(KeyboardInterrupt, SystemExit):
        for drone in ar_drones:
            drone.disconnect()


def marker_funct():
    ar_drones = general_data['AR Drones']
    try:
        while 1:
            marker_process(ar_drones)
    except(KeyboardInterrupt, SystemExit):
        for drone in ar_drones:
            if drone.aruco_detector is not None:
                drone.aruco_detector.done()


def main():

    thread_1 = threading.Thread(target=pygame_funct)
    thread_2 = threading.Thread(target=ardrone_funct)
    thread_3 = threading.Thread(target=marker_funct)
    thread_1.setDaemon(True)
    thread_3.daemon = True
    thread_1.start()
    thread_3.start()
    thread_2.start()


if __name__ == '__main__':
    set_up_ardrones()
    main()

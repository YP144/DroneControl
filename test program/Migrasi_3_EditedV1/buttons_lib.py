import pygame as py
from Button import *


def set_up_buttons(all_screen, drones):
    """set all buttons for every screen"""
    control_screen = all_screen[3]
    manual_screen = all_screen[4]

    """get surface size"""
    cons_width, cons_height = control_screen.get_size()
    mans_width, mans_height = manual_screen.get_size()
    """for Main Control Screen"""
    thresw = 0.05
    

    boid_button = Button((cons_width*(0.125 + thresw), cons_height*0.4),
                         'Boid Start', type='toggle')
    trajectory_button = Button((cons_width*(0.225 + thresw), cons_height*0.4),
                               'Trajectory Start', type='toggle')
    draw_rad_button = Button((cons_width*(0.325 + thresw), cons_height*0.4),
                             'Draw Radius', type='toggle')
    mouse_foll_button = Button((cons_width*(0.425 + thresw), cons_height*0.4),
                               'Mouse Follow', type='toggle')
    move_drone_button = Button((cons_width*(0.525 + thresw), cons_height*0.4),
                               'Moving Drone', type='toggle')
    plot_screen_button = Button((cons_width*(0.625 + thresw), cons_height*0.4),
                                'Plot Screen', type='toggle')
                                


    plot_graph_button = Button((cons_width*(0.125 + thresw), cons_height*0.625),
                               'Plot Graph')
    record_button = Button((cons_width*(0.225 + thresw), cons_height*0.625),
                           'Recording', type='toggle')
    config_display_button = Button((cons_width*(0.325 + thresw), cons_height*0.625),
                                   'Config Display', type='toggle')
    take_off_button = Button((cons_width*(0.425 + thresw), cons_height*0.625),
                             'Take Off All')
    landing_button = Button((cons_width*(0.525 + thresw), cons_height*0.625),
                            'Landing All')
    start_lf_button = Button((cons_width*(0.625 + thresw), cons_height*0.625),
                             'Start LF', type='toggle')

                             
    start_algo_button = Button((cons_width*(0.125 + thresw), cons_height*0.85),
                               'Start Algorithm', type='toggle')
    draw_path_button = Button((cons_width*(0.225 + thresw), cons_height*0.85), 
                                'Draw Path', type='toggle')
    set_battery_error_button = Button((cons_width*(0.325 + thresw), cons_height*0.85), 
                                'Set Battery 25%')
    plot_all_button = Button((cons_width*(0.425 + thresw), cons_height*0.85), 
                                'Plot All')
    write_csv_button = Button((cons_width*(0.525 + thresw), cons_height*0.85),
                              'Write CSV')
    all_drone_button = Button((cons_width*(0.625 + thresw), cons_height*0.85),
                              'Select All Drones')




    """for Manual Control Screen"""
    forward_button = Button((mans_width*0.25, mans_height*0.2),
                            'Forward', type='toggle')
    backward_button = Button((mans_width*0.25, mans_height*0.4),
                             'Backward', type='toggle')
    right_button = Button((mans_width*0.32, mans_height*0.4),
                          'Rightward', type='toggle')
    left_button = Button((mans_width*0.18, mans_height*0.4),
                         'Leftward', type='toggle')
    cw_button = Button((mans_width*0.40, mans_height*0.2),
                       'Clockwise', type='toggle')
    ccw_button = Button((mans_width*0.40, mans_height*0.4),
                        'Counter CW', type='toggle')
    inc_speed_button = Button((mans_width*0.52, mans_height*0.2),
                              'Increase Speed')
    dec_speed_button = Button((mans_width*0.52, mans_height*0.4),
                              'Decrease Speed')
    relative_move_button = Button((mans_width*0.62, mans_height*0.2),
                                  'Relative Move', type='toggle')
    reset_data_button = Button((mans_width*0.18, mans_height*0.7),
                               'Reset Store Data')
    plot_data_button = Button((mans_width*0.30, mans_height*0.7),
                              'Plot Data')
    fly_land_button = Button((mans_width*0.5, mans_height*0.7),
                             'Take Off or Land')
    """for AR Drone Control Screen"""
    ardrone_buttons_set = ["Connect",
                           "Disconnect",
                           "Emergency Stop",
                           "Trim",
                           "Callibration",
                           "Take Off/Land",
                           "Switch Camera",
                           "Forward",
                           "Left",
                           "Backward",
                           "Right",
                           "Rotate CW",
                           "Rotate CCW",
                           "Up",
                           "Down",
                           "Key Command"
                           ]
    ardrone_buttons_pos = []
    for i in range(len(ardrone_buttons_set)):
        if i < 7:
            if i == 1:
                ardrone_buttons_pos.append((250+(i*85), 50))
            elif i == 2:
                ardrone_buttons_pos.append((250+(i*100), 50))
            elif i == 4:
                ardrone_buttons_pos.append((250+(i*91), 50))
            elif i == 6:
                ardrone_buttons_pos.append((250+(i*98), 50))
            else:
                ardrone_buttons_pos.append((250+(i*94), 50))
        else:
            if 7 < i < 11:
                ardrone_buttons_pos.append((250+((i-8)*83), 150))
            elif i == 11:
                ardrone_buttons_pos.append((250+((i-8)*90), 100))
            elif i == 12:
                ardrone_buttons_pos.append((250+((i-9)*90), 150))
            elif i == 13:
                ardrone_buttons_pos.append((250+((i-9)*90), 100))
            elif i == 14:
                ardrone_buttons_pos.append((250+((i-10)*90), 150))
            else:
                ardrone_buttons_pos.append((250+((i-6)*80), 50))

    """for ArUco Config screen"""
    activate_aruco_button = Button((250, 100),
                                   'Activate ArUco', type='toggle')
    show_camera_button = Button((380, 100),
                                'Show Camera', type='toggle')
    """for Trajectory Config screen"""
    draw_point_button = Button((250, 100),
                               'Draw Points', type='toggle')
    draw_line_button = Button((350, 100),
                              'Draw Line', type='toggle')
    restart_button = Button((430, 100),
                            'Restart')
    """for ArUco Config screen"""
    draw_coord_button = Button((250, 100),
                               'Draw Coord.', type='toggle')
    sync_button = Button((350, 100),
                         'Sync Coord.', type='toggle')
    draw_rect_button = Button((450, 100),
                              'Rect Coord.', type='toggle')
    """for LF Config screen"""
    rec_lf_button = Button((250, 100), 'Record Data LF', type='toggle')
    plot_lf_button = Button((350, 100), 'Lf Plot')
    """all Menu's"""
    """>> Right Menu"""
    main_button = Button((cons_width*0.85, cons_height*0.2), 'Main Control')
    manual_button = Button(
        (cons_width*0.94, cons_height*0.2), 'Manual Control')
    ardrone_button = Button(
        (cons_width*0.843, cons_height*0.4), 'AR Drone Comm.')
    boid_conf_button = Button(
        (cons_width*0.928, cons_height*0.4), 'Boid Config.')
    lf_conf_button = Button(
        (cons_width*0.855, cons_height*0.6), 'LF Config.')
    aruco_conf_button = Button(
        (cons_width*0.935, cons_height*0.6), 'ArUco Config.')
    traject_conf_button = Button(
        (cons_width*0.845, cons_height*0.8), 'Traject Config.')
    pos_conf_button = Button(
        (cons_width*0.935, cons_height*0.8), 'Position Config.')
    """config button"""
    next_config_page_button = Button((170, 500), 'Next Page')
    before_config_page_button = Button((70, 500), 'Before Page')
    """packaging"""
    main_buttons = [boid_button,
                    trajectory_button,
                    draw_rad_button,
                    mouse_foll_button,
                    move_drone_button,
                    plot_screen_button,
                    plot_graph_button,
                    record_button,
                    config_display_button,
                    take_off_button,
                    landing_button,
                    start_lf_button,
                    start_algo_button,
                    draw_path_button,
                    set_battery_error_button,
                    plot_all_button,
                    write_csv_button,
                    all_drone_button]
    manual_buttons = [forward_button,
                      backward_button,
                      right_button,
                      left_button,
                      cw_button,
                      ccw_button,
                      inc_speed_button,
                      dec_speed_button,
                      relative_move_button,
                      reset_data_button,
                      plot_data_button,
                      fly_land_button]
    aruco_buttons = [activate_aruco_button,
                     show_camera_button]
    trajectory_buttons = [draw_point_button,
                          draw_line_button,
                          restart_button]
    lf_buttons = [rec_lf_button,
                  plot_lf_button]
    pos_sys_buttons = [draw_coord_button,
                       sync_button,
                       draw_rect_button]
    menu_buttons = [main_button,
                    manual_button,
                    ardrone_button,
                    boid_conf_button,
                    lf_conf_button,
                    aruco_conf_button,
                    traject_conf_button,
                    pos_conf_button]
    config_buttons = [before_config_page_button,
                      next_config_page_button]

    ardrone_buttons = []
    for button, pos in zip(ardrone_buttons_set, ardrone_buttons_pos):
        if ardrone_buttons_set.index(button) < 7:
            ardrone_button = Button(pos, button, condition=False)
        else:
            ardrone_button = Button(
                pos, button, type='toggle', condition=False)
        ardrone_buttons.append(ardrone_button)

    """choosing drone"""
    for x in range(len(drones)):
        if 0 < len(drones) <= 6:
            if len(drones) < 3:
                drone_button = Button(
                    (cons_width*0.05, cons_height*(0.4 + (0.2*x))), f'Drone {x+1}')
            else:
                if x < 3:
                    drone_button = Button(
                        # (cons_width*0.01, cons_height*(0.4 + (0.2*x))), f'Drone {x+1}')
                        (cons_width*0.05, cons_height*(0.4 + (0.225*x))), f'Drone {x+1}')

                else:
                    drone_button = Button(
                        (cons_width*0.09, cons_height*(0.4 + (0.2*(x-3)))), f'Drone {x+1}')
        else:
            drone_button = Button(
                (cons_width*0.08, cons_height*0.4), f'Drone cannot be choose', condition=False)
        menu_buttons.append(drone_button)

    """sprite grouping"""
    main_button_group = py.sprite.Group()
    main_button_group.add(main_buttons)
    manual_button_group = py.sprite.Group()
    manual_button_group.add(manual_buttons)
    menu_button_group = py.sprite.Group()
    menu_button_group.add(menu_buttons)
    ardrone_button_group = py.sprite.Group()
    ardrone_button_group.add(ardrone_buttons)
    aruco_button_group = py.sprite.Group()
    aruco_button_group.add(aruco_buttons)
    config_button_group = py.sprite.Group()
    config_button_group.add(config_buttons)
    trajectory_button_group = py.sprite.Group()
    trajectory_button_group.add(trajectory_buttons)
    lf_button_group = py.sprite.Group()
    lf_button_group.add(lf_buttons)
    pos_sys_button_group = py.sprite.Group()
    pos_sys_button_group.add(pos_sys_buttons)
    all_buttons = (main_buttons,
                   manual_buttons,
                   menu_buttons,
                   main_button_group,
                   manual_button_group,
                   menu_button_group,
                   ardrone_buttons,
                   ardrone_button_group,
                   config_buttons,
                   config_button_group,
                   aruco_buttons,
                   aruco_button_group,
                   trajectory_buttons,
                   trajectory_button_group,
                   pos_sys_buttons,
                   pos_sys_button_group,
                   lf_buttons,
                   lf_button_group)
    return all_buttons

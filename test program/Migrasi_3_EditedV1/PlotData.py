from matplotlib import pyplot as plt


def plotting_windows(x, y1, y2):
    fig, ax = plt.subplots(1, 1)
    ax.clear()
    fig.suptitle('Drone Data')
    ax.plot(x, y1, color='g', label='Vx')
    ax.plot(x, y2, color='r', label='Vy')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Speed(m/s)')
    ax.grid(True)
    ax.autoscale(True)
    ax.legend()
    plt.show()


def plotting_all(drones):
    for drone in drones:
        fig, ax = plt.subplots(1, 1)
        fig2, [ax2, ax3] = plt.subplots(2, 1)
        ax.clear()
        ax2.clear()
        ax3.clear()
        fig.suptitle(f'Drone {drone.id} Speed Data')
        fig2.suptitle(f'Drone {drone.id} Position Data')
        x = drone.store_data['Time']
        vx = drone.store_data['Vx']
        vy = drone.store_data['Vy']
        pos_x = drone.store_data['Position x']
        pos_y = drone.store_data['Position y']
        set_point_x = drone.store_data['Set Point x']
        set_point_y = drone.store_data['Set Point y']
        ax.plot(x, vx, color='g', label='Vx')
        ax.plot(x, vy, color='r', label='Vy')
        ax2.plot(x, pos_x, color='g', label='Position x')
        ax2.plot(x, set_point_x, color='b', label='Set Point x')
        ax3.plot(x, pos_y, color='g', label='Position y')
        ax3.plot(x, set_point_y, color='b', label='Set Point y')
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Speed(m/s)')
        ax2.set_xlabel('Time(s)')
        ax2.set_ylabel('Position x (cm)')
        ax3.set_xlabel('Time(s)')
        ax3.set_ylabel('Position y(cm)')
        ax.grid(True)
        ax.autoscale(True)
        ax.legend()
        ax2.grid(True)
        ax2.autoscale(True)
        ax2.legend()
        ax3.grid(True)
        ax3.autoscale(True)
        ax3.legend()
    plt.show()
    pass


def plot_drone_data(drone, plot_type):
    if plot_type == "all":
        x = drone.store_data['Time']
        y1 = drone.store_data['Vx']
        y2 = drone.store_data['Vy']
    if plot_type == "forward":
        x = drone.store_data['Delta Time F']
        y1 = drone.store_data['Vx']
        y2 = drone.store_data['Vy']
    if plot_type == "backward":
        x = drone.store_data['Delta Time B']
        y1 = drone.store_data['Vx']
        y2 = drone.store_data['Vy']
    if plot_type == "right":
        x = drone.store_data['Delta Time R']
        y1 = drone.store_data['Vx']
        y2 = drone.store_data['Vy']
    if plot_type == "left":
        x = drone.store_data['Delta Time L']
        y1 = drone.store_data['Vx']
        y2 = drone.store_data['Vy']
    x_pos = drone.store_data['Position x']
    y_pos = drone.store_data['Position y']
    # for pos in drone.store_data['Position']:
    #     x_pos.append(pos.x)
    #     y_pos.append(pos.y)
    fig, ax = plt.subplots(1, 1)
    fig2, ax2 = plt.subplots(1, 1)
    ax.clear()
    fig.suptitle(f'Drone {drone.id} Data')
    ax.plot(x, y1, color='g', label='Vx')
    ax.plot(x, y2, color='r', label='Vy')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Speed(m/s)')
    ax.grid(True)
    ax.autoscale(True)
    ax.legend()
    ax2.clear()
    fig2.suptitle(f'Drone {drone.id} Pos')
    ax2.plot(x, x_pos, color='g', label='Pos x')
    ax2.plot(x, y_pos, color='r', label='Pos y')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Position (cm)')
    ax2.grid(True)
    ax2.autoscale(True)
    ax2.legend()
    plt.show()


def signal_plot(drone):
    x = drone.store_data['Time']
    ex = drone.store_data['ex']
    ey = drone.store_data['ey']
    ux = drone.store_data['Control Signal x']
    uy = drone.store_data['Control Signal y']
    pos_x = drone.store_data['Position x']
    pos_y = drone.store_data['Position y']
    sp_x = drone.store_data['Set Point x']
    sp_y = drone.store_data['Set Point y']
    vx = drone.store_data['Vx']
    vy = drone.store_data['Vy']
    input_vx = drone.store_data['Input vx']
    input_vy = drone.store_data['Input vy']
    dist = drone.store_data['Distance to target']
    fig, [ax, ax2] = plt.subplots(2, 1)
    fig2, [ax3, ax4, axDist] = plt.subplots(3, 1)
    fig3, ax5 = plt.subplots(1, 1)
    all_ax = [ax, ax2, ax3, ax4, ax5, axDist]
    for axis in all_ax:
        axis.clear()
        axis.set_xlabel('Time(s)')
        if all_ax.index(axis) != 4:
            axis.set_ylabel('Position (cm)')
        else:
            axis.set_ylabel('Speed (m/s)')
    fig.suptitle('Signal Data')
    fig2.suptitle('Position Data')
    fig3.suptitle('Speed Data')
    ax.plot(x, ex, color='g', label='ex')
    ax.plot(x, ey, color='b', label='ey')
    ax2.plot(x, ux, color='g', label='Control Signal x')
    ax2.plot(x, uy, color='b', label='Control Signal y')
    ax3.plot(x, pos_x, color='g', label='Pos x')
    ax3.plot(x, sp_x, color='b', label='Set Point x')
    ax4.plot(x, pos_y, color='g', label='Pos y')
    ax4.plot(x, sp_y, color='b', label='Set Point y')
    axDist.plot(x, dist, color='b', label='Distance to target')
    ax5.plot(x, vx, color='g', label='Vx (m/s)')
    ax5.plot(x, vy, color='r', label='Vy (m/s)')
    ax5.plot(x, input_vx, color='b', label='input Vx (m/s)')
    ax5.plot(x, input_vy, color='y', label='input Vy (m/s)')
    for axes in all_ax:
        axes.grid(True)
        # gca = axes.gca()
        axes.set_ylim([0, 2])
        # axes.set_xlim([0, 10])
        # axes.autoscale(True)
        axes.legend()

    plt.show()
    pass


def lf_plot(lf_data):
    t = lf_data.lf_store_data['Time']
    leader_id = lf_data.lf_store_data['Leader id']
    lead_pos_x = lf_data.lf_store_data['Leader pos x']
    lead_pos_y = lf_data.lf_store_data['Leader pos y']
    traject_point_x = lf_data.lf_store_data['Trajectory point x']
    traject_point_y = lf_data.lf_store_data['Trajectory point y']
    foll_1_pos_x = lf_data.lf_store_data['Follower 1 pos x']
    foll_1_pos_y = lf_data.lf_store_data['Follower 1 pos y']
    foll_2_pos_x = lf_data.lf_store_data['Follower 2 pos x']
    foll_2_pos_y = lf_data.lf_store_data['Follower 2 pos y']
    l_to_foll_1 = lf_data.lf_store_data['L dist to foll 1']
    l_to_foll_2 = lf_data.lf_store_data['L dist to foll 2']
    between_foll = lf_data.lf_store_data['Between followers']
    limit_dist = lf_data.lf_store_data['Limit distance']
    drone_1_battery = lf_data.lf_store_data['Drone 1 battery']
    drone_2_battery = lf_data.lf_store_data['Drone 2 battery']
    drone_3_battery = lf_data.lf_store_data['Drone 3 battery']
    fig, [ax, ax2] = plt.subplots(2, 1)
    fig2, [ax3, ax4] = plt.subplots(2, 1)
    fig3, ax5 = plt.subplots(1, 1)
    fig4, [axId, axBattery] = plt.subplots(2, 1)
    all_ax = [ax, ax2, ax3, ax4, ax5, axId, axBattery]
    ax.plot(t, lead_pos_x, color='b', label='leader x pos')
    ax.plot(t, traject_point_x, color='y', label='Trajectory set point x')
    ax2.plot(t, lead_pos_y, color='b', label='leader y pos')
    ax2.plot(t, traject_point_y, color='y', label='Trajectory set point y')
    ax3.plot(t, foll_1_pos_x, color='g', label='Follower 1 x pos')
    ax4.plot(t, foll_1_pos_y, color='g', label='Follower 1 y pos')
    ax3.plot(t, foll_2_pos_x, color='m', label='Follower 2 x pos')
    ax4.plot(t, foll_2_pos_y, color='m', label='Follower 2 y pos')
    ax3.plot(t, traject_point_x, color='y', label='Trajectory set point x')
    ax4.plot(t, traject_point_y, color='y', label='Trajectory set point y')
    ax5.plot(t, l_to_foll_1, color='b', label='Leader to follower 1 distance')
    ax5.plot(t, l_to_foll_2, color='g', label='Leader to follower 2 distance')
    ax5.plot(t, between_foll, color='m', label='Distance between followers')
    ax5.plot(t, limit_dist, color='r', label='Limit distance between drones')
    axId.plot(t, leader_id, color='b', label='Leader Id')
    axBattery.plot(t, drone_1_battery, color='b', label='Drone 1 Battery')
    axBattery.plot(t, drone_2_battery, color='g', label='Drone 2 Battery')
    axBattery.plot(t, drone_3_battery, color='m', label='Drone 3 Battery')

    for axis in all_ax:
        axis.set_xlabel('Time (s)')
        axis.grid(True)
        axis.autoscale(True)
        axis.legend()
    ax.set_ylabel('Position x(cm)')
    ax2.set_ylabel('Position y(cm)')
    ax3.set_ylabel('Position x(cm)')
    ax4.set_ylabel('Position y(cm)')
    ax5.set_ylabel('Distance (cm)')
    axId.set_ylabel('Id')
    axBattery.set_ylabel('Battery (%)')
    fig.suptitle('Leader Position')
    fig2.suptitle('Follower Position')
    fig3.suptitle('Distance between drones')
    fig4.suptitle('Drone id and battery')
    plt.show()
    pass

import numpy as np
from matplotlib import pyplot as plt
# %matplotlib inline

from matplotlib import animation

from pyplot3d.uav import Uav
from pyplot3d.utils import ypr_to_R
import pandas as pd



def animate_quadcopter_history(times, x, R):
    plt.style.use('seaborn')

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    space_lim = (0, 2)
    arm_length = 0.3  # in meters
    uav_plot = Uav(ax, arm_length,tilt_angle=np.deg2rad(30)) # TODO: change hardcode
    def update_plot(i):
        
        # ax.cla()
            
        uav_plot.draw_at(x[:, i], R[:, :, i])
        
        # These limits must be set manually since we use
        # a different axis frame configuration than the
        # one matplotlib uses.
        
        ax.set_xlim(space_lim)
        ax.set_ylim(space_lim)
        ax.set_zlim((0, space_lim[1]))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_box_aspect([1, 1, 1])
        # ax.invert_zaxis()
        ax.set_title("Quadcopter Animation (Time: {0:.3f} s)".format(times[i]))
    
    # animate @ 1/desired_interval hz, with data from every step_size * dt
    animate_interval = 50
    step_size = 25
    steps = len(times)
    ind = [i * step_size for i in range(steps // step_size)]
    ani = animation.FuncAnimation(fig, update_plot,frames=ind,interval=animate_interval);
    plt.show()

# Load your data 
data = pd.read_csv('quadcopter_data.csv')
times = data['Time'].values

posHistory = data[['PosX', 'PosY', 'PosZ']].values
attHistory = data[['Yaw','Pitch', 'Roll']].values
x = posHistory.T
steps = len(times)

R = np.zeros((3, 3, steps))
for i in range(steps):
    ypr = attHistory[i,:]
    R[:, :, i] = ypr_to_R(ypr, degrees=False)


# TODO: change constants

animate_quadcopter_history(times, x, R)
from ipywidgets import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.spatial.transform import Rotation as R

def plot_gesture_log(log_frames, idx):

    

    n_frames = log_frames.shape[0]
    n_cols = log_frames.shape[1]

    # Define initial parameters
    init_frequency = 0
    
    # Create the figure and the lines that we will manipulate    
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches    
    fig = plt.figure(figsize=(800*px, 900*px))
    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        
    # see https://www.w3.org/TR/webxr-hand-input-1/
    index_offset = 7
    rh_offset = 25*7
    f_right_thumb, = ax1.plot([log_frames[idx,rh_offset + index_offset * 0 + 0], log_frames[idx,rh_offset + index_offset * 1 + 0], log_frames[idx,rh_offset + index_offset * 2 + 0], log_frames[idx,rh_offset + index_offset * 3 + 0], log_frames[idx,rh_offset + index_offset * 4 + 0]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 1], log_frames[idx,rh_offset + index_offset * 1 + 1], log_frames[idx,rh_offset + index_offset * 2 + 1], log_frames[idx,rh_offset + index_offset * 3 + 1], log_frames[idx,rh_offset + index_offset * 4 + 1]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 2], log_frames[idx,rh_offset + index_offset * 1 + 2], log_frames[idx,rh_offset + index_offset * 2 + 2], log_frames[idx,rh_offset + index_offset * 3 + 2], log_frames[idx,rh_offset + index_offset * 4 + 2]],
                              'o-', lw=2)
    f_right_index, = ax1.plot([log_frames[idx,rh_offset + index_offset * 0 + 0], log_frames[idx,rh_offset + index_offset * 5 + 0], log_frames[idx,rh_offset + index_offset * 6 + 0], log_frames[idx,rh_offset + index_offset * 7 + 0], log_frames[idx,rh_offset + index_offset * 8 + 0], log_frames[idx,rh_offset + index_offset * 9 + 0]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 1], log_frames[idx,rh_offset + index_offset * 5 + 1], log_frames[idx,rh_offset + index_offset * 6 + 1], log_frames[idx,rh_offset + index_offset * 7 + 1], log_frames[idx,rh_offset + index_offset * 8 + 1], log_frames[idx,rh_offset + index_offset * 9 + 1]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 2], log_frames[idx,rh_offset + index_offset * 5 + 2], log_frames[idx,rh_offset + index_offset * 6 + 2], log_frames[idx,rh_offset + index_offset * 7 + 2], log_frames[idx,rh_offset + index_offset * 8 + 2], log_frames[idx,rh_offset + index_offset * 9 + 2]],
                              'o-', lw=2)
    f_right_middle, = ax1.plot([log_frames[idx,rh_offset + index_offset * 0 + 0], log_frames[idx,rh_offset + index_offset * 10 + 0], log_frames[idx,rh_offset + index_offset * 11 + 0], log_frames[idx,rh_offset + index_offset * 12 + 0], log_frames[idx,rh_offset + index_offset * 13 + 0], log_frames[idx,rh_offset + index_offset * 14 + 0]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 1], log_frames[idx,rh_offset + index_offset * 10 + 1], log_frames[idx,rh_offset + index_offset * 11 + 1], log_frames[idx,rh_offset + index_offset * 12 + 1], log_frames[idx,rh_offset + index_offset * 13 + 1], log_frames[idx,rh_offset + index_offset * 14 + 1]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 2], log_frames[idx,rh_offset + index_offset * 10 + 2], log_frames[idx,rh_offset + index_offset * 11 + 2], log_frames[idx,rh_offset + index_offset * 12 + 2], log_frames[idx,rh_offset + index_offset * 13 + 2], log_frames[idx,rh_offset + index_offset * 14 + 2]],
                              'o-', lw=2)
    f_right_ring, = ax1.plot([log_frames[idx,rh_offset + index_offset * 0 + 0], log_frames[idx,rh_offset + index_offset * 15 + 0], log_frames[idx,rh_offset + index_offset * 16 + 0], log_frames[idx,rh_offset + index_offset * 17 + 0], log_frames[idx,rh_offset + index_offset * 18 + 0], log_frames[idx,rh_offset + index_offset * 19 + 0]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 1], log_frames[idx,rh_offset + index_offset * 15 + 1], log_frames[idx,rh_offset + index_offset * 16 + 1], log_frames[idx,rh_offset + index_offset * 17 + 1], log_frames[idx,rh_offset + index_offset * 18 + 1], log_frames[idx,rh_offset + index_offset * 19 + 1]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 2], log_frames[idx,rh_offset + index_offset * 15 + 2], log_frames[idx,rh_offset + index_offset * 16 + 2], log_frames[idx,rh_offset + index_offset * 17 + 2], log_frames[idx,rh_offset + index_offset * 18 + 2], log_frames[idx,rh_offset + index_offset * 19 + 2]],
                              'o-', lw=2)
    f_right_pinky, = ax1.plot([log_frames[idx,rh_offset + index_offset * 0 + 0], log_frames[idx,rh_offset + index_offset * 20 + 0], log_frames[idx,rh_offset + index_offset * 21 + 0], log_frames[idx,rh_offset + index_offset * 22 + 0], log_frames[idx,rh_offset + index_offset * 23 + 0], log_frames[idx,rh_offset + index_offset * 24 + 0]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 1], log_frames[idx,rh_offset + index_offset * 20 + 1], log_frames[idx,rh_offset + index_offset * 21 + 1], log_frames[idx,rh_offset + index_offset * 22 + 1], log_frames[idx,rh_offset + index_offset * 23 + 1], log_frames[idx,rh_offset + index_offset * 24 + 1]],
                              [log_frames[idx,rh_offset + index_offset * 0 + 2], log_frames[idx,rh_offset + index_offset * 20 + 2], log_frames[idx,rh_offset + index_offset * 21 + 2], log_frames[idx,rh_offset + index_offset * 22 + 2], log_frames[idx,rh_offset + index_offset * 23 + 2], log_frames[idx,rh_offset + index_offset * 24 + 2]],
                              'o-', lw=2)    
    
    
    def plot_joint_frames(ax, joint_poses):
        f_joint_frames = []
        for i in range(25):
            pose = joint_poses[i * 7 : i * 7 + 7]
            r = R.from_quat([pose[3], pose[4], pose[5], pose[6]])
            unit_vector_scale = 0.01
            unit_vectors = [[0, 0, 0],[unit_vector_scale, 0, 0],[0, unit_vector_scale, 0],[0, 0, unit_vector_scale]]
            unit_vectors_trans = r.apply(unit_vectors)
            # ax.plot( [unit_vectors_trans[0,0], unit_vectors_trans[1,0]],
            #          [unit_vectors_trans[0,1], unit_vectors_trans[1,1]],
            #          [unit_vectors_trans[0,2], unit_vectors_trans[1,2]])
            f_x, = ax.plot( [unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[1,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[1,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[1,2] + pose[2]], 'r-')
            f_y, = ax.plot( [unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[2,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[2,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[2,2] + pose[2]], 'g-')
            f_z, = ax.plot( [unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[3,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[3,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[3,2] + pose[2]], 'b-')
            
            f_joint_frames.append(f_x)
            f_joint_frames.append(f_y)
            f_joint_frames.append(f_z)
            
        return f_joint_frames

    f_joint_frames = plot_joint_frames(ax1, log_frames[idx,rh_offset:rh_offset+25*7])

    # Axes
    #axis_offset = [0.0, 0.75, -0.25]
    log_frames_means = np.mean(log_frames,axis=0)
    axis_offset = [log_frames_means[rh_offset + index_offset * 0 + 0],log_frames_means[rh_offset + index_offset * 0 + 1],log_frames_means[rh_offset + index_offset * 0 + 2]]
    scale = 0.15
    ax1.axis('equal')
    ax1.set_xlim([scale*-1 + axis_offset[0], scale*1 + axis_offset[0]])
    ax1.set_xlabel('x-axis')
    ax1.set_ylim([scale*-1 + axis_offset[1], scale*1 + axis_offset[1]])
    ax1.set_ylabel('y-axis')
    ax1.set_zlim([scale*-1 + axis_offset[2], scale*1 + axis_offset[2]])
    ax1.set_zlabel('z-axis')
    ax1.view_init(elev=45, azim=-45)
    
    axcolor = 'lightgoldenrodyellow'

    plt.show()
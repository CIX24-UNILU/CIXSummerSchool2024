import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.spatial.transform import Rotation as R

def plotDataBuffer(filename):

    data_buffer = np.loadtxt(filename, skiprows=1, delimiter=',')

    n_frames = data_buffer.shape[0]
    n_cols = data_buffer.shape[1]

    # Define initial parameters
    init_frequency = 0
    
    # Create the figure and the lines that we will manipulate    
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches    
    fig = plt.figure(figsize=(800*px, 900*px))
    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
    idx = 0
    
    # see https://www.w3.org/TR/webxr-hand-input-1/
    index_offset = 7
    rh_offset = 25*7
    f_right_thumb, = ax1.plot([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 1 + 0], data_buffer[idx,rh_offset + index_offset * 2 + 0], data_buffer[idx,rh_offset + index_offset * 3 + 0], data_buffer[idx,rh_offset + index_offset * 4 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 1 + 1], data_buffer[idx,rh_offset + index_offset * 2 + 1], data_buffer[idx,rh_offset + index_offset * 3 + 1], data_buffer[idx,rh_offset + index_offset * 4 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 1 + 2], data_buffer[idx,rh_offset + index_offset * 2 + 2], data_buffer[idx,rh_offset + index_offset * 3 + 2], data_buffer[idx,rh_offset + index_offset * 4 + 2]],
                              'o-', lw=2)
    f_right_index, = ax1.plot([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 5 + 0], data_buffer[idx,rh_offset + index_offset * 6 + 0], data_buffer[idx,rh_offset + index_offset * 7 + 0], data_buffer[idx,rh_offset + index_offset * 8 + 0], data_buffer[idx,rh_offset + index_offset * 9 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 5 + 1], data_buffer[idx,rh_offset + index_offset * 6 + 1], data_buffer[idx,rh_offset + index_offset * 7 + 1], data_buffer[idx,rh_offset + index_offset * 8 + 1], data_buffer[idx,rh_offset + index_offset * 9 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 5 + 2], data_buffer[idx,rh_offset + index_offset * 6 + 2], data_buffer[idx,rh_offset + index_offset * 7 + 2], data_buffer[idx,rh_offset + index_offset * 8 + 2], data_buffer[idx,rh_offset + index_offset * 9 + 2]],
                              'o-', lw=2)
    f_right_middle, = ax1.plot([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 10 + 0], data_buffer[idx,rh_offset + index_offset * 11 + 0], data_buffer[idx,rh_offset + index_offset * 12 + 0], data_buffer[idx,rh_offset + index_offset * 13 + 0], data_buffer[idx,rh_offset + index_offset * 14 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 10 + 1], data_buffer[idx,rh_offset + index_offset * 11 + 1], data_buffer[idx,rh_offset + index_offset * 12 + 1], data_buffer[idx,rh_offset + index_offset * 13 + 1], data_buffer[idx,rh_offset + index_offset * 14 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 10 + 2], data_buffer[idx,rh_offset + index_offset * 11 + 2], data_buffer[idx,rh_offset + index_offset * 12 + 2], data_buffer[idx,rh_offset + index_offset * 13 + 2], data_buffer[idx,rh_offset + index_offset * 14 + 2]],
                              'o-', lw=2)
    f_right_ring, = ax1.plot([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 15 + 0], data_buffer[idx,rh_offset + index_offset * 16 + 0], data_buffer[idx,rh_offset + index_offset * 17 + 0], data_buffer[idx,rh_offset + index_offset * 18 + 0], data_buffer[idx,rh_offset + index_offset * 19 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 15 + 1], data_buffer[idx,rh_offset + index_offset * 16 + 1], data_buffer[idx,rh_offset + index_offset * 17 + 1], data_buffer[idx,rh_offset + index_offset * 18 + 1], data_buffer[idx,rh_offset + index_offset * 19 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 15 + 2], data_buffer[idx,rh_offset + index_offset * 16 + 2], data_buffer[idx,rh_offset + index_offset * 17 + 2], data_buffer[idx,rh_offset + index_offset * 18 + 2], data_buffer[idx,rh_offset + index_offset * 19 + 2]],
                              'o-', lw=2)
    f_right_pinky, = ax1.plot([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 20 + 0], data_buffer[idx,rh_offset + index_offset * 21 + 0], data_buffer[idx,rh_offset + index_offset * 22 + 0], data_buffer[idx,rh_offset + index_offset * 23 + 0], data_buffer[idx,rh_offset + index_offset * 24 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 20 + 1], data_buffer[idx,rh_offset + index_offset * 21 + 1], data_buffer[idx,rh_offset + index_offset * 22 + 1], data_buffer[idx,rh_offset + index_offset * 23 + 1], data_buffer[idx,rh_offset + index_offset * 24 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 20 + 2], data_buffer[idx,rh_offset + index_offset * 21 + 2], data_buffer[idx,rh_offset + index_offset * 22 + 2], data_buffer[idx,rh_offset + index_offset * 23 + 2], data_buffer[idx,rh_offset + index_offset * 24 + 2]],
                              'o-', lw=2)    
    
    
    def plot_joint_frames(ax, joint_poses):
        f_joint_frames = []
        for i in range(25):
            pose = joint_poses[i * 7 : i * 7 + 7]
            r = R.from_quat([pose[3], pose[4], pose[5], pose[6]])
            unit_vector_scale = 0.01
            unit_vectors = [[0, 0, 0],[unit_vector_scale, 0, 0],[0, unit_vector_scale, 0],[0, 0, unit_vector_scale]]
            unit_vectors_trans = r.apply(unit_vectors)
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

    f_joint_frames = plot_joint_frames(ax1, data_buffer[idx,rh_offset:rh_offset+25*7])

    # Axes
    #axis_offset = [0.0, 0.75, -0.25]
    data_buffer_means = np.mean(data_buffer,axis=0)
    axis_offset = [data_buffer_means[rh_offset + index_offset * 0 + 0],data_buffer_means[rh_offset + index_offset * 0 + 1],data_buffer_means[rh_offset + index_offset * 0 + 2]]
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

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.1, bottom=0.25)

    # Make a horizontal slider to control the sample index.
    axsample = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    sample_idx_slider = Slider(
        ax=axsample,
        label='Frame Index',
        valmin=0,
        valmax=data_buffer.shape[0]-1,
        valinit=init_frequency,
        valfmt="%i",
    )

    # The function to be called anytime a slider's value changes
    def update(val):
        idx = int(val)
        f_right_thumb.set_data_3d([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 1 + 0], data_buffer[idx,rh_offset + index_offset * 2 + 0], data_buffer[idx,rh_offset + index_offset * 3 + 0], data_buffer[idx,rh_offset + index_offset * 4 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 1 + 1], data_buffer[idx,rh_offset + index_offset * 2 + 1], data_buffer[idx,rh_offset + index_offset * 3 + 1], data_buffer[idx,rh_offset + index_offset * 4 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 1 + 2], data_buffer[idx,rh_offset + index_offset * 2 + 2], data_buffer[idx,rh_offset + index_offset * 3 + 2], data_buffer[idx,rh_offset + index_offset * 4 + 2]])
        
        f_right_index.set_data_3d([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 5 + 0], data_buffer[idx,rh_offset + index_offset * 6 + 0], data_buffer[idx,rh_offset + index_offset * 7 + 0], data_buffer[idx,rh_offset + index_offset * 8 + 0], data_buffer[idx,rh_offset + index_offset * 9 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 5 + 1], data_buffer[idx,rh_offset + index_offset * 6 + 1], data_buffer[idx,rh_offset + index_offset * 7 + 1], data_buffer[idx,rh_offset + index_offset * 8 + 1], data_buffer[idx,rh_offset + index_offset * 9 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 5 + 2], data_buffer[idx,rh_offset + index_offset * 6 + 2], data_buffer[idx,rh_offset + index_offset * 7 + 2], data_buffer[idx,rh_offset + index_offset * 8 + 2], data_buffer[idx,rh_offset + index_offset * 9 + 2]])
        
        f_right_middle.set_data_3d([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 10 + 0], data_buffer[idx,rh_offset + index_offset * 11 + 0], data_buffer[idx,rh_offset + index_offset * 12 + 0], data_buffer[idx,rh_offset + index_offset * 13 + 0], data_buffer[idx,rh_offset + index_offset * 14 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 10 + 1], data_buffer[idx,rh_offset + index_offset * 11 + 1], data_buffer[idx,rh_offset + index_offset * 12 + 1], data_buffer[idx,rh_offset + index_offset * 13 + 1], data_buffer[idx,rh_offset + index_offset * 14 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 10 + 2], data_buffer[idx,rh_offset + index_offset * 11 + 2], data_buffer[idx,rh_offset + index_offset * 12 + 2], data_buffer[idx,rh_offset + index_offset * 13 + 2], data_buffer[idx,rh_offset + index_offset * 14 + 2]])
        
        f_right_ring.set_data_3d([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 15 + 0], data_buffer[idx,rh_offset + index_offset * 16 + 0], data_buffer[idx,rh_offset + index_offset * 17 + 0], data_buffer[idx,rh_offset + index_offset * 18 + 0], data_buffer[idx,rh_offset + index_offset * 19 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 15 + 1], data_buffer[idx,rh_offset + index_offset * 16 + 1], data_buffer[idx,rh_offset + index_offset * 17 + 1], data_buffer[idx,rh_offset + index_offset * 18 + 1], data_buffer[idx,rh_offset + index_offset * 19 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 15 + 2], data_buffer[idx,rh_offset + index_offset * 16 + 2], data_buffer[idx,rh_offset + index_offset * 17 + 2], data_buffer[idx,rh_offset + index_offset * 18 + 2], data_buffer[idx,rh_offset + index_offset * 19 + 2]])
        
        f_right_pinky.set_data_3d([data_buffer[idx,rh_offset + index_offset * 0 + 0], data_buffer[idx,rh_offset + index_offset * 20 + 0], data_buffer[idx,rh_offset + index_offset * 21 + 0], data_buffer[idx,rh_offset + index_offset * 22 + 0], data_buffer[idx,rh_offset + index_offset * 23 + 0], data_buffer[idx,rh_offset + index_offset * 24 + 0]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 1], data_buffer[idx,rh_offset + index_offset * 20 + 1], data_buffer[idx,rh_offset + index_offset * 21 + 1], data_buffer[idx,rh_offset + index_offset * 22 + 1], data_buffer[idx,rh_offset + index_offset * 23 + 1], data_buffer[idx,rh_offset + index_offset * 24 + 1]],
                              [data_buffer[idx,rh_offset + index_offset * 0 + 2], data_buffer[idx,rh_offset + index_offset * 20 + 2], data_buffer[idx,rh_offset + index_offset * 21 + 2], data_buffer[idx,rh_offset + index_offset * 22 + 2], data_buffer[idx,rh_offset + index_offset * 23 + 2], data_buffer[idx,rh_offset + index_offset * 24 + 2]])
        
        update_joint_frames(f_joint_frames, data_buffer[idx,rh_offset:])

        fig.canvas.draw_idle()




    def update_joint_frames(joint_frame_handles, joint_poses):
        for i in range(25):
            pose = joint_poses[i * 7 : i * 7 + 7]
            r = R.from_quat([pose[3], pose[4], pose[5], pose[6]])
            unit_vector_scale = 0.01
            unit_vectors = [[0, 0, 0],[unit_vector_scale, 0, 0],[0, unit_vector_scale, 0],[0, 0, unit_vector_scale]]
            unit_vectors_trans = r.apply(unit_vectors)
            joint_frame_handles[i*3 + 0].set_data_3d([unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[1,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[1,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[1,2] + pose[2]])
            
            joint_frame_handles[i*3 + 1].set_data_3d( [unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[2,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[2,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[2,2] + pose[2]])

            joint_frame_handles[i*3 + 2].set_data_3d( [unit_vectors_trans[0,0] + pose[0], unit_vectors_trans[3,0] + pose[0]],
                    [unit_vectors_trans[0,1] + pose[1], unit_vectors_trans[3,1] + pose[1]],
                    [unit_vectors_trans[0,2] + pose[2], unit_vectors_trans[3,2] + pose[2]])

        

    # register the update function with each slider
    sample_idx_slider.on_changed(update)

    plt.show()


#plotDataBuffer('scissors_log_example.csv')
#plotDataBuffer('paper_log_example.csv')
plotDataBuffer('rock_log_example.csv')
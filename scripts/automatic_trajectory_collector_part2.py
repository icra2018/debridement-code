"""
Run this after running the automatic trajectory collector. This gets the data 
in the format I need for my old code. I need this separate for data cleaning, etc.

(c) September 2017 by Daniel Seita
"""

import cv2
import numpy as np
import os
import pickle
import sys
import utilities as utils
from autolab.data_collector import DataCollector
from dvrk.robot import *
np.set_printoptions(suppress=True)


def is_this_clean(val, theta_l2r):
    """ Note: I return the distance as the second tuple element, or -1 if irrelevant. """
    frame, l_center, r_center = val
    if (l_center == (-1,-1) or r_center == (-1,-1)):
        return False, -1
    left_pt_hom = np.array([l_center[0], l_center[1], 1])
    right_pt = left_pt_hom.dot(theta_l2r)
    dist = np.sqrt( (r_center[0]-right_pt[0])**2 + (r_center[1]-right_pt[1])**2 )
    if dist >= 12:
        return False, dist
    return True, dist


def filter_points_in_results(camera_map, directory):
    """ Iterate through all trajectories to concatenate the data.

    Stuff to filter:

    (1) Both a left and a right camera must actually exist. In my code I set invalid
        ones to have (-1,-1) so that's one case.

    (2) Another case would be if the left-right transformation doesn't look good. Do
        this from the perspective of the _left_ camera since it's usually better. In
        other words, given pixels from the left camera, if we map them over to the
        right camera, the right camera's pixels should be roughly where we expect. If
        it's completely off, something's wrong. Use `camera_map` for this! I use a 
        distance of 12 for this, since that's about a 1mm difference in the workspace.

    The result is one list of all the cleaned up data. Each element in the list should
    consist of a tuple of `(frame,l_center,r_center)` where `frame` is really the pose.
    """
    clean_data = []
    traj_dirs = sorted([dd for dd in os.listdir(directory) if 'traj_' in dd])
    print("len(traj_dirs): {}".format(traj_dirs))

    for td in traj_dirs:
        traj_data = pickle.load(open(directory+td+'/traj_poses_list.p', 'r'))
        assert len(traj_data) > 1 and len(traj_data[0]) == 3
        num_td = 0
        
        for (i, val) in enumerate(traj_data):
            isclean, dist = is_this_clean(val, camera_map)
            if isclean:
                print("{}  CLEAN : {} (dist {})".format(str(i).zfill(3), val, dist)) # Clean
                clean_data.append(val)
                num_td += 1
            else:
                print("{}        : {} (dist {})".format(str(i).zfill(3), val, dist)) # Dirty

        print("dir {}, len(raw_data) {}, len(clean_data) {}\n".format(td, len(traj_data), num_td))

    print("\nNow returning clean data w/{} elements".format(len(clean_data)))
    return clean_data


def process_data(clean_data):
    """ Processes the filtered, cleaned data into something I can use in my old code.

    TODO
    """
    pass


if __name__ == "__main__":
    """
    First, load in the parameters file, only for getting the left to right camera
    pixel correspondence. It's OK to use version 00 for this since these points should
    not change among different versions, since it's just matching circle centers.

    Then, clean up the data using various heuristics (see the method documentation for
    detals). Then process it into a form that I need, and save it
    """
    params = pickle.load(open('config/mapping_results/params_matrices_v00.p', 'r'))
    directory = 'traj_collector/'

    clean_data = filter_points_in_results(params['theta_l2r'], directory)
    #proc_data = process_data(clean_data)
    #pickle.dump(proc_data, open('', 'w'))

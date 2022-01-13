# from FBL_libraries import FiveBarLinkage_lib_R07 as FBL_lib
import numpy as np
from math import floor
from matplotlib import pyplot as plt
from matplotlib import animation
# import matplotlib.patches as patches



'''
one function with a type argument? (e.g. standard, lissajous...)
    but then what would other args look like?

    (type, params) ??

should drive trace be a class?
    then have a method for each type of drive trace...
'''
def get_drive_trace_():

    return


def get_float_trace_pos(drive1, drive2, r1, r2):
    '''
    2CI solver where centers of circles are given by the two drive arrays (size 2xn)
    '''

    d_sqrd = (drive1[0,:]-drive2[0,:])**2 + (drive1[1,:]-drive2[1,:])**2
    d = d_sqrd**0.5

    a = (d_sqrd + r1**2 - r2**2)/(2*d)

    h = (r1**2 - a**2)**0.5

    x = drive1[0,:] + a/d*(drive1[0,:]-drive2[0,:]) - h/d*(drive1[1,:]-drive2[1,:])
    y = drive1[1,:] + a/d*(drive1[1,:]-drive2[1,:]) + h/d*(drive1[0,:]-drive2[0,:])

    return np.array([x,y])

def get_float_trace_neg(drive1, drive2, r1, r2):
    '''
    2CI solver where centers of circles are given by the two drive arrays (size 2xn)
    '''

    d_sqrd = (drive1[0,:]-drive2[0,:])**2 + (drive1[1,:]-drive2[1,:])**2
    d = d_sqrd**0.5

    a = (d_sqrd + r1**2 - r2**2)/(2*d)

    h = (r1**2 - a**2)**0.5

    x = drive1[0,:] + a/d*(drive1[0,:]-drive2[0,:]) + h/d*(drive1[1,:]-drive2[1,:])
    y = drive1[1,:] + a/d*(drive1[1,:]-drive2[1,:]) - h/d*(drive1[0,:]-drive2[0,:])

    return np.array([x,y])

def get_coupler_trace(drive, float, k, theta):
    '''
    for each timestep:
        - make a vector from drive point to float point
        - rotate by theta and scale by k
            - theta=0: k scales along the floating link
                - k=1: should return the float trace exactly
                - k=.5: halfway point of floating link
        - result is the coupler point
    '''

    link = float - drive # vector of link from driving joint to end effector

    # rotation matrix
    rot_mat = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])

    # first component is the rotated and scaled unit vector
    # second comopnent shifts so that vector starts at the drive points
    coupler_trace = k*np.dot(rot_mat,link) + drive

    return coupler_trace

def get_smear(trace, spin_center, omega):

    return smear

def get_spirograph(smear, spin_center, omega, num_lobes):
    n = smear.shape[1]
    angular_width = omega*n

    rot_mat = np.array([[np.cos(angular_width), -np.sin(angular_width)],[np.sin(angular_width), np.cos(angular_width)]])

    spirograph = []
    for lobe in range(num_lobes):
        smear = np.dot(rot_mat,smear)
        this_lobe = smear + spin_center
        spirograph.append(this_lobe)

    return spirograph

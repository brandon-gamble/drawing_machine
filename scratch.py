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

class drive_trace():
    def __init__(self):
        return
    def circle(r,center,starting_theta,omega,n):
        '''
        r               float       radius
        center          2x1 array   center location, (x;y)
        starting_theta  float       first theta value
        omega           float       angular velocity
        n               int         number of points

        e.g.
        n = 2000
        c = np.array([[0],[0]])
        drive_trace.circle(2,c,0,0.12,n)
        '''

        # initialize output vector with zeros
        circle = np.zeros([2,n])

        # vector of time values
        t_vec = np.linspace(0,n-1,n)
        t_vec = t_vec + starting_theta # offset by starting theta

        circle[0,:] = r*np.cos(omega*t_vec) # x values
        circle[1,:] = r*np.sin(omega*t_vec) # y values
        circle = circle + center # shift by circle center
        return circle

    def lissajous(a, b, omega, delta, n):
        # https://mathworld.wolfram.com/LissajousCurve.html

        drive = np.zeros([2,n])

        t_vec = np.linspace(0,n-1,n)

        drive[0,:] = a*np.sin(omega*t_vec + delta)
        drive[1,:] = b*np.sin(t_vec)

        return drive

def get_drive_trace(r,c,omega,n):
    # makes a circle 

    drive = np.zeros([2,n])
    drive[0,:] = r*np.cos(omega * np.linspace(0,n-1,n))
    drive[1,:] = r*np.sin(omega * np.linspace(0,n-1,n))
    drive = drive + c
    return drive

def get_2ci_pos(drive1, drive2, r1, r2):
    '''
    2CI solver where centers of circles are given by the two drive arrays (size 2xn)
    http://www.ambrsoft.com/TrigoCalc/Circles2/circle2intersection/CircleCircleIntersection.htm

    drive   2xn array   drive array
    r       float       radius of link
    '''

    d_sqrd = (drive1[0,:]-drive2[0,:])**2 + (drive1[1,:]-drive2[1,:])**2
    d = d_sqrd**0.5

    A = 1/4*((d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(-d+r1+r2))**0.5

    var1 = (r1**2-r2**2)/2/d_sqrd
    var2 = 2*A/d_sqrd

    x = (drive1[0,:]+drive2[0,:])/2 + (drive2[0,:]-drive1[0,:])*var1 + (drive1[1,:]-drive2[1,:])*var2
    y = (drive1[1,:]+drive2[1,:])/2 + (drive2[1,:]-drive1[1,:])*var1 - (drive1[0,:]-drive2[0,:])*var2

    return np.array([x,y])

def get_2ci_neg(drive1, drive2, r1, r2):
    '''
    2CI solver where centers of circles are given by the two drive arrays (size 2xn)
    '''

    d_sqrd = (drive1[0,:]-drive2[0,:])**2 + (drive1[1,:]-drive2[1,:])**2
    d = d_sqrd**0.5

    A = 1/4*((d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(-d+r1+r2))**0.5

    var1 = (r1**2-r2**2)/2/d_sqrd
    var2 = 2*A/d_sqrd

    x = (drive1[0,:]+drive2[0,:])/2 + (drive2[0,:]-drive1[0,:])*var1 - (drive1[1,:]-drive2[1,:])*var2
    y = (drive1[1,:]+drive2[1,:])/2 + (drive2[1,:]-drive1[1,:])*var1 + (drive1[0,:]-drive2[0,:])*var2

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
    n = smear.shape[1]          # smear is 2xn, so shape[1] is how many points
    angular_width = omega*n     # total angle occupied by smear

    # rotation matrix
    rot_mat = np.array([[np.cos(angular_width), -np.sin(angular_width)],[np.sin(angular_width), np.cos(angular_width)]])

    spirograph = []
    for lobe in range(num_lobes):
        smear = np.dot(rot_mat,smear)
        this_lobe = smear + spin_center
        spirograph.append(this_lobe)

    return spirograph

def check_clearance(c1,arm1,c2,arm2):
    # c takes form (x,y,r)

    d = np.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

    if arm1+arm2 >= c1[2]+c2[2]+d:
        check = True
    else:
        check = False

    return check

if __name__ == "__main__":

    '''
    1   simple 5bl trace test using 2ci
    '''

    test = 1

    if test == 1:
        n = 2000
        c = np.array([[0],[0]])
        drive1 = get_drive_trace(2,c,.12,n)

        c = np.array([[9],[0]])
        drive2 = get_drive_trace(3,c,.11,n)

        float_p = get_2ci_pos(drive1, drive2, 10,10)
        float_n = get_2ci_neg(drive1, drive2, 10,10)

        plt.plot(drive1[0,:],drive1[1,:])
        plt.plot(drive2[0,:],drive2[1,:])
        plt.plot(float_p[0,:],float_p[1,:])
        plt.plot(float_n[0,:],float_n[1,:])
        plt.show()

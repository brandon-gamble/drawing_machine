'''
Collection of activation functions for populating nodes.


'''

def test(val1,weight1,val2,weight2):
    return val1*weight1 + val2*weight2

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

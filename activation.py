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

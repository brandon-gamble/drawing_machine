import graph
import scratch
import numpy as np
from matplotlib import pyplot as plt

'''
1   integrating graph and scratch to solve a node encoded 5bl
2   using graph to solve pantograph and plot machine by hand
3   solve pantograph and plot machine using graph.draw_machine()
4   what happens when clearance is <0?
        graph gets blown out
5   clearance correction on 5bl

'''


test = 5

if test == 1:

    n = 2000
    c = np.array([[0],[0]]) # circle center
    drive1 = scratch.get_drive_trace(2,c,.12,n) # circular drive trace

    c = np.array([[9],[0]]) # circle center
    drive2 = scratch.get_drive_trace(3,c,.11,n) # circular drive trace

    a = graph.node(None) # root node (spiro end effector)
    b = graph.node(drive1) # driving node 1
    c = graph.node(drive2) # drivign node 2

    # connect a to b with link length 10
    a.left_parent = b
    a.left_weight = 10

    # connect a to c with link length 10
    a.right_parent = c
    a.right_weight = 10

    # compute end effector location
    graph.postorder_populate_w_clearance_check(a)

    # plot
    plt.plot(a.value[0,:],a.value[1,:])
    plt.show()


elif test == 2:
    '''
    gets a math error ( invalid value in sqrt) in scratch.py line 61:
    A = 1/4*((d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(-d+r1+r2))**0.5

    but well produces the pantograph effect of enlarging the pre-image

    '''

    #####################
    # setup input nodes #
    #####################

    n = 600

    fixed_pt = np.zeros([2,n]) # fixed point of pantograph

    c = np.array([[1],[0]]) # center of circle
    pre_image = scratch.drive_trace.circle(0.1,c,.02,n) # circle as pre-image

    #####################
    # instantiate nodes #
    #####################

    a = graph.node(None)
    b = graph.node(None)
    c = graph.node(None)
    d = graph.node(pre_image)
    e = graph.node(None)
    f = graph.node(fixed_pt)

    ###########################
    # build graph connections #
    ###########################

    a.left_parent = c
    a.left_weight = 2
    a.right_parent = b
    a.right_weight = 1

    b.left_parent = c
    b.left_weight = 1
    b.right_parent = d
    b.right_weight = 1

    c.left_parent = f
    c.left_weight = 2
    c.right_parent = e
    c.right_weight = 1

    e.left_parent = f
    e.left_weight = 1
    e.right_parent = d
    e.right_weight = 1

    ##################
    # populate graph #
    ##################
    graph.postorder_populate(a)

    ################
    #     plot     #
    ################

    # input
    plt.plot(f.value[0,0],f.value[1,0]) # fixed point
    plt.plot(d.value[0,:],d.value[1,:]) # pre-image

    # joints
    plt.plot(e.value[0,:],e.value[1,:])
    plt.plot(c.value[0,:],c.value[1,:])
    plt.plot(b.value[0,:],b.value[1,:])

    # image
    plt.plot(a.value[0,:],a.value[1,:])

    # machine
    long_x = [a.value[0,0],c.value[0,0],f.value[0,0]]
    long_y = [a.value[1,0],c.value[1,0],f.value[1,0]]
    long_arms = np.array([long_x,long_y])

    short_x = [b.value[0,0],d.value[0,0],e.value[0,0]]
    short_y = [b.value[1,0],d.value[1,0],e.value[1,0]]
    short_arms = np.array([short_x,short_y])

    plt.plot(long_x,long_y,'b--')

    plt.plot(short_x,short_y,'b--')

    plt.show()

elif test == 3:
    '''
    gets a math error ( invalid value in sqrt) in scratch.py line 61:
    A = 1/4*((d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(-d+r1+r2))**0.5

    but well produces the pantograph effect of enlarging the pre-image

    '''

    #####################
    # setup input nodes #
    #####################

    n = 600

    fixed_pt = np.zeros([2,n]) # fixed point of pantograph

    c = np.array([[1],[0]]) # center of circle
    pre_image = scratch.drive_trace.circle(0.1,c,.02,n) # circle as pre-image

    #####################
    # instantiate nodes #
    #####################

    a = graph.node(None)
    b = graph.node(None)
    c = graph.node(None)
    d = graph.node(pre_image)
    e = graph.node(None)
    f = graph.node(fixed_pt)

    ###########################
    # build graph connections #
    ###########################

    a.left_parent = c
    a.left_weight = 2
    a.right_parent = b
    a.right_weight = 1

    b.left_parent = c
    b.left_weight = 1
    b.right_parent = d
    b.right_weight = 1

    c.left_parent = f
    c.left_weight = 2
    c.right_parent = e
    c.right_weight = 1

    e.left_parent = f
    e.left_weight = 1
    e.right_parent = d
    e.right_weight = 1

    ##################
    # populate graph #
    ##################
    graph.postorder_populate(a)

    #####################
    #     plot paths    #
    #####################

    # input
    plt.plot(f.value[0,0],f.value[1,0]) # fixed point
    plt.plot(d.value[0,:],d.value[1,:]) # pre-image

    # joints
    plt.plot(e.value[0,:],e.value[1,:])
    plt.plot(c.value[0,:],c.value[1,:])
    plt.plot(b.value[0,:],b.value[1,:])

    # image
    plt.plot(a.value[0,:],a.value[1,:])

    ########################
    #     plot machine     #
    ########################
    graph.plot_machine(a,0)
    plt.show()

elif test == 4:

    n = 5000
    c = np.array([[0],[0]]) # circle center
    drive1 = scratch.get_drive_trace(2,c,.12,n) # circular drive trace

    c = np.array([[9],[0]]) # circle center
    drive2 = scratch.get_drive_trace(3,c,.11,n) # circular drive trace

    a = graph.node(None) # root node (spiro end effector)
    b = graph.node(drive1) # driving node 1
    c = graph.node(drive2) # drivign node 2

    # connect a to b with link length 10
    a.left_parent = b
    a.left_weight = 6

    # connect a to c with link length 10
    a.right_parent = c
    a.right_weight = 5

    # compute end effector location
    graph.postorder_populate(a)

    # plot
    plt.plot(a.value[0,:],a.value[1,:])
    graph.plot_machine(a,0)
    plt.show()

elif test == 5:
    n = 5000
    c = np.array([[0],[0]]) # circle center
    drive1 = scratch.get_drive_trace(2,c,.12,n) # circular drive trace

    c = np.array([[9],[0]]) # circle center
    drive2 = scratch.get_drive_trace(3,c,.11,n) # circular drive trace

    a = graph.node(None) # root node (spiro end effector)
    b = graph.node(drive1) # driving node 1
    c = graph.node(drive2) # drivign node 2

    # connect a to b with link length 10
    a.left_parent = b
    a.left_weight = 6

    # connect a to c with link length 10
    a.right_parent = c
    a.right_weight = 3

    # compute end effector location
    graph.postorder_populate_w_clearance_check(a)

    # plot
    plt.plot(a.value[0,:],a.value[1,:])
    graph.plot_machine(a,0)
    plt.show()

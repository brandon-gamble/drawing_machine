import graph
import scratch
import numpy as np
from matplotlib import pyplot as plt

'''
1   integrating graph and scratch to solve a node encoded 5bl

'''

test = 1


if test == 1:

    n = 2000
    c = np.array([[0],[0]])
    drive1 = scratch.get_drive_trace(2,c,.12,n)

    c = np.array([[9],[0]])
    drive2 = scratch.get_drive_trace(3,c,.11,n)

    a = graph.node(None) # root node
    b = graph.node(drive1)
    c = graph.node(drive2)

    a.left_child = b
    a.left_weight = 10

    a.right_child = c
    a.right_weight = 10

    graph.postorder_populate_w_clearance_check(a)

    plt.plot(a.value[0,:],a.value[1,:])
    plt.show()

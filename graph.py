import numpy as np
import smallestenclosingcircle

# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python

# activation function
def activation(v1,w1,v2,w2):
    return v1*w1 + v2*w2

import scratch
def activation(v1,w1,v2,w2):
    return scratch.get_2ci_pos(v1,v2,w1,w2)

#########
# GRAPH #
#########




########
# TREE #
########
class node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.left_weight = 1
        self.right_child = None
        self.right_weight = 1

    # def insert_left(self, value):
    #     if self.left_child == None:
    #         self.left_child = node(value)
    #     else:
    #         new_node = node(value)
    #         new_node.left_child = self.left_child
    #         self.left_child = new_node
    #
    # def insert_right(self, value):
    #     if self.right_child == None:
    #         self.right_child = node(value)
    #     else:
    #         new_node = node(value)
    #         new_node.right_child = self.right_child
    #         self.right_child = new_node

    def populate_node(self):
        self.value = activation(self.left_child.value,self.left_weight, self.right_child.value,self.right_weight)

def preorder(root):
    if root:
        print(root.value)
        preorder(root.left_child)
        preorder(root.right_child)

def inorder(root):
    if root:
        inorder(root.left_child)
        print(root.value)
        inorder(root.right_child)
def postorder(root):
    if root:
        postorder(root.left_child)
        postorder(root.right_child)
        print(root.value)

def postorder_populate(root):
    try:
        # true if no value
        is_empty = not root.value
    except:
        # if value exists and is array, we can't interpet "not root.value"
        # so we must forcefully say that is_empty = False
        is_empty = False

    if is_empty: # if node is empty, enter loop to populate
        postorder_populate(root.left_child)
        postorder_populate(root.right_child)
        root.populate_node()

def postorder_populate_w_clearance_check(root):
    try:
        # true if no value
        is_empty = not root.value
    except:
        # if value exists and is array, we can't interpet "not root.value"
        # so we must forcefully say that is_empty = False
        is_empty = False

    if is_empty: # if node is empty, enter loop to populate
        postorder_populate_w_clearance_check(root.left_child)
        postorder_populate_w_clearance_check(root.right_child)

        # make bounding circles for traces of parent nodes
        # circle format is list with (x,y,r)
        circ_left = smallestenclosingcircle.make_circle(root.left_child.value.transpose())
        circ_right = smallestenclosingcircle.make_circle(root.right_child.value.transpose())

        d = np.sqrt((circ_left[0]-circ_right[0])**2+(circ_left[0]-circ_right[0])**2)

        clearance = (root.left_weight + root.right_weight) - (circ_left[2] + d + circ_right[2])
        if clearance >= 0:
            root.populate_node()
        else:
            print('clearance is %f. not long enough' % clearance)


if __name__ == "__main__":

    '''
    1   simple tree, manual populate
    2   more complex tree, traversing
    3   same tree as 2, but trying to autopopulate with post order
    '''

    test = 3

    if test == 1:
        '''
        sample graph to solve

         [A]
         |  \
         |  (1)
         |    \
        (3)   [B]
         |   /   \
         | (2)   (1)
         | /       \
        [C]        [D]
                   / \
                 (1) (.5)
                 /     \
               [E]    [F]

        input:
            C = 2
            E = 1
            F = 4
        propagation:
            A = 13
            B = 7
            D = 3

        '''

        #################################################
        #               solve using "tree"              #
        # technically not tree bc c connects to a and b #
        #################################################

        a = node(None)
        b = node(None)
        c = node(2)
        d = node(None)
        e = node(1)
        f = node(4)

        a.left_child = c
        a.left_weight = 3
        a.right_child = b
        a.right_weight = 1

        b.left_child = c
        b.left_weight = 2
        b.right_child = d
        b.right_weight = 1

        d.left_child = e
        d.left_weight = 1
        d.right_child = f
        d.right_weight = 0.5

        d.populate_node()
        b.populate_node()
        a.populate_node()

        print('inputs:')
        print('c: %d' % c.value) # 2
        print('e: %d' % e.value) # 1
        print('f: %d' % f.value) # 4

        print('outputs')
        print('a: %d' % a.value) # 13
        print('b: %d' % b.value) # 7
        print('d: %d' % d.value) # 3


    elif test == 2:

        a = node(1)
        b = node(2)
        c = node(3)
        d = node(4)
        e = node(5)
        f = node(6)
        g = node(7)
        h = node(8)
        i = node(9)
        j = node(10)
        k = node(11)
        l = node(12)
        m = node(13)

        a.left_child = c
        a.right_child = b
        b.left_child = c
        b.right_child = d
        c.left_child = e
        c.right_child = f
        d.left_child = h
        d.right_child = g
        g.left_child = h
        g.right_child = i
        h.left_child = j
        h.right_child = k
        j.left_child = l
        j.right_child = m

        print('preorder')
        preorder(a)

        print('inorder')
        inorder(a)

        print('postorder')
        postorder(a)

    elif test == 3:

        # input nodes
        f = node(6)
        i = node(4)
        k = node(3)
        l = node(1)
        m = node(2)
        e = node(5)

        # intermediate/output nodes
        a = node(None)
        b = node(None)
        c = node(None)
        d = node(None)
        g = node(None)
        h = node(None)
        j = node(None)

        a.left_child = c
        a.right_child = b
        b.left_child = c
        b.right_child = d
        c.left_child = e
        c.right_child = f
        d.left_child = h
        d.right_child = g
        g.left_child = h
        g.right_child = i
        h.left_child = j
        h.right_child = k
        j.left_child = l
        j.right_child = m

        print('postorder (unpopulated):')
        postorder(a)

        print('postorder populating...')
        postorder_populate(a)

        print('postorder (following postorder population scheme)')
        postorder(a)

        # desired order of postorder is:
        # 5,6,11, 5,6,11, 1,2,3, 3,6,1, 2,3,3, 6,4,10 ,16,27,38
        # which corresponds to:
        # e,f,c, e,f,c, l,m,j, k,h,l ,m,j,k, h,i,g, d,b,a

#################################################
#               solve using graph               #
#################################################

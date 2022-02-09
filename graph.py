import numpy as np
import smallestenclosingcircle
import activation as act_fns
from matplotlib import pyplot as plt

# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python

# # activation function
# def activation(v1,w1,v2,w2):
#     return v1*w1 + v2*w2
#
# import scratch
# def activation(v1,w1,v2,w2):
#     return scratch.get_2ci_pos(v1,v2,w1,w2)

class node:
    '''
    typical tree notation is that parent is root and each parent as two children.
    however, for case of linkage solver, tree is traversed from leaves back up to root.
    as we traverse, every node is the solution of two inputs. as such, we will use
    the opposite of typical tree notation, instead saying that every child has exactly
    two parents. to compute the child, we solve an activation function with the parents as inputs
    '''
    def __init__(self, value):
        # initalize Node
        # for empty node, initialize as "node.(None)"
        self.value = value
        self.left_parent = None  # initialize without data in parents
        self.right_parent = None
        self.left_weight = 1    # initailize with weight of 1
        self.right_weight = 1
        self.activation_function = act_fns.get_2ci_pos # default activation is get_2ci_pos

    # def insert_left(self, value):
    #     if self.left_parent == None:
    #         self.left_parent = node(value)
    #     else:
    #         new_node = node(value)
    #         new_node.left_parent = self.left_parent
    #         self.left_parent = new_node
    #
    # def insert_right(self, value):
    #     if self.right_parent == None:
    #         self.right_parent = node(value)
    #     else:
    #         new_node = node(value)
    #         new_node.right_parent = self.right_parent
    #         self.right_parent = new_node

    def populate_node(self):
        # populate node with activation function
        self.value = self.activation_function(self.left_parent.value, self.right_parent.value, self.left_weight, self.right_weight)

def preorder(root):
    # print root values by preorder algorithm
    if root:
        print(root.value)
        preorder(root.left_parent)
        preorder(root.right_parent)

def inorder(root):
    # print root values by inorder algorithm
    if root:
        inorder(root.left_parent)
        print(root.value)
        inorder(root.right_parent)

def postorder(root):
    # print root values by postorder algorithm
    # postorder, as it turns out, guarantees that we start with leaves and traverse
    # up tree to root. this order is sufficient for populating tree data from inputs
    # at leaves to output at root
    if root:
        postorder(root.left_parent)
        postorder(root.right_parent)
        print(root.value)

def postorder_populate(root):
    '''
    our goal is to populate the tree starting with the leaves (input parent nodes)
    and traversing all the way to the root. postorder traversal algorithm will give
    us the correct order. at each node during the traversal, we need to check if it
    contains data in its value attribute. if the value is None, then it has not been
    populated and we must compute its value from its parents.

    therefore, what we need is a flag for whether node.value is empty (None) or
    full (contains an array).

    if a node is empty, then "not node.value" returns True
    if a node is full, then "not node.value" returns an error:
        "truth value of array with more than one element is ambiguous"
        suggestion is to use any(), but NoneType doesn't have any() attribute.

    we are in a bit of a catch22.

    to solve this, we put evaluation in a try/except
    if there is no value, then the try block executes and is_empty is True
    if there is a value, then the try block will fail and go to the except block,
    where we mark the flag false.

    finally, we start our recursive loop using "if is_empty: ..."

    this loop is the same as the postorder algorithm but instead of printing
    each node when we get to it, we populate it
    '''
    try:
        # true if no value
        is_empty = not root.value
    except:
        # if value exists and is array, we can't interpet "not root.value"
        # so we must forcefully say that is_empty = False
        is_empty = False

    if is_empty: # if node is empty, enter loop to populate
        postorder_populate(root.left_parent)
        postorder_populate(root.right_parent)
        root.populate_node()

def postorder_populate_w_clearance_check(root):
    '''
    our goal is to populate the tree starting with the leaves (input parent nodes)
    and traversing all the way to the root. postorder traversal algorithm will give
    us the correct order. at each node during the traversal, we need to check if it
    contains data in its value attribute. if the value is None, then it has not been
    populated and we must compute its value from its parents.

    therefore, what we need is a flag for whether node.value is empty (None) or
    full (contains an array).

    if a node is empty, then "not node.value" returns True
    if a node is full, then "not node.value" returns an error:
        "truth value of array with more than one element is ambiguous"
        suggestion is to use any(), but NoneType doesn't have any() attribute.

    we are in a bit of a catch22.

    to solve this, we put evaluation in a try/except
    if there is no value, then the try block executes and is_empty is True
    if there is a value, then the try block will fail and go to the except block,
    where we mark the flag false.

    finally, we start our recursive loop using "if is_empty: ..."

    this loop is the same as the postorder algorithm but instead of printing
    each node when we get to it, we populate it

    *** before populating, we check to make sure we have clearance for the linkage
    '''
    try:
        # true if no value
        is_empty = not root.value
    except:
        # if value exists and is array, we can't interpet "not root.value"
        # so we must forcefully say that is_empty = False
        is_empty = False

    if is_empty: # if node is empty, enter loop to populate
        postorder_populate_w_clearance_check(root.left_parent)
        postorder_populate_w_clearance_check(root.right_parent)

        # make bounding circles for traces of parent nodes
        # circle format is list with (x,y,r)
        circ_left = smallestenclosingcircle.make_circle(root.left_parent.value.transpose())
        circ_right = smallestenclosingcircle.make_circle(root.right_parent.value.transpose())

        # distance between parent circles
        d = np.sqrt((circ_left[0]-circ_right[0])**2+(circ_left[1]-circ_right[1])**2)

        # clerance of linkage
        clearance = (root.left_weight + root.right_weight) - (circ_left[2] + d + circ_right[2])
        if clearance < 0:
            print('correcting negative clearance (%f)' % clearance)
            # if we don't have clearance, then extend link lengths
            # note that to extend the link, we subtract a negative clearance -> i.e. add length
            root.left_weight = root.left_weight - clearance/2
            root.right_weight = root.right_weight - clearance/2

        root.populate_node()


def plot_parents(node,t):
    # ASSUMES THAT EVERYTHING IS POPULATED
    if node.left_parent and node.right_parent:
        x = [node.left_parent.value[0,t], node.value[0,t], node.right_parent.value[0,t]]
        y = [node.left_parent.value[1,t], node.value[1,t], node.right_parent.value[1,t]]
        plt.plot(x,y,'b')

def plot_machine(root,t):
    if root:
        plot_machine(root.left_parent,t)
        plot_machine(root.right_parent,t)
        plot_parents(root,t)

if __name__ == "__main__":

    '''
    1   simple tree, manual populate each node
    2   more complex tree, traversing
    3   same tree as 2, but trying to autopopulate with post order
    '''

    test = 1

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

        a.left_parent = c
        a.left_weight = 3
        a.right_parent = b
        a.right_weight = 1
        a.activation_function = act_fns.test

        b.left_parent = c
        b.left_weight = 2
        b.right_parent = d
        b.right_weight = 1
        b.activation_function = act_fns.test

        d.left_parent = e
        d.left_weight = 1
        d.right_parent = f
        d.right_weight = 0.5
        d.activation_function = act_fns.test

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

        a.left_parent = c
        a.right_parent = b
        b.left_parent = c
        b.right_parent = d
        c.left_parent = e
        c.right_parent = f
        d.left_parent = h
        d.right_parent = g
        g.left_parent = h
        g.right_parent = i
        h.left_parent = j
        h.right_parent = k
        j.left_parent = l
        j.right_parent = m

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

        a.left_parent = c
        a.right_parent = b
        a.activation_function = act_fns.test
        b.left_parent = c
        b.right_parent = d
        b.activation_function = act_fns.test
        c.left_parent = e
        c.right_parent = f
        c.activation_function = act_fns.test
        d.left_parent = h
        d.right_parent = g
        d.activation_function = act_fns.test
        g.left_parent = h
        g.right_parent = i
        g.activation_function = act_fns.test
        h.left_parent = j
        h.right_parent = k
        h.activation_function = act_fns.test
        j.left_parent = l
        j.right_parent = m
        j.activation_function = act_fns.test

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

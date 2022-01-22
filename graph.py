# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python

# activation function
def activation(v1,w1,v2,w2):
    return v1*w1 + v2*w2


#########
# GRAPH #
#########




########
# TREE #
########
class tree_node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.left_weight = 1
        self.right_child = None
        self.right_weight = 1

    # def insert_left(self, value):
    #     if self.left_child == None:
    #         self.left_child = tree_node(value)
    #     else:
    #         new_node = tree_node(value)
    #         new_node.left_child = self.left_child
    #         self.left_child = new_node
    #
    # def insert_right(self, value):
    #     if self.right_child == None:
    #         self.right_child = tree_node(value)
    #     else:
    #         new_node = tree_node(value)
    #         new_node.right_child = self.right_child
    #         self.right_child = new_node

    def populate_node(self):
        self.value = activation(self.left_child.value,self.left_weight, self.right_child.value,self.right_weight)

def preorder(node):
    if node:
        print(node.value)
        preorder(node.left_child)
        preorder(node.right_child)

def inorder(node):
    if node:
        inorder(node.left_child)
        print(node.value)
        inorder(node.right_child)
def postorder(node):
    if node:
        postorder(node.left_child)
        postorder(node.right_child)
        print(node.value)

def postorder_populate(node):
    if not node.value:
        postorder_populate(node.left_child)
        postorder_populate(node.right_child)
        node.populate_node()


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

        a = tree_node(None)
        b = tree_node(None)
        c = tree_node(2)
        d = tree_node(None)
        e = tree_node(1)
        f = tree_node(4)

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

        a = tree_node(1)
        b = tree_node(2)
        c = tree_node(3)
        d = tree_node(4)
        e = tree_node(5)
        f = tree_node(6)
        g = tree_node(7)
        h = tree_node(8)
        i = tree_node(9)
        j = tree_node(10)
        k = tree_node(11)
        l = tree_node(12)
        m = tree_node(13)

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
        f = tree_node(6)
        i = tree_node(4)
        k = tree_node(3)
        l = tree_node(1)
        m = tree_node(2)
        e = tree_node(5)

        # intermediate/output nodes
        a = tree_node(None)
        b = tree_node(None)
        c = tree_node(None)
        d = tree_node(None)
        g = tree_node(None)
        h = tree_node(None)
        j = tree_node(None)

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

# Generic Linkage Solver

## Inspiration
This project started in 2017 after I came across a video of a [Guilloche Drawing Machine](https://www.youtube.com/watch?v=BG9e06IWAxE). This machine was effectively a five bar linkage (5BL) and a spinning table. The motors of the linkage would rotate at constant speeds that varied slightly from one another. Simultaneously, the surface that the linkage drew on rotated. I was captivated by the complex and beautiful curves the machine was able to produce.
These Guilloche drawings were reminiscent of the spirograph drawings I would make as a kid, but far more intricate and organic.

The nature of physical pen plotters is that the drawing must be produced slowly, otherwise the pen will not draw a smooth, full line. As such, these Guilloche drawings take quite a bit of time to produce. Futhermore, they are defined by more than 10 parameters. I wanted a way to simulate the machine in order to quickly produce a drawing from a given set of parameters and explore how tuning different parameters affected the drawing.

I derived geometric equations that solved the forward kinematics of the 5BL and for many years used these equations to explore the 5BL, as implemented in [this repository](https://github.com/brandon-gamble/five_bar_linkage). I expanded my work and eventually wrote my [undergraduate thesis](https://scholarworks.uvm.edu/hcoltheses/406/) on the 5BL.

## Generic Linkage Graph Representation
Over the years, I had developed multiple implementations of my 5BL equations in both Matlab and Python, but I wasn't satisfied with their rigidity. Everything I had developed was strictly tied to the 5BL.
I was inspired by the drawings of other plotting machines - so called harmonographs, lissagraphs, pintographs, mesmergraphs, and so on. I wanted a way to simulate these other drawing machines without having to derive all of their respective kinematics from scratch.

In the fall of 2022, I was able to reframe my thinking of how to go about solving the kinematics of the 5BL in a way that expands to other linkages and drawing machines. What I realized is that parallel driven linkages have a common denominator in their kinematics: the two circle intersection (2CI) equation.
For the 5BL, it is easy to find the locations of the intermediate joints by their angle and link lengths with simple trig. Using the intermediate joint coordinates as the centers of two circles and the floating link lengths as their radii, the 2CI equation is solved to find the location of the end effector.

![5bl](/assets/diagrams/5bl.png)

Similarly, for a 4BL, the distal joint of the driving link is solved with simple trig. The end effector is found by solving the 2CI equation for circles centered at distal joint of the driving link and the fixed frame joint.

![4bl](/assets/diagrams/4bl.png)

How are these related? Well, first note that the 2CI solver accepts four arguments: two circle centers and two radii. When solving for a joint location, the radii are always the link lengths on either side of the joint, and the circle centers are the locations of the neighboring joints. For the 5BL, the neighboring joints were both found with trig. For the 4BL, one neighboring joint was found with trig and one neighboring joint was fixed.

For the purpose of drawing curves, we vectorize the 2CI approach, first solving for all the locations of each neighbor joint during the time we are interested in. This array of points is passed to the 2CI solver to produce an array of all the corresponding locations of the joint of interest. What does this input array look like? For the 5BL, both input arrays describe points around a circle. For the 4BL, one input array is points around a circle and the other is a fixed point.

My friend George helped me to realize that We can represent both of these graphically as, well, graphs with three nodes - two parents and one child. The input nodes contain circle center information, and the weights of the connections from parents to child represent the physical link lengths. Borrowing terminology from neural networks, the activation function for the child node is the 2CI equation.

![Node](/assets/diagrams/node.png)

In this way, both the 5BL and 4BL have the same graph representation. The difference between them is simply the values contained at the input nodes.
The beautiful thing about encoding a linkage this way is how it can be expanded.

### Expansions

#### Coupler
For example, what if instead of tracing the path of a joint, we want to trace a coupler curve? We can represent the coupler location as another node on our graph. Conveniently, we can describe the coupler location relative to its parent joints using two radii and solve for its location using the 2CI equation.

![Coupler node](/assets/diagrams/coupler.png)

#### Scissor 5BL
A more complex example is the scissor 5BL. To analyze this linkage, we can work backwards from the end effector to the input nodes. **A** is the child of **B** and **C**, so we draw edges connecting **A** to **B** and **C**.
**B** is the coupler of link **DF**, i.e., it is the child of **D** and **F**, so we draw edges connecting **B** to **D** and **F**.
Similarly, we draw edges connecting **C** to **D** and **E**.
Finally, **D** is the child of **E** and **F**, so we draw edges connecting **D** to **E** and **F**.

![scissor 5bl image](/assets/diagrams/scissor_5bl.png)

#### 4/5 BL
We have described the 4BL as a 2CI solution whose inputs are a circular path and a static point. When we trade the static point for another circular path, we get a 5BL. But what happens if we use other cyclic paths (non-circular) as the inputs to the 2CI solver? For example, What if the input paths are ellipses? Lissajous curves? 4BL traces? Using our node representation, it is incredibly simple to solve for the motions of complex machines, as well as generate graphs that may not have a physical analog linkage.
<< image with :
3 nodes (circle and point inputs) -> 4BL
3 nodes (circle and circle inputs) -> 5bl
7 nodes (4bl inputs) -> nested 4bl
3 nodes (ellipse inputs) -> archimedes trammel
3 nodes (lissajous) -> analog?? >>  **
** hypothesized that 5bl trace approaches lissajous for infinitely large radius... so maybe there is somewhat a physical analog?

#### Pantograph
The pantograph, a device with a history in manufacturing, can also be represented as a graph.
<< pantograph graph image >>
The standard pantograph scales an input path to an output path. It is typically configured to enlarge the input path, but can be used in the inverse to miniaturize the input path. While this functionality is not of interest to me in plotting organic curves, if the link lengths are modified such that the pantograph is no longer a parallelogram, then the input curve becomes warped. In this way, we can use a modified pantograph to distort curves and produce pleasing drawings.

## Graph Population
Given a graph representation of a linkage system, how do we go about solving for the curve drawn by the end effector?

Looking at these graphs, it is easy to see that we can start with the input nodes and populate their children. At successive iterations of population, we can always find an unpopulated child with two parents.

Let's look at the scissor 5BL example: if we try to populate **B** or **C** first, we will get an error because **D**, which is a parent to both **B** and **C**, is not yet populated. Instead, we must start at the input nodes **E** and **F** and populate **D**. With **D** populated, **B** and **C** can now be populated. Finally, **A** can be populated and the graph is fully populated.

The order of population is easy for a person to see, but how can we tell the computer to efficiently traverse the graph and populate each node starting from the input nodes and working toward the end effector node?

Well, it turns out that if our system doesn't have any couplers, i.e., all links are simple bars connected at their ends, our graph representation will be a binary tree. Furthermore, it will be a full binary tree, i.e., every node has exactly zero or two parents (note that we have inverted parent/child notation used in trees).
With this realization, I explored the common binary tree traversal algorithms, and found that the post-order traversal algorithm would guarantee that we start at the input nodes ("leaves") and traverse upward to the end effector ("root") one layer of the tree at a time.

Following the post-order traversal we can inspect each node along the way: if it is empty, populate it and move on, if it is populated, move on.
When we arrive at the end effector node, we will have populated every node in the graph.

It was a concern that the post-order traversal algorithm wouldn't work for graphs that include couplers, since these are strictly graphs and NOT binary trees. However, after more experimentation, it was found that this algorithm works not only for full binary trees, but also for the graphs we get as a result of introducing couplers to a linkage system. Very convenient!

We now have a way of representing a linkage system as a graph as well as an algorithm for traversing and populating the graph.  

<!-- ## Terminology
A 5BL has two driving links, two floating links, and a grounding link. For the purpose of drawing spirographs, the driving links are rotated at constant speeds and a complex curve is drawn. In order to be able to simulate more complex machines, the kinematics of the 5BL are broken into discrete steps.

The **drive point** is joint of the driving link and the floating link.
The **drive trace** is the path traced by the drive point.  For the 5BL, the drive traces are simply circles.

The **float point** is the joint between the floating links.
The **end-effector** is the location we place the virtual pen that draws our nice curves.
The **float trace** is the curve drawn when we place the end-effector at the float point.
The end-effector can be placed at other locations fixed relative to a floating link. When the end-effector is not at the float point, we call its path a **coupler trace**.

Note that the float trace is found geometrically as the intersection of two circles (2CI). The circles are centered at the drive points with radii equal to the lengths of the floating links. This is useful later on when we expand to more complicated drawing machines.

Finally, to go from the float trace to a **spirograph**, we must rotate the drawing surface while the 5BL draws the float trace. As the table rotates, the float trace is stretched, or smeared out in an arc. Note that the float trace is cyclic. We call the smeared image of the float trace a **smear trace**. To make computation faster, we only compute a single smear trace and then copy it as desired to create the final spirograph image.

## Drive Trace

As previously mentioned, the drive traces of a 5BL drawing machine are simply circles. By using drive traces that are non-circular, we can simulate more complex drawing machines and draw new spirograph images.

For example, the scissored 5BL (sometimes referred to as a pintograph) can actually be simulated without any additional math if we realize that the output of the machine is a float trace whose driving traces are coupler traces of the parent 5BL.

A four bar linkage can be analyzed as a float trace whose driving traces are a circle and a stationary point. We can thus simulate a four bar linkage and use the output as the driving trace for a spirograph. We can go further by using coupler traces of the four bar linkage as driving traces for a spirograph image.

The harmonograph is similar to a 5BL but the driving links get their energy from a pendulum rather than from a motor. As such, their motion damps out as the machine draws. This can be simulated by using inward spirals as drive traces.

Other ideas for modified drive traces are using polygons, helices, lissajous curves, or any other cyclic curve.

## Neural Net / Tree Encoding

If we abstract the above analysis one step further we can think of it as a tree-like structure. If can encode the drawing machine generically as a tree, then we can encode very complex machines as well as machines that may not have a physical analog.

The first step is to realize that the coupler trace of a link can actually be solved as a 2CI of the two joints of the link. Rather than defining the coupler point using polar coordinates wrt the two joints, we define is using its distances to each of the joints.

With the coupler trace reframed as a 2CI, we now have only one kinematic solver.

Now, how does a drawing machine translate to a tree structure? Take the simple 5bl, for example. The driving points are represented as input nodes, and the end effector is represented as an output node, which is connected to the two input nodes. The data held at each node is a set of points.
For an input node, the points are computed by an arbitrary driver function (could be a circle, as in the 5bl, or a more complicated curve such as a Lissajous curve).
Any node that is not an input has exactly two nodes connected to it, and its data is the set of points that are the 2CI solution to the sets of points of its connecting nodes.

if no coupler, then tree is full
if coupler, then not a tree bc we have a cycle

Notation to clarify:
upstream/downstream direction: think of upstream as the input side and info is propagated downstream as we solve each layer

parent/child direction: are parents the input nodes, since two parents have a child, or use tree terminology for parent as root and each parent has two children.

use tree terms or net terms? -->

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
For the 5BL, it is easy to find the locations of the intermediate joints by their angle and link lengths with simple trigonometry. Using the intermediate joint coordinates as the centers of two circles and the floating link lengths as their radii, the 2CI equation is solved to find the location of the end effector.

![5bl](/assets/diagrams/5bl.png)

Similarly, for a 4BL, the distal joint of the driving link is solved with simple trigonometry. The end effector is found by solving the 2CI equation for circles centered at distal joint of the driving link and the fixed frame joint.

![4bl](/assets/diagrams/4bl.png)

How are these related? Well, first note that the 2CI solver accepts four arguments: two circle centers and two radii. When solving for a joint location, the radii are always the link lengths on either side of the joint, and the circle centers are the locations of the neighboring joints. For the 5BL, the neighboring joints were both found with trigonometry. For the 4BL, one neighboring joint was found with trigonometry and one neighboring joint was fixed.

Again, at a single point in time the 2CI solver accepts two points (circle centers) and two radii. But we are interested in drawing curves over a long period of time. As such, we vectorize the 2CI approach, first solving for all the locations of each neighbor joint during the time we are interested in. This array of points is passed to the 2CI solver to produce an array of all the corresponding locations of the joint of interest. What does these input arrays look like? For the 5BL, both input arrays describe points around a circle, that is, the paths of each intermediate joint spinning continuously. For the 4BL, one input array is points around a circle and the other is a fixed point.

I was trying to find a good data structure to store a drawing machine given this new perspective. My [friend George](https://github.com/dairykillsme) suggested a tree structure. Technically, as we will see later on, some linkages can be represented by a binary tree and some linkages (spoiler alert: linkages with coupler curves) are technically not trees but instead graphs. It's similar to the square/rectangle scenario. Every tree is a graph but not every graph is a tree. That being said, the 4BL and 5BL can both be represented these graphically as, well, graphs. Both have three nodes - two parents and one child. The input nodes contain circle center information, and the weights of the connections from parents to child represent the physical link lengths. Borrowing terminology from neural networks, the activation function for the child node is the 2CI equation.

![Node](/assets/diagrams/node.png)

Notice that both the 4BL and 5BL only have two inputs leading to the end effector. The difference between them is simply the values contained at the input nodes. For the 4BL, one input contains points around a circle and one input contains a static point. For the 5BL, each input contains points around a circle. In this way, both the 5BL and 4BL have the same graph representation.

![4bl node](/assets/diagrams/4bl_node.png)
![5bl node](/assets/diagrams/5bl_node.png)

The beautiful thing about encoding a linkage this way is how it can be expanded to more complex linkages without having to derive any new kinematic equations. Furthermore, since we are free to pass any array of points as the value of an input node, we can create graphs that do not have a physical analog.

### Expansions

#### Coupler
What if instead of tracing the path of a joint, we want to trace a coupler curve? We can represent the coupler location as another node on our graph. Conveniently, we can describe the coupler location relative to its parent joints using two radii and solve for its location using the 2CI equation.

![Coupler node](/assets/diagrams/coupler.png)

#### Scissor 5BL
A more complex example is the scissor 5BL. To analyze this linkage, we can work backwards from the end effector to the input nodes. **A** is the child of **B** and **C**, so we draw edges connecting **A** to **B** and **C**.
**B** is the coupler of link **DF**, i.e., it is the child of **D** and **F**, so we draw edges connecting **B** to **D** and **F**.
Similarly, we draw edges connecting **C** to **D** and **E**.
Finally, **D** is the child of **E** and **F**, so we draw edges connecting **D** to **E** and **F**.

![scissor 5bl image](/assets/diagrams/scissor_5bl.png)

Here is an example plot of a scissor 5BL. All link lengths are symmetric, resulting in symmetric joint paths. The paths of E and F are pure circles.

![S5BL_eg1](/assets/drawings/scissor_5bl_01.JPG)

In this example, the links lengths are no longer symmetric. The result is quite interesting. The path of A alludes somewhat to a torus; the path of B has been stretched to be fatter; the paths of C and D have been stretched to be long and skinny.

![S5BL_eg1a](/assets/drawings/scissor_5bl_01_a.JPG)

<!-- #### 4/5 BL
We have described the 4BL as a 2CI solution whose inputs are a circular path and a static point. When we trade the static point for another circular path, we get a 5BL. But what happens if we use other cyclic paths (non-circular) as the inputs to the 2CI solver? For example, What if the input paths are ellipses (achieved with the trammel of Archimedes)? Lissajous curves (achieved with [sufficiently large 5BL](https://www.reddit.com/r/mathpics/comments/bta0az/i_found_that_pintograph_drawings_converge_to/))? 4BL traces? Using our node representation, it is incredibly simple to solve for the motions of complex machines, as well as generate graphs that may not have a physical analog linkage.

<< image with :
7 nodes (4bl inputs) -> nested 4bl
3 nodes (ellipse inputs) -> archimedes trammel
3 nodes (lissajous) -> analog?? >>  **
** hypothesized that 5bl trace approaches lissajous for infinitely large radius... so maybe there is somewhat a physical analog? -->

#### Pantograph
The pantograph, a device with a history in manufacturing, can also be easily represented as a graph.

The standard pantograph scales an input path to an output path. It is typically configured to enlarge the input path, but can be used in the inverse to miniaturize the input path. While this functionality is not of interest for plotting organic curves, the pantograph can still be of use: if the link lengths are modified such that the pantograph is no longer a parallelogram, then the output curve becomes both scaled _and_ warped. In this way, we can use a modified pantograph to distort curves and produce pleasing drawings.

![pantograph](/assets/diagrams/pantograph.png)


## Graph Population
Given a graph representation of a linkage system, how do we go about solving for the curve drawn by the end effector?

Looking at these graphs, it is easy to see that we can start with the input nodes and populate their immediate children. At successive iterations of population, we can always find an unpopulated child with two populated parents. We work our way from the input nodes all the way to the root node in this manner: finding an unpopulated node with two populated parents and populating that child.

![scisor 5bl graph](/assets/diagrams/scissor_5bl_graph.png)

Let's look at the scissor 5BL example: if we try to populate **B** or **C** first, we will get an error because **D**, which is a parent to both **B** and **C**, is not yet populated. Instead, we must start at the input nodes **E** and **F** and populate **D**. With **D** populated, **B** and **C** can now be populated. Finally, **A** can be populated and the graph is fully populated.

The order of population is easy for a person to see, but how can we tell the computer to efficiently traverse the graph and populate each node starting from the input nodes and working toward the end effector node?

Well, it turns out that if our system doesn't have any couplers, i.e., all links are simple bars connected at their ends, our graph representation will be a binary tree. Furthermore, it will be a full binary tree, i.e., every node has exactly zero or two parents (note that we have inverted parent/child notation used in trees).
With this realization, I explored the common binary tree traversal algorithms, and found that the post-order traversal algorithm would guarantee that we start at the input nodes ("leaves") and traverse upward to the end effector ("root") one layer of the tree at a time.

Following the post-order traversal we can inspect each node along the way: if it is empty, populate it and move on, if it is populated, move on.
When we arrive at the end effector node, we will have populated every node in the graph.

It was a concern that the post-order traversal algorithm wouldn't work for graphs that include couplers, since these are strictly graphs and NOT binary trees. However, after more experimentation, it was found that this algorithm works not only for full binary trees, but also for the graphs we get as a result of introducing couplers to a linkage system. Very convenient!

Looking at the scissor 5BL once more, which, as noted, is actually a graph, NOT a binary tree: the post-order traversal algorithm returns the order **EEF**-**DCE**-**FDE**-**BA**. Note that **E** and **F** are input nodes, so they are already populated. Removing them from our traversal order, we get: **DCDBA**. We can drop the second **D** since the first time we encounter it in the traversal we will populate it. So our order of population becomes: **DCBA**. Following this order for population, we get exactly what we intuitively worked out above. We start with **D**, as it is the child of the two input nodes. Then we can populate **C** and **B**, and finally populate **A**.

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

# Library for drawing machine based on five bar linkage

## Terminology
A five bar linkage has two driving links, two floating links, and a grounding link. For the purpose of drawing spirographs, the driving links are rotated at constant speeds and a complex curve is drawn. In order to be able to simulate more complex machines, the kinematics of the five bar linkage are broken into discrete steps.

The **drive point** is joint of the driving link and the floating link.
The **drive trace** is the path traced by the drive point.  For the five bar linkage, the drive traces are simply circles.

The **float point** is the joint between the floating links.
The **end-effector** is the location we place the virtual pen that draws our nice curves.
The **float trace** is the curve drawn when we place the end-effector at the float point.
The end-effector can be placed at other locations fixed relative to a floating link. When the end-effector is not at the float point, we call its path a **coupler trace**.

Note that the float trace is found geometrically as the intersection of two circles. The circles are centered at the drive points with radii equal to the lengths of the floating links. This is useful later on when we expand to more complicated drawing machines.

Finally, to go from the float trace to a **spirograph**, we must rotate the drawing surface while the five bar linkage draws the float trace. As the table rotates, the float trace is stretched, or smeared out in an arc. Note that the float trace is cyclic. We call the smeared image of the float trace a **smear trace**. To make computation faster, we only compute a single smear trace and then copy it as desired to create the final spirograph image.

## Drive Trace

As previously mentioned, the drive traces of a five bar linkage drawing machine are simply circles. By using drive traces that are non-circular, we can simulate more complex drawing machines and draw new spirograph images.

For example, the scissored five bar linkage (sometimes referred to as a pintograph) can actually be simulated without any additional math if we realize that the output of the machine is a float trace whose driving traces are coupler traces of the parent five bar linkage.

A four bar linkage can be analyzed as a float trace whose driving traces are a circle and a stationary point. We can thus simulate a four bar linkage and use the output as the driving trace for a spirograph. We can go further by using coupler traces of the four bar linkage as driving traces for a spirograph image.

The harmonograph is similar to a five bar linkage but the driving links get their energy from a pendulum rather than from a motor. As such, their motion damps out as the machine draws. This can be simulated by using inward spirals as drive traces. 

Other ideas for modified drive traces are using polygons, helices, lissajous curves, or any other cyclic curve.

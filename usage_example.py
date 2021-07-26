from cadquery import Workplane

Box = Workplane("XY").box(1, 1, 1, centered=(False, False, False))
Sphere = Workplane("XY").sphere(1)

# operation between Workplane
result = Box + Sphere # same as Box | Sphere, Box.union(Sphere)
result = Box & Sphere # same as Box.intersect(Sphere)
result = Box - Sphere # same as Box.cut(Sphere)


# show_object(result, options={"color":(0, 0, 255)})
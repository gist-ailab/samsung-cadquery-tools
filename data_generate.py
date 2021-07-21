import cadquery as cq
from cadquery import exporters
import numpy as np
import random
from os.path import join
# constant
COORDINATE_KEY = [
  "XY",
  "YZ",
  "XZ"
]
FACE_KEY = [
  ">Z", # Face farthest in the positive z dir
  "<Z", # Face farthest in the negative z dir
  ">Y",
  "<Y",
  ">X",
  "<X"
]

def create_circle_hole_shape(height = 10.0, width = 10.0, thickness = 10.0):
  # create box
  height = 10.0
  width = 10.0
  thickness = 10.0
  coordinate_key = random.choice(COORDINATE_KEY)
  face_key = random.choice(FACE_KEY)
  box = cq.Workplane(coordinate_key).box(height, width, thickness)

  # add hole
  diameter = np.random.uniform(min(height, width)/10, min(height, width)/3)
  depth = np.random.uniform(thickness/10, thickness/2)
  x = np.random.uniform((-height+diameter)/2 + 0.01, (height-diameter)/2 - 0.01)
  y = np.random.uniform((-width+diameter)/2 + 0.01, (width-diameter)/2 - 0.01)
  result = box.faces(face_key).workplane().center(x, y).hole(diameter=diameter, depth=depth)

  return result
# save to step file




if __name__=="__main__":
  total_data = 100
  data_name = "circle_hole_{}.step"
  for i in range(total_data):
    save_path = join("circle_hole_dataset", data_name.format(i))
    result = create_circle_hole_shape()
    exporters.export(result, save_path)

import cadquery as cq
from cadquery import Assembly, Vector, Location, Color, BoundBox, exporters
from cadquery.cq import Workplane
from cadquery.selectors import BoxSelector, InverseSelector
import numpy as np
import random
from os.path import join

from file_utils import check_and_create_dir
# constant
COORDINATE_KEY = [
  "XY",
  "YZ",
  "XZ"
]
FACE_KEY = [
  ">X",
  "<X",
  ">Y",
  "<Y",
  ">Z", # Face farthest in the positive z dir
  "<Z", # Face farthest in the negative z dir
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
  
  # get bbox of hole
  face_idx = FACE_KEY.index(face_key)
  hole_bbox = (box-result).val().BoundingBox()
  tolerance_idx = face_idx // 2
  tolerance = 0.001
  min_point = [hole_bbox.xmin, hole_bbox.ymin, hole_bbox.zmin]
  max_point = [hole_bbox.xmax, hole_bbox.ymax, hole_bbox.zmax]
  min_point[tolerance_idx]-=0.001
  max_point[tolerance_idx]+=0.001

  # set selector for hole and other faces
  hole_selector = BoxSelector(min_point, max_point)
  other_selector = InverseSelector(hole_selector)
  
  hole_faces = result.faces(hole_selector)
  other_faces = result.faces(other_selector)

  # make assembly and set color for hole and other faces
  assy = Assembly(hole_faces, name="hole", color=Color("red"))
  assy.add(other_faces, name="box", color=Color("black"))

  return assy



if __name__=="__main__":
  total_data = 100
  data_root = "labeled_circle_hole_dataset"
  data_name = "circle_hole_{}.step"
  
  check_and_create_dir(data_root)
  result = create_circle_hole_shape() # return Assembly

  for i in range(total_data):
    save_path = join(data_root, data_name.format(i))
    result.save(save_path, exportType='STEP')
  
  
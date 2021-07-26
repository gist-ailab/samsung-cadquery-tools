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



# hole parameter
BBOX_TOLERANCE = 0.001
SIDE_MARGIN = 0.05

# original box parameter
HEIGHT = 10.0
WIDTH = 10.0
THICKNESS = 10.0


def create_circle_hole_shape():
  # create box
  height = HEIGHT
  width = WIDTH
  thickness = THICKNESS
  coordinate_key = random.choice(COORDINATE_KEY)
  face_key = random.choice(FACE_KEY)
  box = cq.Workplane(coordinate_key).box(height, width, thickness)

  # add hole
  diameter = np.random.uniform(min(height, width)/10, min(height, width)/3)
  depth = np.random.uniform(thickness/10, thickness/2)
  x = np.random.uniform((-height+diameter)/2 + SIDE_MARGIN, (height-diameter)/2 - SIDE_MARGIN)
  y = np.random.uniform((-width+diameter)/2 + SIDE_MARGIN, (width-diameter)/2 - SIDE_MARGIN)
  result = box.faces(face_key).workplane().center(x, y).hole(diameter=diameter, depth=depth)
  
  # get bbox of hole
  face_idx = FACE_KEY.index(face_key)
  hole_bbox = (box-result).val().BoundingBox()
  tolerance_idx = face_idx // 2
  tolerance = BBOX_TOLERANCE
  
  min_point = [hole_bbox.xmin, hole_bbox.ymin, hole_bbox.zmin]
  max_point = [hole_bbox.xmax, hole_bbox.ymax, hole_bbox.zmax]
  for i in range(3):
    if i == tolerance_idx:
      min_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      max_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      continue
    min_point[i]-= tolerance
    max_point[i]+= tolerance
  

  # set selector for hole and other faces
  hole_selector = BoxSelector(min_point, max_point)
  other_selector = InverseSelector(hole_selector)
  
  hole_faces = result.faces(hole_selector)
  other_faces = result.faces(other_selector)

  # make assembly and set color for hole and other faces
  assy = Assembly(hole_faces, name="hole", color=Color("red"))
  assy.add(other_faces, name="box", color=Color("gray"))

  return assy

def create_rect_hole_shape():
  # create box
  height = HEIGHT
  width = WIDTH
  thickness = THICKNESS
  coordinate_key = random.choice(COORDINATE_KEY)
  face_key = random.choice(FACE_KEY)
  box = cq.Workplane(coordinate_key).box(height, width, thickness)

  # add hole
  hole_width = np.random.uniform(min(height, width)/10, min(height, width)/3)
  hole_height = np.random.uniform(min(height, width)/10, min(height, width)/3)
  depth = np.random.uniform(thickness/10, thickness/2)
  x = np.random.uniform((-height+hole_width)/2 + SIDE_MARGIN, (height-hole_width)/2 - SIDE_MARGIN)
  y = np.random.uniform((-width+hole_height)/2 + SIDE_MARGIN, (width-hole_height)/2 - SIDE_MARGIN)
  result = box.faces(face_key).workplane().center(x, y).rect(hole_width, hole_height).cutBlind(-depth)
  
  
  
  # get bbox of hole
  face_idx = FACE_KEY.index(face_key)
  hole_bbox = (box-result).val().BoundingBox()
  tolerance_idx = face_idx // 2
  tolerance = BBOX_TOLERANCE
  
  min_point = [hole_bbox.xmin, hole_bbox.ymin, hole_bbox.zmin]
  max_point = [hole_bbox.xmax, hole_bbox.ymax, hole_bbox.zmax]
  for i in range(3):
    if i == tolerance_idx:
      min_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      max_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      continue
    min_point[i]-= tolerance
    max_point[i]+= tolerance
  
  

  # set selector for hole and other faces
  hole_selector = BoxSelector(min_point, max_point)
  other_selector = InverseSelector(hole_selector)
  
  hole_faces = result.faces(hole_selector)
  other_faces = result.faces(other_selector)

  # make assembly and set color for hole and other faces
  assy = Assembly(hole_faces, name="hole", color=Color("red"))
  assy.add(other_faces, name="box", color=Color("gray"))

  return assy

def create_polygon_hole_shape(side_num=3):
  # create box
  height = HEIGHT
  width = WIDTH
  thickness = THICKNESS
  coordinate_key = random.choice(COORDINATE_KEY)
  face_key = random.choice(FACE_KEY)
  box = cq.Workplane(coordinate_key).box(height, width, thickness)

  # add hole
  diameter = np.random.uniform(min(height, width)/10, min(height, width)/3)
  depth = np.random.uniform(thickness/10, thickness/2)
  x = np.random.uniform((-height+diameter)/2 + SIDE_MARGIN, (height-diameter)/2 - SIDE_MARGIN)
  y = np.random.uniform((-width+diameter)/2 + SIDE_MARGIN, (width-diameter)/2 - SIDE_MARGIN)
  result = box.faces(face_key).workplane().center(x, y).polygon(side_num, diameter).cutBlind(-depth)
  
  # get bbox of hole
  face_idx = FACE_KEY.index(face_key)
  hole_bbox = (box-result).val().BoundingBox()
  tolerance_idx = face_idx // 2
  tolerance = BBOX_TOLERANCE
  
  min_point = [hole_bbox.xmin, hole_bbox.ymin, hole_bbox.zmin]
  max_point = [hole_bbox.xmax, hole_bbox.ymax, hole_bbox.zmax]
  for i in range(3):
    if i == tolerance_idx:
      min_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      max_point[i]+= tolerance*(-1)**(face_idx % 2 + 1)
      continue
    min_point[i]-= tolerance
    max_point[i]+= tolerance
  

  # set selector for hole and other faces
  hole_selector = BoxSelector(min_point, max_point)
  other_selector = InverseSelector(hole_selector)
  
  hole_faces = result.faces(hole_selector)
  other_faces = result.faces(other_selector)

  # make assembly and set color for hole and other faces
  assy = Assembly(hole_faces, name="hole", color=Color("red"))
  assy.add(other_faces, name="box", color=Color("gray"))

  return assy


if __name__=="__main__":
  total_data = 300
  
  hole_type_list = ["circle", "rect", "tri"]
  
  generator = {
    "circle": create_circle_hole_shape,
    "rect": create_rect_hole_shape,
    "tri": create_polygon_hole_shape
  }
  
  for hole_type in hole_type_list:
    data_root = "labeled_{}_hole_dataset".format(hole_type)
    data_name = "{}_hole_{}.step"
  
    check_and_create_dir(data_root)
    
    for i in range(total_data):
      result = generator[hole_type]() # return Assembly
      
      save_path = join(data_root, data_name.format(hole_type, i))
      result.save(save_path, exportType='STEP')
    
  
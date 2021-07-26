import os
from os.path import join, isfile, isdir, splitext
from os import listdir

from datetime import datetime
import logging
import shutil
import json
import pickle

# logger
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(level=logging.INFO)
    return logger



# os file functions
def get_file_list(path):
    file_list = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    return file_list

def get_dir_list(path):
    dir_list = [join(path, f) for f in listdir(path) if isdir(join(path, f))]

    return dir_list

def get_dir_name(path):
    return path.split("/")[-1]

def get_file_name(path):
    file_path, _ = splitext(path)
    return file_path.split("/")[-1]

def check_and_create_dir(dir_path):
    if not check_dir(dir_path):
        os.mkdir(dir_path)
        return True
    else:
        return False

def check_and_reset_dir(dir_path):
    if check_dir(dir_path):
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        return True
    else:
        os.mkdir(dir_path)
        return False

def check_dir(dir_path):
    return os.path.isdir(dir_path)

def check_file(file_path):
    return os.path.isfile(file_path)

def get_time_stamp():
    return datetime.timestamp(datetime.now())

def relative_path_to_abs_path(rel_path):
    os.path.abspath(rel_path)
    return os.path.abspath(rel_path)

def remove_file(file_path):
    os.remove(file_path)
def remove_dir(dir_path):
    shutil.rmtree(dir_path)

#============== Specific file format
class FileFormat: #TODO
    yaml_format = []
    json_format = []
    pickle_format = []
    
# yaml 
def save_dic_to_yaml(dic, yaml_path):
    import yaml
    with open(yaml_path, 'w') as y_file:
        _ = yaml.dump(dic, y_file, default_flow_style=False)

def load_yaml_to_dic(yaml_path):
    import yaml
    with open(yaml_path, 'r') as y_file:
        dic = yaml.load(y_file, Loader=yaml.FullLoader)
    return dic



# json
def load_json_to_dic(json_path):
    with open(json_path, 'r') as j_file:
        dic = json.load(j_file)
    return dic

def save_dic_to_json(dic, json_path):
    with open(json_path, 'w') as j_file:
        json.dump(dic, j_file, sort_keys=True, indent=4)



# pickle
def save_to_pickle(data, pickle_path):
    with open(pickle_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(pickle_path):
    with open(pickle_path, 'rb') as f:
        data = pickle.load(f)
    return data

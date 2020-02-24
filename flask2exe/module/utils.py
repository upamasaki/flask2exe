import os
import glob
import shutil
import codecs
import pprint
import base64

import json


def get_img_info(file_paths, message):
    # args : file_paths[message['count']]
    data = {}
    data['img_name'] = file_paths[message['count']].split('\\')[-1]
    data['img_path'] = file_paths[message['count']]
    data['count'] = message['count']
    
    return data

def move_skel_file(img_type, phase_type, message, file_path):

    save_dir = message['output_dir'] + phase_type + '\\' + img_type
    os.makedirs(save_dir, exist_ok=True)

    shutil.copy(file_path, save_dir)
    print(">copy {} ---> {}".format(file_path, save_dir))

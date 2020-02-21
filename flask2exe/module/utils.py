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


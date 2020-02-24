# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
import os
import glob
import sys
import shutil
import codecs
import pprint
import base64

import pandas as pd


from datetime import datetime
from flask2exe import app

from flask import Flask, jsonify, abort, make_response, render_template, request
from flask_cors import CORS
import json


# add path
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(__file__))
print(">sys.path")
pprint.pprint(sys.path)

## my module
from module import utils

log_path = "./log/"
log_file = "logFile.csv"
file_paths = []
count = 0

total_data = []

#img_file = "X:\\aisin_image\\乗車前(谷)\\18日納品\\20191118_1\\VideoData_CAM4_CAM5\\正面図\\第一必要ファイル\\20190820111100CAM5_094.png"
img_file = "./flask2exe/static/assets/img/not_Image.png"
b64 = base64.encodestring(open(img_file, 'rb').read())
message = {'test': 'test'}
img64 = {'img_data': b64.decode('utf8')}
message['page_title'] = 'Hidden-Annotation'
message['config_dir'] = './config/'
message['config_file'] = 'config.json'
message['skel_file'] = 'skeleton_pos.csv'
message['config_path'] = message['config_dir']+message['config_file']
message['skel_path'] = message['config_dir']+message['skel_file']

message['output_file'] = 'output.json'
message['output_dir'] = './log/'
message['output_path'] = message['output_dir'] + message['output_file']


#####################################
## index page

def logInit():
    global message

    print(">run logInit()")
    os.makedirs(log_path, exist_ok=True)
    os.makedirs(message['config_dir'], exist_ok=True)

    now = datetime.now()
    file_name = now.strftime("%Y%m%d_%H%M%S") + ".csv"

    skel_df = pd.read_csv(message['skel_path'], encoding="SHIFT-JIS")
    print("skel_df")
    print(skel_df)
    
    message['skel_name_key'] = [(s1, s2) for s1, s2 in zip(skel_df['posname'], skel_df['keyname'])]
    message['skel_key'] = [i for i in skel_df['keyname']]
    message['skel_key_dump'] = json.dumps(message['skel_key'])

    return file_name

def log_write(log_path, file_name, value, img_path):   
    img_name = img_path.split('\\')[-1]

    print(">img_name:{}  type:{}".format(img_name, value))    
    base_file_path = message['read_path'] + "\\" + img_name
    
    
    if(value==1):
        send_file_path = "./log/" + message['type1']
        
        os.makedirs(send_file_path, exist_ok=True)

        shutil.copy(base_file_path, send_file_path)
        print(">copy {} ---> {}".format(base_file_path, send_file_path))

    if(value==2):
        send_file_path = "./log/" + message['type2']
        os.makedirs(send_file_path, exist_ok=True)

        shutil.copy(base_file_path, send_file_path)
        print(">copy {} ---> {}".format(base_file_path, send_file_path))

@app.route('/')
def index():
    global message

    print("read root index.html")
    message["log_file"] = logInit()
    reload_setting()
    message['page_title'] = 'Hidden-Annotation'
    return render_template('index.html', msg=message, img64=img64)

def reload_progress():
    global message
    global file_paths

    file_paths1 = glob.glob("./log/{}/*".format(message['type1']))
    file_paths2 = glob.glob("./log/{}/*".format(message['type2']))
    message['path_len'] = len(file_paths)
    message['path1_len'] = len(file_paths1)
    message['path2_len'] = len(file_paths2)
    message['pvalue'] = int(message['count']/message['path_len']*100)

def reload_setting():
    global file_paths
    global message

    try:
        with open(message['config_path'], encoding='shift_jis') as f:
            data = json.load(f)
            message.update(data)

            file_paths = glob.glob("{}/*".format(message['read_path']))
            reload_progress()
            

    except:
        print("not found config file")
        
    print(">reload config  message")
    pprint.pprint(message)


@app.route("/next<int:img_type>", methods=["POST"])  #追加
def next(img_type):
    global message
    global total_data

    
    print(">next type:{}".format(img_type))
    b64 = base64.encodestring(open(file_paths[message['count']], 'rb').read())
    img64 = {'img_data': b64.decode('utf8')}
    print(">message['count']:{}".format(message['count']))
    log_write(log_path, log_file, img_type, file_paths[message['count']])
    
    data = utils.get_img_info(file_paths, message)
    data['img_type'] = img_type
    message['data'] = data
    
    total_data.append(message['data'])

    ## =======================================
    ## next data info 
    message['count'] = message['count'] + 1
    data = utils.get_img_info(file_paths, message)

    print("Date dict")
    pprint.pprint(data)
    message.update(data)

    reload_progress()

    print(">msg:")
    pprint.pprint(message)

    print(">total data:")
    pprint.pprint(total_data)

    return render_template('index.html', msg=message, img64=img64)

@app.route("/back")  #追加
def back():
    global message
    global total_data

    print(">run back count:{}".format(message['count']))

    print("data before")
    pprint.pprint(total_data)
    total_data.pop()

    print(" |\n |\n\\/")
    print("data after")
    pprint.pprint(total_data)
    message['count'] = message['count'] -1

    data = utils.get_img_info(file_paths, message)
    data['img_type'] = -1
    message.update(data)

    print("> back message")
    pprint.pprint(message)
    print(">run back fin.... count:{}".format(message['count']))
    return render_template('index.html', msg=message, img64=img64)

#####################################
## Config page

@app.route("/Config")  #追加
def Config():
    global message
    message['page_title'] = 'Config'

    with open(message['config_path'], 'w') as f:
        json.dump(message, f, indent=4, ensure_ascii=False)
    
    reload_setting()

    print(">Config page -- msg:")
    pprint.pprint(message)
    
    return render_template('config.html', msg=message)

@app.route("/update_setting", methods=["POST"])  #追加
def update_setting():
    global message

    print("run update_setting()")
    req = request.form
    message.update(req)
    message['count'] = int(message['save_count'])
    print(message)
    
    with open(message['config_dir']+'config.json', 'w') as f:
        json.dump(message, f, indent=4, ensure_ascii=False)
    
    reload_setting()
    return render_template('config.html', msg=message, img64=img64)

#####################################
## Common page

@app.route("/save_data")  #追加
def save_data():
    global message
    global total_data

    with open(message['config_path'], 'w') as f:
        json.dump(message, f, indent=4, ensure_ascii=False)
    
    with open(message['output_path'], 'w') as f:
        json.dump(total_data, f, indent=4, ensure_ascii=False)

    print(">save_data -- ")
    pprint.pprint(message)

    print(">total_data")
    pprint.pprint(total_data)

    return render_template('index.html', msg=message, img64=img64)


#####################################
## skeleton page
#####################################

@app.route('/Skeleton')
def Skeleton():
    message['page_title'] = 'Skeleton-Annotation'
    return render_template('Skeleton.html', msg=message, img64=img64)

@app.route("/skeleton_next<string:phase_type>-<string:img_type>", methods=["POST"])  #追加
def skeleton_next(img_type, phase_type):
    global message
    global total_data
    global file_paths
    
    ## =======================================
    ## now data save section
    print(">img_type:{}, phase_type:{}".format(img_type, phase_type))
    utils.move_skel_file(img_type, phase_type, message, file_paths[message['count']])
    
    data = utils.get_img_info(file_paths, message)
    data['img_type'] = img_type
    data['img_flag'] = message[img_type]
    data['phase_type'] = phase_type
    data['phase_flag'] = message[phase_type]

    message['data'] = data
    total_data.append(message['data'])

    ## =======================================
    ## next data info 
    message['count'] = message['count'] + 1
    data = utils.get_img_info(file_paths, message)
    message.update(data)

    b64 = base64.encodestring(open(file_paths[message['count']], 'rb').read())
    img64 = {'img_data': b64.decode('utf8')}
    
    reload_progress()

    print(">msg:")
    pprint.pprint(message)

    print(">total data:")
    pprint.pprint(total_data)

    return render_template('Skeleton.html', msg=message, img64=img64)


@app.route("/skeleton_back")  #追加
def skeleton_back():
    global message
    global total_data

    print(">run back count:{}".format(message['count']))

    print("data before")
    pprint.pprint(total_data)
    total_data.pop()

    print(" |\n |\n\\/")
    print("data after")
    pprint.pprint(total_data)
    message['count'] = message['count'] -1

    data = utils.get_img_info(file_paths, message)
    data['img_type'] = -1
    message.update(data)

    print("> back message")
    pprint.pprint(message)
    print(">run back fin.... count:{}".format(message['count']))
    return render_template('Skeleton.html', msg=message, img64=img64)
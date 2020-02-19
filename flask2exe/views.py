# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
import os
import glob
import shutil
import codecs
import pprint
import base64

from datetime import datetime
from flask2exe import app

from flask import Flask, jsonify, abort, make_response, render_template, request
from flask_cors import CORS
import json

log_path = "./log/"
log_file = "logFile.csv"
file_paths = []
count = 0

img_file = "X:\\aisin_image\\乗車前(谷)\\18日納品\\20191118_1\\VideoData_CAM4_CAM5\\正面図\\第一必要ファイル\\20190820111100CAM5_094.png"
b64 = base64.encodestring(open(img_file, 'rb').read())
message = {'test': 'test'}
img64 = {'img_data': b64.decode('utf8')}
message['page_title'] = 'Hidden-Annotation'

def logInit():
    print("run logInit()")
    os.makedirs(log_path, exist_ok=True)
    now = datetime.now()
    file_name = now.strftime("%Y%m%d_%H%M%S") + ".csv"
    return file_name

def log_write(log_path, file_name, value, img_path):   
    pprint.pprint(value)
    img_name = img_path.split('\\')[-1]

    print("img_name")
    print(img_name)
    print("value")
    print(value)
    # パラメータをローカルのファイルに書き込むだけ
    with open(log_path + file_name, mode='a') as f:
        f.write("{}, {}\n".format(img_name, value))
    
    base_file_path = message['read_path'] + "\\" + img_name
    print("base_file_path")
    pprint.pprint(base_file_path)

    
    if(value==1):
        send_file_path = "./log/" + message['type1']
        print(send_file_path)
        os.makedirs(send_file_path, exist_ok=True)

        shutil.copy(base_file_path, send_file_path)

    if(value==2):
        send_file_path = "./log/" + message['type2']
        print(send_file_path)
        os.makedirs(send_file_path, exist_ok=True)

        shutil.copy(base_file_path, send_file_path)

    

log_file = logInit()


def get_file_path():
    file_paths = glob.glob("X:\\aisin_image\\乗車前(谷)\\18日納品\\20191118_1\\VideoData_CAM4_CAM5\\正面図\\第一必要ファイル\\*")
    print(file_paths)


@app.route('/')
def index():
    print("read root index.html")
    message['page_title'] = 'Hidden-Annotation'
    return render_template('index.html', msg=message, img64=img64)

@app.route('/Skeleton')
def Skeleton():
    message['page_title'] = 'Skeleton-Annotation'
    return render_template('index.html', msg=message, img64=img64)

def reload_progress():
    global message
    global count
    global file_paths

    #
    file_paths1 = glob.glob("./log/{}/*".format(message['type1']))
    file_paths2 = glob.glob("./log/{}/*".format(message['type2']))
    message['path_len'] = 11030#len(file_paths)
    message['path1_len'] = len(file_paths1)
    message['path2_len'] = len(file_paths2)
    message['count'] = count
    message['pvalue'] = int(message['count']/message['path_len']*100)

def reload_setting():
    global file_paths
    global message
    global count

    try:
        with open('./log/config.json', encoding='shift_jis') as f:
            data = json.load(f)
            message.update(data)

            file_paths = glob.glob("{}/*".format(message['read_path']))
            count = int(message['save_count'])
            reload_progress()
            print("message1")
            print(message)
            

    except:
        print("not found config file")
        
    print("message['count'] = int(message['save_count'])")
    print(message)
    

reload_setting()




@app.route("/update_setting", methods=["POST"])  #追加
def update_setting():
    global message
    print("run update_setting()")
    req = request.form
    
    message.update(req)
    print(message)
    
    with open('./log/config.json', 'w') as f:
        json.dump(message, f, indent=4, ensure_ascii=False)
    
    reload_setting()
    return render_template('index.html', msg=message, img64=img64)


@app.route("/next", methods=["POST"])  #追加
def next():
    global count

    print("run next()")
    print("len(file_paths):{}".format(len(file_paths)))
    b64 = base64.encodestring(open(file_paths[count], 'rb').read())
    img64 = {'img_data': b64.decode('utf8')}
    print("count:{}".format(count))
    log_write(log_path, log_file, 0, file_paths[count])
    
    count = count + 1
    reload_progress()

    return render_template('index.html', msg=message, img64=img64)

@app.route("/type1", methods=["POST"])  #追加
def type1():
    global count

    print("run next()")
    b64 = base64.encodestring(open(file_paths[count], 'rb').read())
    img64 = {'img_data': b64.decode('utf8')}
    print("count:{}".format(count))
    log_write(log_path, log_file, 1, file_paths[count])
    
    count = count + 1
    reload_progress()

    return render_template('index.html', msg=message, img64=img64)

@app.route("/type2", methods=["POST"])  #追加
def type2():
    global count

    print("run next()")
    b64 = base64.encodestring(open(file_paths[count], 'rb').read())
    img64 = {'img_data': b64.decode('utf8')}
    print("count:{}".format(count))
    log_write(log_path, log_file, 2, file_paths[count])
    
    count = count + 1
    reload_progress()

    return render_template('index.html', msg=message, img64=img64)
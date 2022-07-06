from dataclasses import dataclass
import requests
import datetime
from app import app
from flask import jsonify
import os

def get_picture(ip:str):
    r = requests.get(f"http://{ip}/capture")
    now = str(datetime.datetime.now())
    path = f"{app.config['UPLOAD_FOLDER']}/{ip}"
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    id = len(os.listdir(path=path))
    
    # f = open(f"{path}/{now.replace(':','-').replace(' ','-')}-{ip}.jpg", "wb")
    f = open("%s/IMG%05d.jpg" % (path, id), "wb")
    f.write(r.content)
    f.close()
    print(f"Image saved {ip} at {now}")
    return True

def get_config(ip:str):
    r = requests.get(f"http://{ip}/status")
    return jsonify(r.json())
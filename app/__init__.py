from flask import Flask, flash, request, redirect, url_for
from flask_apscheduler import APScheduler
import time
import requests
from config import *

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'app/storage/pictures'
app.config['picture_storage'] = 'app/storage/pictures'


from app.controllers import indexController
from app.controllers import pictureController
from app.controllers import jobController
from app.components.job import load_scheduler, init_jobs, resume_jobs, load_jobs
from app.components.picture import get_config, get_picture

APPscheduler = load_scheduler()
APPscheduler.api_enabled = True
APPscheduler.init_app(app)
APPscheduler.start(paused=False)

# time.sleep(5)
init_jobs(APPscheduler)
# jobs = load_jobs()

# for ip in jobs.keys():
#     seconds = int(jobs[ip]['interval'])
    
#     if(APPscheduler.get_job(ip)!=None):
#         APPscheduler.remove_job(ip)
#     print(f"Try http://192.168.1.13:{port}/job/add/{ip}/{seconds}")
#     request.get(f"192.168.1.13:{port}/job/add/{ip}/{seconds}")


APPscheduler.scheduler.print_jobs()

# resume_jobs(APPscheduler)

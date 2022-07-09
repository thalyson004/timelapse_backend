from app import app
from app.components.picture import get_picture, get_config
from app.components.job import *
from flask import jsonify
from datetime import datetime

@app.route("/job/add/<ip>/<seconds>")
def job_add(ip:str, seconds:str):
    seconds = int(seconds)
    from app import APPscheduler
    if(APPscheduler.get_job(ip)!=None):
        APPscheduler.remove_job(ip)
    
    APPscheduler.add_job(
        id=ip, 
        func= lambda : get_picture(ip),
        trigger='interval', 
        seconds=seconds,
        max_instances=5,
    )
    
    jobs = load_jobs()
    jobs[ip] = {
        'interval':seconds,
        'framesize': get_config(ip).json["framesize"]
    }
    save_jobs(jobs)
        
    
    return "Job created/changed"

@app.route("/job/remove/<ip>")
def job_remove(ip:str):
    from app import APPscheduler
    if(APPscheduler.get_job(ip)!=None):
        APPscheduler.remove_job(ip)
        jobs = load_jobs()
        jobs.pop(ip, None)
        save_jobs(jobs)    
    
    
    return "Job removed"

@app.route("/job/list")
def job_list():
    return jsonify(load_jobs())
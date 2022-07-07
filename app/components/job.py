from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pickle 

from app.components.picture import get_picture

path = 'app/storage/jobs/jobs'

def load_scheduler()->APScheduler:
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 5
    }
    scheduler = APScheduler(
        # scheduler=BackgroundScheduler(
        #     jobstores=jobstores,
        #     executors=executors, 
        #     job_defaults=job_defaults,
        #     daemon=True
        # ),
        scheduler=BackgroundScheduler({
            'apscheduler.job_defaults.max_instances': '3',
        }),
    )
    
    return scheduler

def load_jobs()->dict:
    jobs = None
    try:
        # load jobs
        jobs = pickle.load(open(path, 'rb'))
        print('Jobs loaded')
    except:
        # No file
        jobs = dict()
        pickle.dump(jobs, open(path, 'wb'))
        print('Jobs created')
        
    return jobs

def save_jobs(jobs:dict)->dict:
    pickle.dump(jobs, open(path, 'wb'))  
    return jobs
        
def init_jobs(scheduler:APScheduler):
    jobs = load_jobs()
    print(jobs)

    for ip in jobs.keys():
        seconds = int(jobs[ip]['interval'])
        print(f"IP {ip} ->>> Interval: {seconds}")
        
        if(scheduler.get_job(ip)!=None):
            scheduler.remove_job(ip)
        
        scheduler.add_job(
            id=ip, 
            func= lambda : get_picture(ip),
            trigger='interval', 
            seconds=seconds,
            max_instances=5,
        )
        
      
def resume_jobs(scheduler:APScheduler):
    jobs = load_jobs()
    for job in jobs.keys():
        print(f"Resume {job}")
        scheduler.resume_job(job)
'''
jobs = {
    '192.168.1.11' : {
        'interval': 10
        'framesize': 12
    },  
    '192.168.1.113' : {
        'interval': 10
        'framesize': 10
    }
}
'''
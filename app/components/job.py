from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import pickle 

from app.components.picture import get_picture

path = 'app/storage/jobs/jobs'

def load_scheduler()->APScheduler:
    scheduler = APScheduler(
        scheduler=BackgroundScheduler(
            {
                'apscheduler.executors.default': {
                    'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                    'max_workers': '20'
                },
                'apscheduler.executors.processpool': {
                    'type': 'processpool',
                    'max_workers': '5'
                },
                'apscheduler.job_defaults.max_instances': 3,
                'apscheduler.job_defaults.coalesce': 'false',
            }, 
            daemon=True)
    )
    init_jobs(scheduler)
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
        print(f"IP {ip} ->>> Interval: {int(jobs[ip]['interval'])}")
        scheduler.add_job(
            id=ip, 
            func= lambda : get_picture(ip),
            trigger='interval', 
            seconds=int(jobs[ip]['interval']),
            replace_existing=False,
        )

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
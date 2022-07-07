from app import app, request, APPscheduler
import multiprocess
import time
from app.components.job import load_scheduler, init_jobs, resume_jobs, load_jobs
from app.components.picture import get_config, get_picture
from flask_script import Manager

from config import *

app.run(
    host=ipv4, 
    port=port, 
    debug=False, 
    use_reloader=False,
    threaded=True,
)
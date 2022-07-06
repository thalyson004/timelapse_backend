from flask import Flask, flash, request, redirect, url_for
from flask_apscheduler import APScheduler


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'app/storage/pictures'
app.config['picture_storage'] = 'app/storage/pictures'


from app.controllers import indexController
from app.controllers import pictureController
from app.controllers import jobController
from app.components.job import load_scheduler

APPscheduler = load_scheduler()
APPscheduler.init_app(app)
APPscheduler.start()
print(APPscheduler.scheduler.print_jobs())
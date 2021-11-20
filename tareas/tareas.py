import os 
import subprocess
from datetime import datetime

import boto3
from celery import Celery

import db
from model import Tarea

aws_access_key_id = os.getenv('AWS_ACCES_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCES_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')

resource = boto3.resource(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
    aws_session_token = aws_session_token
)

redis_host = os.getenv('REDIS_HOST')

celery_app = Celery(__name__, broker = f'redis://{redis_host}:6379/0')

@celery_app.task(name = 'process_audio')
def process_audio(task_id):
    tarea = db.session.query(Tarea).get(task_id)

    in_file_name = f"uploads/{tarea.fileName}.{tarea.originalFormat}"
    out_file_name = f"downloads/{tarea.fileName}.{tarea.newFormat}"

    in_file = os.path.join("uploads", f"{tarea.fileName}.{tarea.originalFormat}")

    resource.Bucket('cloud-uniandes-grupo-25').download_file(in_file_name, in_file)

    out_file = os.path.join("downloads", f"{tarea.fileName}.{tarea.newFormat}")

    subprocess.call(['ffmpeg', '-i', in_file, out_file,'-y'])

    resource.Bucket('cloud-uniandes-grupo-25').upload_file(out_file, out_file_name)

    download_file_exist = os.path.exists(out_file)
    if download_file_exist :
        os.remove(out_file)

    upload_file_exist = os.path.exists(in_file)
    if upload_file_exist :
        os.remove(in_file)

    tarea.lastUpdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    tarea.status = "processed"

    db.session.add(tarea)
    db.session.commit()

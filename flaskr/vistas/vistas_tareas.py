import os
from datetime import datetime
import uuid
import boto3

from celery import Celery
from flask import request, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from modelos.modelos import db, Usuario, Tareas, TareasSchema

aws_access_key_id = os.getenv('AWS_ACCES_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCES_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')

resource = boto3.resource(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key,
    aws_session_token = aws_session_token
)

tareas_schema = TareasSchema()

redis_host = os.getenv('REDIS_HOST')

celery_app = Celery(__name__, broker = f'redis://{redis_host}:6379/0')

@celery_app.task(name = 'process_audio')
def process_audio(*args):
    pass
class VistaTareas(Resource):

    @jwt_required()
    def get(self):

        query = Tareas.query.filter(Tareas.usuario == get_jwt_identity())

        if request.is_json :
            if "order" in request.json and request.json["order"] == 1  :
                query = query.order_by(Tareas.id.desc())
            if "max" in request.json:
                tareas = query.limit(int(request.json["max"]))
            else :
                tareas = query.all()
        else :
            tareas = query.all()

        return [ tareas_schema.dump(tarea) for tarea in tareas]
            

    @jwt_required()
    def post(self):

        file = request.files['fileName']
        format = request.form.get("newFormat")

        file_path = os.path.join("uploads",file.filename)

        file.save(file_path)

        resource.Bucket('cloud-uniandes-grupo-25').upload_file(file_path, f"uploads/{file.filename}")

        upload_file_exist = os.path.exists(file_path)
        if upload_file_exist :
            os.remove(file_path)

        usuario = Usuario.query.get_or_404(get_jwt_identity())

        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tarea = Tareas(
            fileName = file.filename.rsplit('.')[0], 
            originalFormat = file.filename.rsplit('.')[-1],
            newFormat = format,
            timeStamp = time,
            lastUpdate = time )

        db.session.add(tarea)        
        usuario.tareas.append(tarea)
        db.session.commit()

        args = (tarea.id,)
        process_audio.apply_async(args = args, queue = 'process_audio')

        return "Empezo procesamiento", 202

class VistaTareasTest(Resource):

    @jwt_required()
    def post(self):

        file = request.json["fileName"]
        format = request.json["newFormat"] 

        copy_source = {
                'Bucket': 'cloud-uniandes-grupo-25',
                'Key': f"carga/{file}"
        }

        original_format = file.rsplit('.')[-1]
        new_file = f'{str(uuid.uuid1())}.{original_format}'
        resource.meta.client.copy(copy_source, 'cloud-uniandes-grupo-25', f'uploads/{new_file}')

        usuario = Usuario.query.get_or_404(get_jwt_identity())

        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tarea = Tareas(
            fileName = new_file.rsplit('.')[0], 
            originalFormat = new_file.rsplit('.')[-1],
            newFormat = format,
            timeStamp = time,
            lastUpdate = time )

        db.session.add(tarea)        
        usuario.tareas.append(tarea)
        db.session.commit()

        args = (tarea.id,)
        process_audio.apply_async(args = args, queue = 'process_audio')

        return "Empezo procesamiento", 202
class VistaTarea(Resource):

    @jwt_required()
    def get(self,id_task):

        tarea = Tareas.query.filter(Tareas.usuario == get_jwt_identity(), Tareas.id == id_task).first()
        if tarea is None:
            return "La tarea no existe", 404

        return tareas_schema.dump(tarea)

    @jwt_required()
    def put(self,id_task):

        tarea = Tareas.query.filter(Tareas.usuario == get_jwt_identity(), Tareas.id == id_task).first()
        if tarea is None:
            return "La tarea no existe", 404

        if tarea.status == "processed" :
            resource.Object('cloud-uniandes-grupo-25', f"downloads/{tarea.fileName}.{tarea.newFormat}").delete()

        tarea.status = "uploaded"
        tarea.newFormat = request.json["newFormat"]
        tarea.lastUpdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        db.session.commit()

        args = (tarea.id,)
        process_audio.apply_async(args = args, queue = 'process_audio')

        return tareas_schema.dump(tarea)

    @jwt_required()
    def delete(self,id_task):

        tarea = Tareas.query.filter(Tareas.usuario == get_jwt_identity(), Tareas.id == id_task).first()
        if tarea is None:
            return "La tarea no existe", 404

        resource.Object('cloud-uniandes-grupo-25', f"downloads/{tarea.fileName}.{tarea.newFormat}").delete()

        resource.Object('cloud-uniandes-grupo-25', f"uploads/{tarea.fileName}.{tarea.originalFormat}").delete()

        db.session.delete(tarea)
        db.session.commit()

        return "Tarea borrada exitosamente", 404



class VistaArchivo(Resource):

    @jwt_required()
    def get(self,filename):


        file = filename.rsplit('.')[0]
        tarea = Tareas.query.filter(Tareas.usuario == get_jwt_identity(), Tareas.fileName == file).first()
        if tarea is None:
            return "Nombre de archivo no existe", 404

        out_file = os.path.join("downloads", filename)

        resource.Bucket('cloud-uniandes-grupo-25').download_file(f"downloads/{filename}", out_file)

        download_file = os.path.join("downloads", filename)
        download_file_exist = os.path.exists(download_file)

        if download_file_exist :
            return send_from_directory(directory="downloads", filename=filename)


        return "No se encontro el archivo en el servidor", 500
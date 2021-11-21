import os

from flask import Flask
from flask_restful import Api

from vistas.vista_health import VistaHealth
from vistas.vista_loging import VistaSignUp, VistaLogIn
from vistas.vistas_tareas import VistaTareas, VistaTarea, VistaArchivo, VistaTareasTest
from modelos.modelos import db
from config.config import cfg
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app(env = 'production'):
    app = Flask(__name__)  

    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_pass = os.getenv('POSTGRES_PASS')
    app.config.from_object(cfg[env])
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{postgres_pass}@{postgres_host}:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    return app

app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)

cors = CORS(app)

api = Api(app)

api.add_resource(VistaTareas, '/api/tasks')
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>')
api.add_resource(VistaArchivo, '/api/files/<string:filename>')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTareasTest, '/api/tasks/carga')
api.add_resource(VistaHealth, '/')



jwt = JWTManager(app)



                 

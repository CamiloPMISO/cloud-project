
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    tareas = db.relationship('Tareas', cascade='all, delete, delete-orphan')

class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fileName = db.Column(db.String(128))
    originalFormat = db.Column(db.String(128))
    newFormat = db.Column(db.String(128))
    timeStamp = db.Column(db.String(128))
    lastUpdate = db.Column(db.String(128))
    status = db.Column(db.String(128), default = 'uploaded')
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class TareasSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Tareas
         include_relationships = True
         load_instance = True
import os
import datetime

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from modelos.modelos import db, Usuario

class VistaSignUp(Resource):
    
    def post(self):

        if (request.json["password1"] != request.json["password2"]):
            return "Las contraseñas no coinciden", 404

        usuario = Usuario.query.filter(Usuario.usuario == request.json["username"]).first()

        if usuario is not None:
            return "Usuario ya existe", 404

        correo = Usuario.query.filter(Usuario.correo == request.json["email"]).first()

        if correo is not None:
            return "Correo ya existe", 404

        nuevo_usuario = Usuario(
            usuario=request.json["username"], 
            contrasena=request.json["password1"], 
            correo = request.json["email"])

        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["username"], Usuario.contrasena == request.json["password"]).first()
        if usuario is None:
            return "Usuario o contraseña no valida", 404

        token_de_acceso = create_access_token(identity = usuario.id)
        return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}
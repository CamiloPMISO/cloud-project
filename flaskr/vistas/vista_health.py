from flask_restful import Resource

class VistaHealth(Resource):

    def get(self):
        return "ok", 200
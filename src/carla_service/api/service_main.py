from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import request

from carla_service.api.resources.frontends import Valerie
from carla_service.api.resources.simulators import CarlaSimulator

app = Flask(__name__)
api = Api(app)


class MainApp(Resource):
    def post(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Shutting down..."


api.add_resource(MainApp, '/api/v1/shutdown')
api.add_resource(Valerie, '/api/v1/frontend/Valerie/ReadConfig')
api.add_resource(CarlaSimulator, '/api/v1/simulators/Carla/ScheduleTasks')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)

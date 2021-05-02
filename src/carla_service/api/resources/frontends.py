from flask import jsonify
from flask_restful import Resource, reqparse
from carla_service.frontends import ValeryFrontend


class Valerie(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('path')
        self.args = parser.parse_args()

    def get(self):
        frontend = ValeryFrontend()
        jsonTasks = list(map(lambda task: task.to_json(),
                             frontend.read_input(self.args['path'])))
        return jsonify(jsonTasks)

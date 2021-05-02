from carla_service.assets import SenzorTypes
from carla_service.tasks import CarMovementTask
from flask import jsonify
from flask_restful import Resource, reqparse
from carla_service.frontends import ValeryFrontend
from carla_service.simulator import Simulator
from carla_service.tasks import SpawnCarTask, SpawnCameraTask, TaskFactoryFromJSON
import carla
import json

class CarlaSimulator(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('carlaserver')
        parser.add_argument('tasks', type=str)
        self.args = parser.parse_args()

    def createCarAndCameraTasks(self, cameryType):
        t1 = SpawnCarTask()

        t2 = SpawnCameraTask()
        t2.cameraType = cameryType
        t2.resolution = [1920, 1080]
        t2.tickInterval = 0.1
        t2.ticks = 3
        t2.transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        t3 = SpawnCameraTask()
        t3.cameraType = SenzorTypes.RGB
        t3.resolution = [1920, 1080]
        t3.tickInterval = 0.1
        t3.ticks = 3
        t3.transform = carla.Transform(carla.Location(x=1.5, z=2.4))

        return [t1, t2, t3]

    def post(self):
        s = Simulator(carlaserver=self.args['carlaserver'])
        frontend = ValeryFrontend()
        assert (s)
        assert (frontend)

        tasks = self.createCarAndCameraTasks(SenzorTypes.Semantic)
        s.scheduleTasks([tasks[0]])
        tasks[1].vehicleId = tasks[0].carId
        tasks[2].vehicleId = tasks[0].carId
        s.scheduleTasks([tasks[1], tasks[2]])
        carId = tasks[0].carId
        jsonData = json.loads(self.args['tasks'])
        jsonTaskFactory = TaskFactoryFromJSON()
        tasks = jsonTaskFactory.create(jsonData)
        for t in tasks:
            if isinstance(t, CarMovementTask):
                t.carId = carId
        #assert (len(tasks) > 0)
        s.scheduleTasks(tasks)
        return "tasks scheduled"

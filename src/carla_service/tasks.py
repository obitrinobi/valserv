from enum import Enum
import json
import jsonpickle


class SimulatorTask:
    scene = None
    terminateWorker = False

    def execute(self):
        pass

    def to_json(self):
        return jsonpickle.encode(self)


class TerminationTask(SimulatorTask):
    def __init__(self):
        self.terminateWorker = True


class SpawnCameraTask(SimulatorTask):
    def __init__(self):
        self.cameraType = None
        self.transform = None
        self.vehicleId = None
        self.resolution = None
        self.tickInterval = None
        self.ticks = None

    def execute(self):
        vehicle = self.scene.getAsset(self.vehicleId).actor
        self.scene.spawnCamera(self.cameraType, self.resolution, self.transform, vehicle, self.tickInterval, self.ticks)


class SpawnCarTask(SimulatorTask):
    def __init__(self):
        self.carId = None

    def execute(self):
        self.carId = self.scene.spawnCar()


class CarMovementTask(SimulatorTask):
    def __init__(self):
        self.carId = None
        self.position = None
        self.orientation = None

    def execute(self):
        assert self.scene != None
        self.scene.moveAsset(self.carId, self.position, self.orientation)


class WeatherTask(SimulatorTask):
    class WeatherType(Enum):
        Azimuth = 0
        Altitude = 1

    def execute(self):
        weatherService = self.scene.getWeatherService()
        if self.type == WeatherTask.WeatherType.Azimuth:
            weatherService.set_sun_azimuth_angle(self.value)
        elif self.type == WeatherTask.WeatherType.Altitude:
            weatherService.set_sun_altitude_angle(self.value)


class ToggleSenzorsTask(SimulatorTask):
    def __init__(self):
        self.ticks = 1

    def execute(self):
        assert self.scene != None
        self.scene.toggleSensors(self.ticks)


class TaskFactoryFromJSON:
    def __init__(self):
        pass

    def create(self, jsonContex):
        return list(map(lambda task: jsonpickle.decode(task), jsonContex))

import threading
import uuid
import random
from enum import Enum

import carla
from carla import Location
from carla import ColorConverter as cc, Image
import queue

import time
class SenzorTypes(Enum):
    RGB = 'sensor.camera.rgb'
    Semantic = 'sensor.camera.semantic_segmentation'


# def sensorCallback(image, scene, senzor_id):
# if scene.can_tick(senzor_id):
#    with scene.lock:
#        scene.assets[senzor_id].ticks = scene.assets[senzor_id].ticks - 1
#        if scene.assets[senzor_id].sensorType == SenzorTypes.Semantic:
#            image.save_to_disk('/data/%06d.png' % image.frame, cc.CityScapesPalette)
#        else:
#            image.save_to_disk('/data/%06d.png' % image.frame, cc.Raw)
#        scene.condition.notifyAll()


class SceneAsset:
    def __init__(self, actor):
        self.actor = actor


class CarAsset(SceneAsset):
    pass


class SensorAsset(SceneAsset):
    def __init__(self, actor, cameraType=SenzorTypes.RGB, ticks=1):
        super().__init__(actor)
        self.sensorType = cameraType
        self.attached = False
        self.ticks = ticks


class SceneWeather:
    def __init__(self, weather):
        self.weather = weather

    def set_sun_azimuth_angle(self, angle):
        self.weather.sun_azimuth_angle = angle

    def set_sun_altitude_angle(self, angle):
        self.weather.sun_altitude_angle = angle


class Scene(object):

    def __init__(self, world, **kwargs):
        self.world = world
        self.frame = None
        self.delta_seconds = 1.0 / kwargs.get('fps', 20)
        self._queues = []
        self._settings = None
        self.weather = SceneWeather(world.get_weather())
        self.assets = {}
        #self.syncMode = CarlaSyncMode(self.world, self.get_sensors(), fps=30)

    def make_queue(self, event_type, register_event):
            q = queue.Queue()
            register_event(q.put)
            self._queues.append((event_type,q))

    def __enter__(self):
        self._settings = self.world.get_settings()
        self.frame = self.world.apply_settings(carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_seconds))



        #self.make_queue(self.world.on_tick)

        return self

    def tick(self, timeout):
        self.frame = self.world.tick()
        data = [(t, self._retrieve_data(q, timeout)) for (t, q) in self._queues]
        assert all(x.frame == self.frame for (_, x) in data)
        return data

    def __exit__(self, *args, **kwargs):
        self.world.apply_settings(self._settings)

    def _retrieve_data(self, sensor_queue, timeout):
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data

    def getAsset(self, assetId):
        if assetId in self.assets.keys():
            return self.assets[assetId]
        else:
            return None

    def can_tick(self, sensor_id):
        return self.assets[sensor_id].ticks > 0

    def getWeatherService(self):
        return self.weather

    def spawnCamera(self, cameraType, camera_resolution, camera_transform, vehicle, tickInterval, ticks):
        cameraID = uuid.uuid1()

        blueprint_library = self.world.get_blueprint_library()
        camera_bp = blueprint_library.find(cameraType.value)
        assert (len(camera_resolution) == 2)
        camera_bp.set_attribute('image_size_x', str(camera_resolution[0]))
        camera_bp.set_attribute('image_size_y', str(camera_resolution[1]))
        #camera_bp.set_attribute('sensor_tick', str(tickInterval))
        camera = self.world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        self.assets[cameraID] = SensorAsset(camera, cameraType, ticks)
        self.make_queue(cameraType, camera.listen)
        #self.make_queue(
        #make_queue(sensor.listen)
        return cameraID

    def spawnCar(self):
        carID = uuid.uuid1()

        # The world contains the list blueprints that we can use for adding new
        # actors into the simulation.
        blueprint_library = self.world.get_blueprint_library()

        # Now let's filter all the blueprints of type 'vehicle' and choose one
        # at random.
        bp = random.choice(blueprint_library.filter('vehicle'))

        # A blueprint contains the list of attributes that define a vehicle's
        # instance, we can read them and modify some of them. For instance,
        # let's randomize its color.
        if bp.has_attribute('color'):
            color = random.choice(bp.get_attribute('color').recommended_values)
            bp.set_attribute('color', color)

        # Now we need to give an initial transform to the vehicle. We choose a
        # random transform from the list of recommended spawn points of the map.
        transform = random.choice(self.world.get_map().get_spawn_points())

        # So let's tell the world to spawn the vehicle.
        vehicle = self.world.spawn_actor(bp, transform)
        self.world.get_spectator().set_transform(transform)

        self.assets[carID] = CarAsset(vehicle)

        return carID

    def moveAsset(self, assetId, position, orientation):
        if assetId in self.assets:
            self.assets[assetId].actor.set_location(Location(position[0], position[1], position[2]))
        # TODO implement orientation change

    def get_sensors(self):
        l = []
        for asset_key in self.assets.keys():
            if isinstance(self.assets[asset_key], SensorAsset):
                l.append(self.assets[asset_key].actor)
        return l

    def toggleSensors(self, ticks):
        data = self.tick(timeout=2.0)
        for t, d in data:
            ccType = cc.Raw
            if(t == SenzorTypes.Semantic):
                ccType = cc.CityScapesPalette
            if(isinstance(d, Image)):
                d.save_to_disk('/data/%s.%06d.png' % (t.value,d.frame), ccType)
        #self.syncMode.reset()
        # self.sync_senzors()

import json
import re

from carla_service.valerieclasses import ValDecoder, Sampler, ValEncoder
from carla_service.tasks import CarMovementTask, WeatherTask, ToggleSenzorsTask


class ServiceFronted:
    pass


class ValeryTaskFactory:
    def createTask(variantDict):
        variantName = variantDict['Name']
        task = None
        if "car" in variantName:
            cId = int(re.search('car-(\d+)', variantName, re.IGNORECASE).group(1))
            task = CarMovementTask()
            task.position = [0.0, 0.0, 0.0]
            task.carId = cId
        elif "sun.altitude" in variantName:
            task = WeatherTask()
            task.type = WeatherTask.WeatherType.Altitude
            task.value = float(variantDict['v'])
        elif "sun.azimuth" in variantName:
            task = WeatherTask()
            task.type = WeatherTask.WeatherType.Azimuth
            task.value = float(variantDict['v'])

        if "pos.x" in variantName:
            task.position[0] = float(variantDict['v'])
        if "pos.y" in variantName:
            task.position[1] = float(variantDict['v'])

        return task


class ValeryFrontend:
    ServiceFronted

    def read_input(self, param):
        tasks = []
        with open(param, 'r', encoding='utf-8') as f:
            valeryObj = json.load(f, object_hook=ValDecoder)
            var_path = "out"
            sampler = Sampler(valeryObj)
            for variant in sampler:
                for it in variant.attributelist:
                    itDict = it.ToDict()
                    tasks.append(ValeryTaskFactory.createTask(itDict))
                tasks.append(ToggleSenzorsTask())
                print("\n")

                # for now we assume all sensors collect data

        return tasks

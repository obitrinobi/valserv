import carla
import threading
import queue

from carla_service.assets import Scene
from carla_service.tasks import TerminationTask
import time

class Simulator:

    def __init__(self, client=None, carlaserver='localhost'):
        self.tasks = []
        self.queue = queue.Queue()
        self.terminated = False
        if client is None:
            self.cl = carla.Client(carlaserver, 2000)
        else:
            self.cl = client
        self.cl.set_timeout(2.0)
        threading.Thread(target=self.worker, daemon=True).start()

    def __del__(self):
        self.scheduleTasks([TerminationTask()])

    def isConnected(self):
        return self.cl is not None

    def worker(self):
        workerNotTerminated = True
        with Scene(self.cl.get_world()) as scene:
            while workerNotTerminated:
                item = self.queue.get()
                item.scene = scene
                item.execute()
                workerNotTerminated = not item.terminateWorker
                self.queue.task_done()
    def scheduleTasks(self, taskList):
        for t in taskList:
            #t.scene = self.scene
            #t.execute()
            self.queue.put(t)
        self.queue.join()

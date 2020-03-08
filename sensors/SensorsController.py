from sensors.SensorsChecker import SensorsChecker
import sys
import os

sys.path.insert(0, os.pardir)


class SensorsController(SensorsChecker, ):
    def __init__(self):
        super(SensorsController, self).__init__()


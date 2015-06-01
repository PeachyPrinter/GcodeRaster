from raster import Raster
from os import path
import logging

class Run(object):
    def __init__(self):
        pass

    def start(self):
        laser_width = 0.01
        add_boarders = True
        filename = path.join('..', 'test.jpg')
        raster = Raster(laser_width, add_boarders)
        raster.process_file(filename)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level='INFO')
    Run().start()
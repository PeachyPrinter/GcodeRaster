import logging
import os.path
from scipy import ndimage


class Raster(object):
    def __init__(self, laser_width=0.5, add_borders=True, output_file_name=None, overwrite=False):
        self.file_raster = ImageRaster(laser_width, add_borders)
        self.output_file_name=output_file_name

    def process_file(self, file_name):
        with open(self.output_file_name, 'w') as output_file:
            if os.path.isfile(file_name):
                image = ndimage.imread(file_name)
                result = self.file_raster.process(image)
                output_file.write(result)
            else:
                logging.error("File {0} could not be found.".format(file_name))
                raise IOError("File Not Found")

    def process_folder(self, folder_name):
        pass


class ImageRaster(object):
    def __init__(self, laser_width, add_borders):
        pass

    def process(self, image, height=0.0):
        return "Some thing"
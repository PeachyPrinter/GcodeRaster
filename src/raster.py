import logging
import os.path


class Raster(object):
    def __init__(self, laser_width=0.5, add_borders=True, output_file=None, overwrite=False):
        self.file_raster = FileRaster(laser_width, add_borders)

    def process_file(self, file_name):
        if os.path.isfile(file_name):
            result = self.file_raster.process(file_name)
        else:
            logging.error("File {0} could not be found.".format(file_name))
            raise IOError("File Not Found")

    def process_folder(self, folder_name):
        pass


class FileRaster(object):
    def __init__(self, laser_width, add_borders):
        pass

    def process(self, file_name):
        return file_name
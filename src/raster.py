import logging
import os.path
import datetime
import numpy as np
from scipy import ndimage


class Raster(object):
    def __init__(self, laser_width=0.5, add_borders=True, output_file_name=None):
        self.file_raster = ImageRaster(laser_width, add_borders)
        if output_file_name:
            self.output_file_name=output_file_name
        else:
            self.output_file_name='out{0}.gcode'.format(datetime.datetime.now().strftime('%Y-%b-%d-%H%M'))

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
        self.laser_width = laser_width
        self.add_borders = add_borders
        self.extrude = 0.0

    def print_ascii(self, image):
        string = '\n'
        for y in range(0, image.shape[0]):
            for x in range(0, image.shape[1]):
                if np.array_equal(image[y][x], [0, 0, 0]):
                    string += '$'
                else:
                    string += ' '
            string += '\n'
        return string + '\n-------\n'

    def process(self, image, height=0.0):
        image = self._add_border(image)
        self.max_y_pix = image.shape[0]
        self.max_x_pix = image.shape[1]
        logging.info("Image Dimensions: width: {0} height: {1}".format(self.max_x_pix, self.max_y_pix))

        gcode = ""
        for y in range(0, image.shape[0]):
            gcode += ';row {0}\n'.format(y)
            gcode += self._process_column(image[y], y)
        return gcode

    def _process_column(self, column, current_row):
        state = False
        gcode = ''
        last_pos = 0
        extruding_amount = 0.0
        for column_pos in range(column.shape[0]):
            if np.array_equal([0, 0, 0], column[column_pos]):
                extruding_amount += 1
                if state is False:
                    state = True
                    extruding_amount = 1
                    (x, y) = self._to_real(column_pos, current_row)
                    gcode += "G0 F0 X{:.2f} Y{:.2f} Z0.00 E{:.2f}\n".format(x, y, self.extrude)
            else:
                if state is True:
                    state = False
                    self.extrude += extruding_amount
                    extruding_amount = 0
                    (x, y) = self._to_real(last_pos, current_row)
                    gcode += "G1 F1 X{:.2f} Y{:.2f} Z0.00 E{:.2f}\n".format(x, y, self.extrude)
            last_pos = column_pos
        if state is True:
            self.extrude += extruding_amount
            (x, y) = self._to_real(column_pos, current_row)
            gcode += "G1 F1 X{:.2f} Y{:.2f} Z0.00 E{:.2f}\n".format(x, y, self.extrude)
        return gcode


    def _to_real(self, x, y):
        x_pos = float(x * self.laser_width) - ((self.max_x_pix  - 1 * self.laser_width) / 2.0)
        y_pos = float((self.max_y_pix - y) * self.laser_width) - ((self.max_y_pix + 1 * self.laser_width) / 2.0)
        return (x_pos, y_pos)


    def _add_border(self, image):
        vborder = np.zeros((image.shape[0], 1, image.shape[2]))
        toped = np.append(vborder, image, axis=1)
        bottomed = np.append(toped, vborder, axis=1)
        hborder = np.zeros((1, bottomed.shape[1], bottomed.shape[2]))
        lefted = np.append(hborder, bottomed, axis=0)
        righted = np.append(lefted, hborder, axis=0)
        return righted

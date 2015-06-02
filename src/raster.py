import logging
import os.path
import datetime
import numpy as np
from scipy import ndimage


class Raster(object):
    def __init__(self, laser_width=0.5, add_borders=True, output_file_name=None, layer_height=0.1):
        self.layer_height = layer_height
        self.file_raster = ImageRaster(laser_width, add_borders)
        if output_file_name:
            self.output_file_name = output_file_name
        else:
            self.output_file_name = 'out{0}.gcode'.format(datetime.datetime.now().strftime('%Y-%b-%d-%H%M'))

    def process_file(self, file_name):
        with open(self.output_file_name, 'w') as output_file:
            self._process_file(file_name, output_file, 0.0)

    def _process_file(self, file_name, output_file, height):
        if os.path.isfile(file_name):
            image = ndimage.imread(file_name)
            result = self.file_raster.process(image, height)
            output_file.write(result)
        else:
            logging.error("File {0} could not be found.".format(file_name))
            raise IOError("File Not Found")

    def process_folder(self, folder_name):
        files = [os.path.join(folder_name, a_file) for a_file in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, a_file))]
        image_files = [image_file for image_file in files if image_file.split('.')[-1] in ['png', 'jpg', 'jpeg']]
        image_files.sort()
        height = 0.0
        with open(self.output_file_name, 'w') as output_file:
            for a_file in image_files:
                logging.info("Processing: {}".format(a_file))
                self._process_file(a_file, output_file, height)
                height += self.layer_height


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
        logging.info("Laser width: {0} ".format(self.laser_width))
        logging.info("Final Image Dimensions: width: {0}mm height: {1}mm".format(self.max_x_pix * self.laser_width, self.max_y_pix * self.laser_width))

        gcode = "G1 Z{:.2f} F1\n".format(height)
        for y in range(0, image.shape[0]):
            logging.info("Processing row {} of {}".format(y, self.max_y_pix))
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
                    gcode += "G0 F1 X{:.2f} Y{:.2f} E0.00\n".format(x, y, self.extrude)
            else:
                if state is True:
                    state = False
                    self.extrude += extruding_amount
                    extruding_amount = 0
                    (x, y) = self._to_real(last_pos, current_row)
                    gcode += "G1 F1 X{:.2f} Y{:.2f} E{:.2f}\n".format(x, y, self.extrude)
            last_pos = column_pos
        if state is True:
            self.extrude += extruding_amount
            (x, y) = self._to_real(column_pos, current_row)
            gcode += "G1 F1 X{:.2f} Y{:.2f} E{:.2f}\n".format(x, y, self.extrude)
        return gcode


    def _to_real(self, x, y):
        x_pos = float(x * self.laser_width) - (((self.max_x_pix - 1) * self.laser_width) / 2.0)
        y_pos = float((self.max_y_pix - y) * self.laser_width) - (((self.max_y_pix + 1) * self.laser_width) / 2.0)
        logging.debug('{:4.2f} -> {:4.2f} :: {:4.2f} -> {:4.2f}'.format(x, x_pos, y, y_pos))
        return (x_pos, y_pos)


    def _add_border(self, image):
        vborder = np.zeros((image.shape[0], 1, image.shape[2]))
        toped = np.append(vborder, image, axis=1)
        bottomed = np.append(toped, vborder, axis=1)
        hborder = np.zeros((1, bottomed.shape[1], bottomed.shape[2]))
        lefted = np.append(hborder, bottomed, axis=0)
        righted = np.append(lefted, hborder, axis=0)
        return righted

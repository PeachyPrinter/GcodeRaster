import unittest
import logging
from mock import patch, mock_open
import os
import os.path
import sys
import scipy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from raster import Raster, ImageRaster


@patch('raster.ImageRaster')
class RasterTest(unittest.TestCase):

    def test_init_file_should_setup_image_raster_with_defaults(self, mockImageRaster):
        Raster()
        mockImageRaster.assert_called_with(0.5, True)

    @patch.object(os.path, 'isfile')
    @patch.object(scipy.ndimage, 'imread')
    def test_process_file_should_call_image_raster_when_file_exists(self, mock_imread, mock_isfile, mockImageRaster):
        mock_isfile.return_value = True
        mock_imread.return_value = "SomeArray"
        mock_file_raster = mockImageRaster.return_value
        with patch('raster.open', mock_open(), create=True):
            rasterer = Raster()
            rasterer.process_file("test0.png")
        mock_file_raster.process.assert_called_with('SomeArray')

    @patch.object(os.path, 'isfile')
    @patch.object(scipy.ndimage, 'imread')
    def test_process_file_should_write_output_to_file(self, mock_imread, mock_isfile, mockImageRaster):
        output_file = 'out.gcode'
        output_data = "some_gcode"
        mock_isfile.return_value = True
        mock_imread.return_value = "SomeArray"
        mock_file_raster = mockImageRaster.return_value
        mock_file_raster.process.return_value = output_data
        mocked_open = mock_open()

        with patch('raster.open', mocked_open, create=True):
            rasterer = Raster(output_file_name=output_file)
            rasterer.process_file("test0.png")
            mocked_open.assert_called_with(output_file, 'w')
            mocked_open.return_value.write.assert_called_with(output_data)
        mock_file_raster.process.assert_called_with('SomeArray')

    def test_process_file_should_not_call_file_raster_when_file_does_not_exists(self, mockImageRaster):
        mock_file_raster = mockImageRaster.return_value
        with patch('raster.open', mock_open(), create=True):
            rasterer = Raster()
            with self.assertRaises(IOError):
                rasterer.process_file("test1.png")
        self.assertEquals(0, mock_file_raster.process.call_count)

class ImageRasterTest(unittest.TestCase):
    def process_should_return_gcode_for_image(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level='DEBUG')
    unittest.main()

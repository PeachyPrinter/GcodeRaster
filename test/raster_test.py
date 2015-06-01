import unittest
import logging
from mock import patch
import os
import os.path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from raster import Raster, FileRaster


@patch('raster.FileRaster')
class RasterTest(unittest.TestCase):

    def test_init_file_should_setup_file_raster_with_defaults(self, mockFileRaster):
        Raster()
        mockFileRaster.assert_called_with(0.5, True)

    @patch.object(os.path, 'isfile')
    def test_process_file_should_call_file_raster_when_file_exists(self, mock_isfile, mockFileRaster):
        mock_isfile.return_value = True
        mock_file_raster = mockFileRaster.return_value
        rasterer = Raster()
        rasterer.process_file("test0.png")
        mock_file_raster.process.assert_called_with('test0.png')

    def test_process_file_should_not_call_file_raster_when_file_does_not_exists(self, mockFileRaster):
        mock_file_raster = mockFileRaster.return_value
        rasterer = Raster()
        with self.assertRaises(IOError):
            rasterer.process_file("test1.png")
        self.assertEquals(0, mock_file_raster.process.call_count)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level='DEBUG')
    unittest.main()

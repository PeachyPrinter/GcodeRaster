from setuptools import setup, find_packages
from VERSION import version


setup(
    name='PeachyPrinterGcodeRaster',
    version=version,
    description='Tool Set for make images and folders of images into gcode',
    options={},
    url="http://www.peachyprinter.com",
    author="Peachy Printer",
    author_email="software+gcoderaster@peachyprinter.com",
    package_data={},
    install_requires=['scipy', 'numpy', 'PIL'],
    packages=find_packages(),
    py_modules=['VERSION'],
    include_package_data=True
      )

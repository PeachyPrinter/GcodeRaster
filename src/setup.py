from setuptools import setup, find_packages
try:
    from VERSION import version
except ImportError:
    version = "Development"

setup(
    name='PeachyRaster',
    version=version,
    description='Tool Set for make images and folders of images into gcode',
    options={},
    url="http://www.peachyprinter.com",
    author="Peachy Printer",
    author_email="software+gcoderaster@peachyprinter.com",
    package_data={},
    install_requires=['numpy', 'pillow'],
    packages=find_packages(),
    py_modules=['VERSION'],
    include_package_data=True,
    entry_points={'console_scripts': ['peachyraster=peachyraster.peachyraster:main']},
      )

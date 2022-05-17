"""
    VIPS Adapter

    An adapter that uses pyvips, the Python extension of the libvips library, to implement image reading behavior
    Adapter currently mapped to reading .tif, tiff files
"""

import numpy as np

try:
    import pyvips
except Exception as e:
    print("You have an issue with your pyvips installation, it may be because of the dependency on libvips. Contact Adin at adinbsolomon@gmail.com with any questions!")
    raise e

from .adapter import Adapter
from . import config

FORMAT_TO_DTYPE = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128
}


class VIPS(Adapter):

    def __init__(self, filepath: str):
        """__init__ Initialize VIPS adapter object

        :param filepath: Filepath to image file to be opened
        :type filepath: str
        """
        self._image = pyvips.Image.new_from_file(filepath, access="random")

    def get_width(self) -> int:
        """get_height Get the height property of the image using VIPS' implementation

        :return: Height in pixels
        :rtype: int
        """
        return self._image.width

    def get_height(self) -> int:
        """get_height Get the height property of the image using VIPS' implementation

        :return: Height in pixels
        :rtype: int
        """
        return self._image.height

    def get_region(self, region_coordinates, region_dims) -> np.ndarray:
        """get_region Get a pixel region of the image using VIPS' implementation

        :param region_coordinates: A set of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: Iterable
        :param region_dims: A set of (width, height) coordinates representing the region dimensions
        :type region_dims: Iterable
        :return: A numpy array representative of the pixel region from the image
        :rtype: np.ndarray
        """
        if config.VIPS_GET_REGION == "IMAGE_CROP":
            output_img = self._image.crop(*region_coordinates, *region_dims)
            np_output = np.ndarray(
                buffer=output_img.write_to_memory(),
                dtype=FORMAT_TO_DTYPE[output_img.format],
                shape=[output_img.height, output_img.width, output_img.bands]
            )
            return np_output
        elif config.VIPS_GET_REGION == "REGION_FETCH":
            vips_region = pyvips.Region.new(self._image)
            bytestring_buffer = vips_region.fetch(
                *region_coordinates, *region_dims)
            np_output = np.frombuffer(bytestring_buffer, dtype=np.uint8)
            region = np_output.reshape(*region_dims, 3)
            return region
        else:
            raise Exception(
                f"Invalid vips get region mode {config.VIPS_GET_REGION=}")

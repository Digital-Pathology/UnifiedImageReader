"""
    SlideIO Adapter

    An adapter that uses the SlideIO library to implement image reading behavior
    Adapter currently mapped to reading .svs files
"""
import numpy as np

try:
    import slideio
except Exception as e:
    print("You have an issue with your SlideIO installation, it may be because of the dependency on Openslide. Contact Adin at adinbsolomon@gmail.com with any questions!")
    raise e

from .adapter import Adapter


class SlideIO(Adapter):

    def __init__(self, filepath):
        """__init__ Initialize SlideIO adapter object

        :param filepath: Filepath to image file to be opened
        :type filepath: str
        """

        self._image = slideio.open_slide(filepath, "SVS").get_scene(0)

    def get_width(self):
        """get_width Get the width property of the image using SlideIO's implementation

        :return: Height in pixels
        :rtype: int
        """
        return self._image.size[0]

    def get_height(self):
        """get_height Get the height property of the image using SlideIO's implementation

        :return: Width in pixels
        :rtype: int
        """
        return self._image.size[1]

    def get_region(self, region_coordinates, region_dims) -> np.ndarray:
        """get_region Get a pixel region of the image using SlideIO's implementation

        :param region_coordinates: A set of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: Iterable
        :param region_dims: A set of (width, height) coordinates representing the region dimensions
        :type region_dims: Iterable
        :return: A numpy array representative of the pixel region from the image
        :rtype: np.ndarray
        """
        """ Calls the read_block method of a SlideIO Scene object to create an unscaled rectangular region of the image as a numpy array """
        np_array = self._image.read_block((*region_coordinates, *region_dims))
        return np_array

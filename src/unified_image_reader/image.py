
"""
    Image

    1) Provide a filepath, and optionally a reader interface for the image file
    2) Include functionality for reading regions from the image
    3) Include functionality for counting the number of regions and the image's dimensions
"""

import numpy as np

from .image_reader import ImageReader

DEFAULT_REGION_DIMS = (512, 512)


class Image(object):

    """ An image to be streamed into a specialized reader """

    def __init__(self, filepath, reader=None):
        """
        Initialize Image object

        Parameters:
            filepath (str): Filepath to image file to be opened
            reader: Object that serves as an interface to reading the image file (optional)
        """
        self.filepath = filepath
        self.reader = reader or ImageReader(filepath)

    def get_region(self, region_identifier, region_dims=DEFAULT_REGION_DIMS) -> np.ndarray:
        """
        Get a rectangular region from the image

        Parameters:
            region_identifier(Tuple[int]| int): An (x,y) coordinate tuple or an indexed region based on region dimensions
            region_dims (Tuple[int]): An (x,y) coordinate tuple representing the region dimensions, which are 512x512 by default (optional)

        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims=DEFAULT_REGION_DIMS) -> int:
        """
        Get total number of regions from the image based on region dimensions

        Parameters:
            region_dims (Tuple[int]): Region dimensions which are 512x512 by default (optional)
        
        Returns:
            int: Number of regions in the image
        """
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self):
        return self.reader.width

    @property
    def height(self):
        return self.reader.height

    @property
    def dims(self):
        return self.width, self.height

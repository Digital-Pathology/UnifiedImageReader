
"""
    An interface into optimized image reading behavior with optional overriding.
"""

import contextlib
from typing import Optional

import numpy as np

from . import config
from . import image_reader


class Image(contextlib.AbstractContextManager):

    """ 
    Image An image to be streamed into a specialized reader 
    """

    def __init__(self, filepath, reader=None):
        """__init__ Initialize Image object

        :param filepath: Filepath to image file to be opened
        :type filepath: str
        :param reader: Interface to reading the image file, defaults to None
        :type reader: ImageReader or custom class supportive of the same functions, optional
        """
        self.filepath = filepath
        self.reader = reader or image_reader.ImageReader(filepath)
        self._iter = None

    def get_region(self, region_identifier, region_dims=config.DEFAULT_REGION_DIMS) -> np.ndarray:
        """
        get_region Get a pixel region from the image

        :param region_identifier: A  set of (width, height) coordinates or an indexed region based on region dimensions
        :type region_identifier: Union[int, Iterable]
        :param region_dims: A set of (width, height) coordinates representing the region dimensions, defaults to DEFAULT_REGION_DIMS
        :type region_dims: Iterable, optional
        :return: A numpy array representative of the pixel region from the image
        :rtype: np.ndarray
        """
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims=config.DEFAULT_REGION_DIMS) -> int:
        """
        number_of_regions Get total number of regions from the image based on region dimensions

        :param region_dims: A set of (width, height) coordinates representing the region dimensions, defaults to DEFAULT_REGION_DIMS
        :type region_dims: Iterable, optional
        :return: Number of regions in the image
        :rtype: int
        """
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self):
        """
        width Get the width property of the image using its reader

        :return: Width in pixels
        :rtype: int
        """
        return self.reader.width

    @property
    def height(self):
        """
        height Get the height property of the image using its reader

        :return: Height in pixels
        :rtype: int
        """
        return self.reader.height

    @property
    def dims(self):
        """
        dims Get the width and height properties of the image

        :return: Width and height in pixels
        :rtype: Tuple[int]
        """
        return self.width, self.height

    def __iter__(self):
        """
        __iter__ Initialize Image object iterator

        :raises Exception: Iterator already initialized but is called again
        :return: Iterator for Image object
        :rtype: Image
        """
        self._iter = 0
        return self

    def __next__(self):
        """
        __next__ Get the next pixel region index in a sequence of iterating through an Image object

        :raises StopIteration: Iterator has reached the last region in the image
        :return: Next pixel region index
        :rtype: int
        """
        if self._iter >= self.number_of_regions():
            raise StopIteration
        else:
            region = self.get_region(self._iter)
            self._iter += 1
            return region

    def __len__(self):
        """
        __len__ Get the number of pixel regions in an iterable sequence of an Image object

        :return: The number of pixel regions in the Image object
        :rtype: int
        """
        return self.number_of_regions()

    def __exit__(self, **kwargs) -> Optional[bool]:
        return super().__exit__(**kwargs)

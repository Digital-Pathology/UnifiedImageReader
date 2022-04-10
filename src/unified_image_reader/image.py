
"""
    Image

    1) Provide a filepath, and optionally a reader interface for the image file
    2) Include functionality for reading regions from the image
    3) Include functionality for counting the number of regions and the image's dimensions
"""

import contextlib
from types import TracebackType
from typing import Any, Optional, Type

import numpy as np

from . import config
from . import image_reader
from . import util


class Image(contextlib.AbstractContextManager):

    """ An image to be streamed into a specialized reader """

    def __init__(self, filepath: util.FilePath, reader: Optional[image_reader.ImageReader] = None):
        """
        Initialize Image object

        Parameters:
            filepath (str): Filepath to image file to be opened
            reader: Object that serves as an interface to reading the image file (optional)
        """
        self.filepath = filepath
        self.reader = reader or image_reader.ImageReader(filepath)
        self._iter = None

    def get_region(self, region_identifier: util.RegionIdentifier, region_dims: util.RegionDimensions = config.DEFAULT_REGION_DIMS) -> np.ndarray:
        """
        Get a rectangular region from the image

        Parameters:
            region_identifier(Tuple[int]| int): An (x,y) coordinate tuple or an indexed region based on region dimensions
            region_dims (Tuple[int]): An (x,y) coordinate tuple representing the region dimensions, which are 512x512 by default (optional)

        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims: util.RegionDimensions = config.DEFAULT_REGION_DIMS) -> int:
        """
        Get total number of regions from the image based on region dimensions

        Parameters:
            region_dims (Tuple[int]): Region dimensions which are 512x512 by default (optional)

        Returns:
            int: Number of regions in the image
        """
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self) -> int:
        return self.reader.width

    @property
    def height(self) -> int:
        return self.reader.height

    @property
    def dims(self) -> util.RegionDimensions:
        return self.width, self.height

    def __iter__(self):
        if self._iter is not None:
            raise Exception(type(self._iter), self._iter)
        else:
            self._iter = 0
        return self

    def __next__(self):
        if self._iter >= self.number_of_regions():
            raise StopIteration
        else:
            region = self.get_region(self._iter)
            self._iter += 1
            return region

    def __len__(self):
        return self.number_of_regions()

    def __exit__(self, **kwargs) -> Optional[bool]:
        return super().__exit__(**kwargs)

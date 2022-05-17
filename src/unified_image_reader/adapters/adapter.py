"""
    Adapter

    An implementation of image reading behavior that may map specific libraries to working with specific image formats
"""
import abc
from typing import Iterable

import numpy as np


class Adapter(abc.ABC):

    @abc.abstractmethod
    def get_region(self, region_coordinates: Iterable, region_dims: Iterable) -> np.ndarray:
        """get_region Get a pixel region of the image using the adapter library's implementation

        :param region_coordinates: A set of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: Iterable
        :param region_dims: A set of (width, height) coordinates representing the region dimensions
        :type region_dims: Iterable
        :return: A numpy array representative of the pixel region from the image
        :rtype: np.ndarray
        """
        pass

    @abc.abstractmethod
    def get_width() -> int:
        """
        Get the width property of the image using the adapter library's implementation
        """
        pass

    @abc.abstractmethod
    def get_height() -> int:
        """
        Get the height property of the image using the adapter library's implementation
        """
        pass

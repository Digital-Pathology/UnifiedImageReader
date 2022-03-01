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
        """ 
        Get a rectangular region from the image

        Parameters:
            region_coordinates(Tuple[int]): An (x,y) coordinate tuple representing the top-left pixel of the region
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region

        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """ 
        pass

    @abc.abstractmethod
    def get_width() -> int: 
        """ Get the width of the image """
        pass

    @abc.abstractmethod
    def get_height() -> int:
        """ Get the height of the image """ 
        pass

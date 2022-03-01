"""
    Image Reader

    1) Give it a filepath for a supported image format, and optionally an adapter to operate on the image file
    2) If an adapter is not provided as an argument, one will be created from a mapping of formats to adapters
    3) Include utility methods for validation and extraction of region parameters
    4) Include functionality for getting image regions using the reading behavior of an adapter
"""

import os
from typing import Iterable, Union
import numpy as np

from unified_image_reader.adapters import Adapter, VIPS

FORMAT_ADAPTER_MAP = {
    "tif": VIPS,
    "tiff": VIPS
}

class UnsupportedFormatException(Exception): pass
class InvalidCoordinatesException(Exception): pass
class InvalidDimensionsException(Exception): pass

class ImageReader():

    """ Interface for adapters which specify reading behavior """

    def __init__(self, filepath: str, adapter: Union[Adapter, None] = None):
        """
        Initialize ImageReader object

        Parameters:
            filepath (str): Filepath to image file to be opened
            adapter(Adapter | None): Object which specifies reading behavior (optional)

        """
        # process filepath
        assert os.path.isfile(filepath), f"filepath is not a file --> {filepath}"
        self.filepath = filepath
        # initialize the adapter
        self.adapter = None
        if adapter is None: # choose based on file format
            image_format = self.filepath.split('.')[-1]
            adapter = FORMAT_ADAPTER_MAP.get(image_format)
            if adapter is None:
                raise UnsupportedFormatException(image_format)
        self.adapter = adapter(filepath)
    
    def get_region(self, region_identifier: Union[int, Iterable], region_dims: Iterable):
        """
        Get a rectangular region from an image using an adapter's implementation after validating and extracting region data

        Parameters:
            region_identifier(int | Tuple[int]): An (x,y) coordinate tuple or an indexed region based on region dimensions
            region_dims(Tuple[int]): An (x,y) coordinate tuple representing the region dimensions
        
        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """
        # Make sure that region_coordinates is a tuple of length 2
        region_coordinates = None
        if isinstance(region_identifier, int):
            region_coordinates = self.region_index_to_coordinates(region_identifier, region_dims)
        elif isinstance(region_identifier, Iterable):
            assert (len(region_identifier) == 2)
            region_coordinates = region_identifier
        # make sure that the region is in bounds
        self.validate_region(region_coordinates, region_dims)
        # call the implementation
        return self._get_region(region_coordinates, region_dims)

    def _get_region(self, region_coordinates, region_dims) -> np.ndarray:
        """
        Call an adapter's implementation to get a rectangular image region

        Parameters:
            region_coordinates(Tuple[int]): An (x,y) coordinate tuple representing the top-left pixel of the region
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region
        
        Returns:
            np.ndarray: A numpy array representative of the rectangular region from the image
        """ 
        return self.adapter.get_region(region_coordinates, region_dims)

    def number_of_regions(self, region_dims: Iterable):
        """
        Calculates the number of regions in the image based on the dimensions of each region

        Parameters:
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region

        Returns:
            int: The number of regions
        """
        width, height = region_dims
        return (self.width // width) * (self.height // height)

    def validate_region(self, region_coordinates: Iterable, region_dims: Iterable) -> None:
        """
        Checks that a region is within the bounds of the image 

        Parameters:
             region_coordinates(Tuple[int]): An (x,y) coordinate tuple representing the top-left pixel of the region
             region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region
        """
        def not_valid():
            """ Wrapper function to raise an error on invalid coordinates or dimensions"""
            raise IndexError(region_coordinates, region_dims, self.dims)
        # first ensure coordinates are in bounds
        if not (len(region_coordinates) == 2): raise InvalidCoordinatesException(region_coordinates)
        left, top = region_coordinates
        if not (0 <= left < self.width): not_valid()
        if not (0 <= top < self.height): not_valid()
        # then check dimensions with coordinates
        if not (len(region_dims) == 2): raise InvalidDimensionsException(region_dims)
        region_width, region_height = region_dims
        if not (0 < region_width and left+region_width <= self.width): not_valid()
        if not (0 < region_height and top+region_height <= self.height): not_valid()

    def region_index_to_coordinates(self, region_index: int, region_dims: Iterable):
        """
        Converts the index of a region to coordinates of the top-left pixel of the region

        Parameters:
            region_index(int): The nth region of the image (where n >= 0) based on region dimensions
            region_dims(Tuple[int]): A tuple representing the width and height dimensions of the region
        
        Returns:
            Tuple(int): An (x,y) coordinate tuple representing the top-left pixel of the region
        """
        region_width, region_height = region_dims
        width_regions = self.width // region_width
        left = (region_index % width_regions) * region_width
        top = (region_index // width_regions) * region_height
        return (left, top)

    @property
    def width(self):
        return self.adapter.get_width()

    @property
    def height(self):
        return self.adapter.get_height()
    
    @property
    def dims(self):
        return self.width, self.height

"""
    An ImageReader controls the behavior of the image interface. It can either utilize an adapter on a library or custom behavior.
"""

import os
from typing import Any, Iterable, Optional, Tuple, Union

import cv2 as cv
import numpy as np

from unified_image_reader.adapters import Adapter, SlideIO, VIPS
from .exceptions import InvalidCoordinatesException, InvalidDimensionsException, UnsupportedFormatException
from .types import RegionIndex, is_region_index, RegionCoordinates, is_region_coordinates, RegionDimensions, is_region_dimensions, ImageAsNumpyArray

FORMAT_ADAPTER_MAP = {
    "tif": VIPS,
    "tiff": VIPS,
    "svs": SlideIO
}


class ImageReader():
    """
    ImageReader Interface between images and adapters which specify reading behavior

    :raises UnsupportedFormatException: The adapter does not support the image format
    :raises TypeError: Enforces provided type hinting for region_identifier arguments
    :raises IndexError: The top-left pixel or pixel region dimensions are out of bounds of the image dimensions
    :raises InvalidCoordinatesException: The top-left pixel rwas not provided in (width, height) format
    :raises InvalidDimensionsException: Dimensions of the pixel region were not provided in (width, height) format
    """

    def __init__(self, filepath: str, adapter: Optional[Adapter] = None):
        """
        __init__ Initialize ImageReader object

        :param filepath: Filepath to image file to be opened
        :type filepath: str
        :param adapter: Object which specifies reading behavior, defaults to None (automatically selected based on filepath)
        :type adapter: Optional[Adapter], optional
        :raises UnsupportedFormatException: The adapter does not support the image format
        """
        # process filepath
        assert os.path.isfile(
            filepath), f"filepath is not a file --> {filepath}"

        self.filepath = filepath
        # initialize the adapter
        self.adapter = None
        if adapter is None:  # choose based on file format
            image_format = self.filepath.split('.')[-1]
            adapter = FORMAT_ADAPTER_MAP.get(image_format)
            if adapter is None:
                raise UnsupportedFormatException(image_format)
        self.adapter = adapter(filepath)

    def get_region(self, region_identifier: Union[RegionIndex, RegionCoordinates], region_dims: RegionDimensions):
        """
        get_region Get a pixel region from an image using an adapter's implementation after validation and extracting region data

        :raises TypeError: The starting pixels or pixel regions are out of bounds of the image dimensions
        :param region_identifier: A tuple of (width, height) coordinates or an indexed region based on region dimensions
        :type region_identifier: Union[int, Iterable]
        :param region_dims: A set of (weight, height) coordinates representing the region dimensions
        :type region_dims: Iterable
        :return: A numpy array representative of the pixel region from the image
        :rtype: np.ndarray
        """
        region_coordinates = None
        if is_region_index(region_identifier):
            region_coordinates = self.region_index_to_coordinates(
                region_identifier, region_dims)
        elif is_region_coordinates(region_identifier):
            region_coordinates = region_identifier
        else:
            raise_type_error(region_identifier)
        # make sure that the region is in bounds
        self.validate_region(region_coordinates, region_dims)
        # call the implementation
        return self._get_region(region_coordinates, region_dims)

    def _get_region(self, region_coordinates: RegionCoordinates, region_dims: RegionDimensions) -> ImageAsNumpyArray:
        """
        _get_region Call an adapter's implementation to get a pixel region from an image

        :param region_coordinates: A tuple of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: RegionCoordinates
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :return: Implementation resulting in a numpy array representative of the pixel region from the image
        :rtype: ImageAsNumpyArray
        """

        return self.adapter.get_region(region_coordinates, region_dims)

    def number_of_regions(self, region_dims: Iterable):
        """
        number_of_regions Calculates the number of regions in the image based on the dimensions of each region

        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :return: The number of regions
        :rtype: int
        """

        width, height = region_dims
        return (self.width // width) * (self.height // height)

    def validate_region(self, region_coordinates: RegionCoordinates, region_dims: RegionDimensions) -> None:
        """
        validate_region Checks that a region is within the bounds of the image

        :param region_coordinates: A tuple of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: RegionCoordinates
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :raises IndexError: The top-left pixel or pixel region dimensions are out of the bounds of the image dimensions
        :raises InvalidCoordinatesException: The top-left pixel was not presented in (width, height) format
        :raises InvalidDimensionsException: Dimensions of the pixel region were not presented in (width, height) format
        """

        def not_valid():
            """
            not_valid Wrapper function to raise an error on invalid coordinates or dimensions

            :raises IndexError: The top-left pixel or pixel region dimensions are out of the bounds of the image dimensions
            """

            raise IndexError(region_coordinates, region_dims, self.dims)
        # first ensure coordinates are in bounds
        if not (len(region_coordinates) == 2):
            raise InvalidCoordinatesException(region_coordinates)
        left, top = region_coordinates
        if not (0 <= left < self.width):
            not_valid()
        if not (0 <= top < self.height):
            not_valid()
        # then check dimensions with coordinates
        if not (len(region_dims) == 2):
            raise InvalidDimensionsException(region_dims)
        region_width, region_height = region_dims
        if not (0 < region_width and left+region_width <= self.width):
            not_valid()
        if not (0 < region_height and top+region_height <= self.height):
            not_valid()

    def region_index_to_coordinates(self, region_index: RegionIndex, region_dims: RegionDimensions) -> RegionCoordinates:
        """
        region_index_to_coordinates converts the index of a region to coordinates of the top-left pixel of the region

        :param region_index: The nth region of the image (where n >= 0) based on region dimensions
        :type region_index: RegionIndex
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :return: A tuple of (width, height) coordinates representing the top-left pixel of the region
        :rtype: RegionCoordinates
        """
        region_width, region_height = region_dims
        width_regions = self.width // region_width
        left = (region_index % width_regions) * region_width
        top = (region_index // width_regions) * region_height
        return (left, top)

    @property
    def width(self):
        """
        width Get the width property of the image using the adapter's implementation

        :return: Width in pixels
        :rtype: int
        """
        return self.adapter.get_width()

    @property
    def height(self):
        """
        height Get the height property of the image using the adapter's implementation

        :return: Height in pixels
        :rtype: int
        """
        return self.adapter.get_height()

    @property
    def dims(self):
        """
        dims Get the width and height property of the image using the adapter's implementation

        :return: Width and height in pixels
        :rtype: Iterable
        """
        return self.width, self.height


class ImageReaderDirectory(ImageReader):

    """
     Treats a collection of images as a single image whereby regions don't have locations, only alphabetically-organized indices.
     This works with both a directory and a list of image files.
    """

    def __init__(self, data: Union[str, list, tuple]):
        """
        __init__

        :param data: the location(s) of constituent images
        :type data: str
        :raises Exception: when data is a string but isn't a directory
        :raises TypeError: when data is neither a string nor list/tuple
        :raises Exception: when a file in data (when data is a list) doesn't exist as a file 
        """
        if isinstance(data, str):
            self._dir = data
            if not os.path.isdir(self._dir):
                raise Exception(f"{data=} should be a path to a directory")
            self._region_files = [os.path.join(
                self._dir, p) for p in os.listdir(self._dir)]
        elif isinstance(data, [list, tuple]):
            self._region_files = data
            for region_filepath in self._region_files:
                if not os.path.isfile(region_filepath):
                    raise Exception(
                        f"self._region_files should be composed of filepaths to existing image files but includes {region_filepath}")
        else:
            raise TypeError(f"Didn't expect {type(data)=}, {data=}")
        self._region_files.sort()

    def get_region(self, region_identifier: RegionIndex, region_dims: Optional[RegionDimensions] = None) -> ImageAsNumpyArray:
        """
        get_region reads in the image at self._region_files[region_identifier]

        :param region_identifier: the index of the file read (files are indexed alphabetically)
        :type region_identifier: RegionIndex
        :param region_dims: IGNORED - the regions will be whatever the regions of the image file are, defaults to None
        :type region_dims: Optional[RegionDimensions], optional
        :raises NotImplementedError: if the region identifier isn't an index
        :raises IndexError: if region_identifier isn't in range
        :return: region (the image in the file in question)
        :rtype: ImageAsNumpyArray
        """
        if not isinstance(region_identifier, RegionIndex):
            raise NotImplementedError(
                "This ImageReader only operates on aggregated region files which are indexed alphabetically. Region coordinates are not supported.")
        if not (0 <= region_identifier < self.number_of_regions()):
            raise IndexError(
                f"{region_identifier=}, {self.number_of_regions()=}")
        region_filepath = self._region_files[region_identifier]
        return cv.imread(region_filepath)

    def number_of_regions(self, region_dims: Optional[RegionDimensions] = None) -> int:
        """
        number_of_regions the number of region in the image (in this case, the number of image files)

        :param region_dims: IGNORED - the dimensions of the regions in this image are the dimensions of the image in the files, defaults to None
        :type region_dims: Optional[RegionDimensions], optional
        :return: the number of regions in this image (the number of the image files)
        :rtype: int
        """
        return len(self._region_files)

    @property
    def width(self):
        raise NotImplementedError()

    @property
    def height(self):
        raise NotImplementedError()

    @property
    def dims(self):
        raise NotImplementedError()

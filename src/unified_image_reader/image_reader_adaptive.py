"""
    AdaptiveImageReader is an ImageReader and chooses the best library for the job.
"""

from typing import Union

from unified_image_reader.adapters import Adapter, SlideIO, VIPS
from .exceptions import UnsupportedFormatException
from .image_reader import ImageReader
from .types import raise_type_error, RegionIndex, is_region_index, RegionCoordinates, is_region_coordinates, RegionDimensions, is_region_dimensions, Region


FORMAT_ADAPTER_MAP = {
    "tif": VIPS,
    "tiff": VIPS,
    "svs": SlideIO
}


class ImageReaderAdaptive(ImageReader):
    """
    ImageReaderAdaptive applies a strategy pattern for reading images using memory-efficient libraries. The adapter is not chosen until necessary so the user has an opportunity to choose one themselves.

    :raises UnsupportedFormatException: When no adapter is available for the given image
    :raises TypeError: When region identification, region coordinates/dimension validation fails, or adapter is invalid
    :raises IndexError: When the identified region is not within the image
    """

    def __init__(self, filepath: str):
        """
        __init__ Initialize ImageReader object

        :param filepath: Filepath to image file to be opened
        :type filepath: str
        """
        super().__init__(filepath)
        # self._adapter (accessed by self.adapter) is unset by default so that the user can optionally override it.
        self._adapter = None

    def get_region(self, region_identifier: Union[RegionIndex, RegionCoordinates], region_dims: RegionDimensions) -> Region:
        """
        get_region from an image using an adapter's implementation after validating the region bounds

        :param region_identifier: A tuple of (width, height) coordinates or a region index based on region_dims
        :type region_identifier: Union[RegionIndex, RegionCoordinates]
        :param region_dims: A tuple of (weight, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :raises TypeError: The starting pixels or pixel regions are out of bounds of the image dimensions
        :return: A numpy array representative of the pixel region from the image
        :rtype: ImageAsNumpyArray
        """
        region_coordinates = None
        if is_region_index(region_identifier):
            region_coordinates = self._region_index_to_coordinates(
                region_identifier, region_dims)
        elif is_region_coordinates(region_identifier):
            region_coordinates = region_identifier
        else:
            raise_type_error(region_identifier)
        # make sure that the region is in bounds
        self._validate_region(region_coordinates, region_dims)
        # call the implementation
        return self._get_region(region_coordinates, region_dims)

    def number_of_regions(self, region_dims: RegionDimensions) -> int:
        """
        number_of_regions calculates the number of complete regions in the image based on region_dims.

        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :return: The number of regions
        :rtype: int
        """
        width, height = region_dims
        return (self.width // width) * (self.height // height)

    def _validate_region(self, region_coordinates: RegionCoordinates, region_dims: RegionDimensions) -> None:
        """
        validate_region Checks that a region is within the bounds of the image

        :param region_coordinates: A tuple of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: RegionCoordinates
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :raises IndexError: The top-left pixel or pixel region dimensions are out of the bounds of the image dimensions
        :raises TypeError: if region_coordinates or region_dims are not the correct type
        """
        def not_valid():
            """
            not_valid raises an error on invalid coordinates or dimensions

            :raises IndexError: The top-left pixel or pixel region dimensions are out of the bounds of the image dimensions
            """
            raise IndexError(region_coordinates, region_dims, self.dims)
        if not is_region_coordinates(region_coordinates):
            raise_type_error(region_coordinates)
        if not is_region_dimensions(region_dims):
            raise_type_error(region_dims)
        # first ensure coordinates are in bounds
        left, top = region_coordinates
        if not (0 <= left < self.width):
            not_valid()
        if not (0 <= top < self.height):
            not_valid()
        # then check dimensions with coordinates
        region_width, region_height = region_dims
        if not (0 < region_width and left+region_width <= self.width):
            not_valid()
        if not (0 < region_height and top+region_height <= self.height):
            not_valid()

    def _get_region(self, region_coordinates: RegionCoordinates, region_dims: RegionDimensions) -> Region:
        """
        _get_region calls an adapter's implementation to get a pixel region from an image

        :param region_coordinates: A tuple of (width, height) coordinates representing the top-left pixel of the region
        :type region_coordinates: RegionCoordinates
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions
        :type region_dims: RegionDimensions
        :return: Implementation resulting in a numpy array representative of the pixel region from the image
        :rtype: Region
        """
        return self.adapter.get_region(region_coordinates, region_dims)

    def _region_index_to_coordinates(self, region_index: RegionIndex, region_dims: RegionDimensions) -> RegionCoordinates:
        """
        _region_index_to_coordinates converts the index of a region to coordinates of the top-left pixel of the region

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
        width gets the width property of the image using the adapter's implementation

        :return: Width in pixels
        :rtype: int
        """
        return self.adapter.get_width()

    @property
    def height(self):
        """
        height gets the height property of the image using the adapter's implementation

        :return: Height in pixels
        :rtype: int
        """
        return self.adapter.get_height()

    @property
    def dims(self):
        """
        dims gets the width and height property of the image using the adapter's implementation

        :return: Width and height in pixels
        :rtype: Iterable
        """
        return self.width, self.height

    @property
    def adapter(self):
        """
        adapter used by ImageReaderAdaptive to read the image data
        """
        if self._adapter is None:
            # initialize the adapter based on file format
            image_format = self.filepath.split('.')[-1]
            adapter = FORMAT_ADAPTER_MAP.get(image_format)
            if adapter is None:
                raise UnsupportedFormatException(image_format)
            self.adapter = adapter(self.filepath)
        return self._adapter

    @adapter.setter
    def adapter(self, new_adapter: Adapter):
        """
        adapter allows the user to manually choose the adapter for the ImageReaderAdaptive to use

        :param new_adapter: the adapter to use
        :type new_adapter: Adapter
        """
        if not isinstance(new_adapter, Adapter):
            raise_type_error(new_adapter)
        self._adapter = new_adapter

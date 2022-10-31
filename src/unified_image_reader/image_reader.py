"""
    An ImageReader controls the behavior of the image interface: AdaptiveImageReader chooses the best library for the job.
"""

from abc import ABC, abstractmethod
import os

from .exceptions import FileDoesNotExistException
from .types import RegionIdentifier, RegionDimensions, Region, ImageDimensions


class ImageReader(ABC):
    """
    AbstractBaseClass defining the interface for reading large and/or composite images

    :raises FileDoesNotExistException: if filepath given to initializer doesn't exist or is not a file
    :raises NotImplementedError: When a function is not overridden properly
    """

    def __init__(self, filepath: str):
        """
        __init__ verifies the filepath and may be overridden

        :param filepath: the location of the image in question
        :type filepath: str
        :raises FileDoesNotExistException: if filepath either doesn't exist or is not a file
        """
        if not os.path.exists(filepath):
            raise FileDoesNotExistException(f"{filepath=}")
        if not os.path.isfile(filepath):
            raise FileDoesNotExistException(f"{filepath=}")
        self.filepath = filepath

    @abstractmethod
    def get_region(self, region_identifier: RegionIdentifier, region_dims: RegionDimensions) -> Region:
        """
        get_region should return the region of size region_dims identified by region_identifier

        :param region_identifier: either an index (top-left first) or coordinates identifying the region in the image
        :type region_identifier: RegionIdentifier
        :param region_dims: the dimensions of the region
        :type region_dims: RegionDimensions
        :return: the region in question
        :rtype: Region
        """
        raise NotImplementedError()

    @abstractmethod
    def number_of_regions(self, region_dims: RegionDimensions = None) -> int:
        """
        number_of_regions returns the number of regions (of size region_dims) in the image

        :param region_dims: the size of the regions in the image
        :type region_dims: RegionDimensions
        :return: the number of regions in the image
        :rtype: int
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def width(self) -> int:
        """
        width returns the width of the image

        :rtype: int
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def height(self) -> int:
        """
        heigh returns the height of the image

        :rtype: int
        """
        raise NotImplementedError()

    @property
    def dims(self) -> ImageDimensions:
        """
        dims returns (width, height) of the image

        :rtype: ImageDimensions
        """
        return self.width, self.height

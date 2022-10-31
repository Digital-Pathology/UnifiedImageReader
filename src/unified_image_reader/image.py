
"""
    An interface into reading an image with various methods. The most significant of which is the ImageReaderAdaptive, which identifies which library to use to read an image without loading the entire image into memory.
"""

import contextlib
import os
from typing import Optional
from unified_image_reader.exceptions import FileDoesNotExistException
from unified_image_reader.image_reader import ImageReader
from unified_image_reader.image_reader_adaptive import ImageReaderAdaptive
from unified_image_reader.image_reader_directory import ImageReaderDirectory

from unified_image_reader.types import ImageDimensions, Region, RegionDimensions, RegionIdentifier, raise_type_error

from . import config


class Image(contextlib.AbstractContextManager):

    """
    Image An image to be streamed into a specialized reader 
    """

    def __init__(self, filepath: str):
        """__init__ initializes an Image object

        :param filepath: the filepath of the image in question (may be a directory - see ImageReaderDirectory)
        :type filepath: str
        """
        if not os.path.exists(filepath):
            raise FileDoesNotExistException(filepath)
        self.filepath = filepath
        # lazily initialize self._reader to allow for user election
        self._reader = None
        # self._iter helps with `for region in Image(...):`
        self._iter = None

    def get_region(self, region_identifier: RegionIdentifier, region_dims: RegionDimensions = config.DEFAULT_REGION_DIMS) -> Region:
        """
        get_region Get a region from the image

        :param region_identifier: A tuple of (width, height) coordinates or an indexed region based on region dimensions
        :type region_identifier: RegionIdentifier
        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions, defaults to DEFAULT_REGION_DIMS
        :type region_dims: RegionDimensions, optional
        :return: the region identified by region_identifier
        :rtype: Region
        """
        return self.reader.get_region(region_identifier, region_dims)

    def number_of_regions(self, region_dims: RegionDimensions = config.DEFAULT_REGION_DIMS) -> int:
        """
        number_of_regions gets the total number of regions from the image based on region dimensions

        :param region_dims: A tuple of (width, height) coordinates representing the region dimensions, defaults to DEFAULT_REGION_DIMS
        :type region_dims: RegionDimensions, optional
        :return: the number of regions in the image
        :rtype: int
        """
        return self.reader.number_of_regions(region_dims)

    @property
    def width(self) -> int:
        """
        width gets the width property of the image using its reader

        :rtype: int
        """
        return self.reader.width

    @property
    def height(self) -> int:
        """
        height gets the height property of the image using its reader

        :rtype: int
        """
        return self.reader.height

    @property
    def dims(self) -> ImageDimensions:
        """
        dims gets the width and height properties of the image

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

    @property
    def reader(self):
        """
        reader returns self._reader, which determines how regions are read from self.filepath
        """
        if self._reader is None:
            # set self._reader based on filepath
            if os.path.isfile(self.filepath):
                self._reader = ImageReaderAdaptive(self.filepath)
            elif os.path.isdir(self.filepath):
                self._reader = ImageReaderDirectory(self.filepath)
            else:
                raise FileDoesNotExistException(
                    f"{self.filepath=} is neither a file nor a directory")
        return self._reader

    @reader.setter
    def reader(self, new_reader: ImageReader):
        """
        reader allows the user to manually choose the ImageReader to use for their image

        :type new_reader: ImageReader
        """
        if not isinstance(new_reader, ImageReader):
            raise_type_error(new_reader)
        self._reader = new_reader

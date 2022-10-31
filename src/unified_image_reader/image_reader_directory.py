"""
    ImageReaderDirectory treats a directory of images as a whole-slide image where each image in the directory is a region. Files are sorted.
"""

import os

import cv2 as cv
from unified_image_reader.exceptions import DirectoryDoesNotExistException

from .image_reader import ImageReader
from .types import RegionIndex, is_region_index, Region, raise_type_error, Ignored


class ImageReaderDirectory(ImageReader):

    """
     Treats a collection of images as a single image whereby regions don't have locations, only sort-based indexing.
     This works with both a directory and a list of image files.

     :raises NotImplementedError: When region indexing fails, or image width/height/dims are used
     :raises IndexError: When region indexing fails
    """

    def __init__(self, filepath: str):
        """
        __init__ verifies the that the filepath is a valid directory

        :param filepath: the directory containing the region image files
        :type filepath: str
        :raises TypeError: when filepath is not a str
        :raises DirectoryDoesNotExistException: when filepath doesn't exist or isn't a directory
        """
        if not isinstance(filepath, str):
            raise_type_error(filepath)
        if not os.path.exists(filepath):
            raise DirectoryDoesNotExistException(filepath)
        if not os.path.isdir(filepath):
            raise DirectoryDoesNotExistException(filepath)
        self.filepath = filepath
        # collect the filepaths of those images
        self._region_files = [os.path.join(
            self._dir, p) for p in os.listdir(self._dir)]
        self._region_files.sort()

    # TODO - verify that cv doesn't mess up the dimensions or channels of the region
    def get_region(self, region_identifier: RegionIndex, region_dims: Ignored = None) -> Region:
        """
        get_region reads in the image at self._region_files[region_identifier]

        :param region_identifier: the index of the file read (files are indexed alphabetically)
        :type region_identifier: RegionIndex
        :param region_dims: IGNORED - the regions will be whatever the regions of the image file are, defaults to None
        :type region_dims: Ignored
        :raises NotImplementedError: if region_identifier isn't an index
        :raises IndexError: if region_identifier isn't in range
        :return: region (the image in the file in question)
        :rtype: ImageAsNumpyArray
        """
        if not is_region_index(region_identifier):
            raise NotImplementedError(
                "This ImageReader only operates on aggregated region files which are indexed.")
        if not (0 <= region_identifier < self.number_of_regions()):
            raise IndexError(
                f"{region_identifier=}, {self.number_of_regions()=}")
        region_filepath = self._region_files[region_identifier]
        return cv.imread(region_filepath)

    def number_of_regions(self, region_dims: Ignored = None) -> int:
        """
        number_of_regions gets the number of region in the image (in this case, the number of image files in the directory)

        :param region_dims: IGNORED - the dimensions of the regions in this image are the dimensions of the image in the files, defaults to None
        :type region_dims: Ignored
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

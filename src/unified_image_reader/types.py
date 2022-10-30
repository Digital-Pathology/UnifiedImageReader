
"""
    Helpful type aliases and checking functions to improve readability in the rest of unified_image_reader
"""

from typing import Tuple, Optional, Any

import numpy as np

RegionIndex = int
RegionCoordinates = Tuple[int, int]
RegionDimensions = Tuple[int, int]

ImageAsNumpyArray = np.ndarray


def raise_type_error(obj: Any):
    """
    raise_type_error displays the type and stringified object in the TypeError

    :param obj: the object about which the TypeError occurred
    :type obj: Any
    """
    raise TypeError(f"{type(obj)=}, {obj=}")


def is_region_index(obj: Any) -> bool:
    """
     checks whether obj is a RegionIndex (alias for int)

    :rtype: bool
    """
    return isinstance(obj, int)


def is_tuple_of_certain_length_and_type(obj: Any, length: int, element_type: Optional[type] = None) -> bool:
    """
     Checks whether obj is a tuple of specified length and checks elements' types

    :rtype: bool
    """
    if not isinstace(obj, Iterable):
        return False
    if not len(obj) == 2:
        return False
    if element_type is not None:
        for e in obj:
            if not isinstance(e, element_type):
                return False
    return True


def is_region_coordinates(obj: Any) -> bool:
    """
    is_region_coordinates checks whether obj is an iterable of length 2 containing only ints

    :rtype: bool
    """
    return is_tuple_of_certain_length_and_type(obj, 2, int)


def is_region_dimensions(obj: Any) -> bool:
    """
    is_region_dimensions checks whether obj is an iterable of length 2 containing only ints

    :rtype: bool
    """
    return is_tuple_of_certain_length_and_type(obj, 2, int)


def is_image_as_numpy_array(obj: Any) -> bool:
    """
    is_image_as_numpy_array checks whether obj is a numpy array (does not check dimensions)

    :rtype: bool
    """
    return isinstance(obj, ImageAsNumpyArray)


"""
    Helpful type aliases and checking functions to improve readability in the rest of unified_image_reader
"""

# TODO - apply PathLib to make the filepath manipulations more readable throughout the package

from typing import Any, Iterable, Optional, Tuple, Union

import numpy as np

Region = np.ndarray

RegionIndex = int
RegionCoordinates = Tuple[int, int]
RegionIdentifier = Union[RegionIndex, RegionCoordinates]

RegionDimensions = Tuple[int, int]
ImageDimensions = Tuple[int, int]

Ignored = Any


def raise_type_error(obj: Any):
    """
    raise_type_error displays the type and stringified object in the TypeError

    :param obj: the object about which the TypeError occurred
    :type obj: Any
    :raises TypeError: for obvious reasons
    """
    raise TypeError(f"{type(obj)=}, {obj=}")


def is_region_index(obj: Any) -> bool:
    """
     checks whether obj is a RegionIndex (alias for int)

    :rtype: bool
    """
    if isinstance(obj, float):
        return float.is_integer(obj)
    return isinstance(obj, int)


def is_iterable_of_certain_length_and_type(obj: Any, length: int, element_type: Optional[type] = None) -> bool:
    """
     Checks whether obj is a iterable of specified length and checks elements' types

    :rtype: bool
    """
    if not isinstance(obj, Iterable):
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
    return is_iterable_of_certain_length_and_type(obj, 2, int)


def is_region_dimensions(obj: Any) -> bool:
    """
    is_region_dimensions checks whether obj is an iterable of length 2 containing only ints

    :rtype: bool
    """
    return is_iterable_of_certain_length_and_type(obj, 2, int)


def is_region_identifier(obj: Any) -> bool:
    """
    is_region_identifier checks whether obj is a RegionIdentifier

    :rtype: bool
    """
    return is_region_index(obj) or is_region_coordinates(obj)


def is_region(obj: Any) -> bool:
    """
    is_region checks whether obj is a numpy array (does not check dimensions)

    :rtype: bool
    """
    # TODO - validate array type and dimensions
    return isinstance(obj, Region)

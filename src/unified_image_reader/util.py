
"""
    Utility functions and classes for the Unified Image Reader
"""

import os
from typing import List, NewType, Tuple, Union

RegionDimensions = NewType('RegionDimensions', Tuple[int, int])

RegionIndex = NewType('RegionIndex', int)
RegionCoordinates = NewType('RegionCoordinates', Tuple[int, int])
RegionIdentifier = NewType(
    'RegionIdentifier', Union[RegionIndex, RegionCoordinates])

FilePath = NewType('FilePath', str)


def listdir_recursive(path: FilePath) -> List[FilePath]:
    """
    listdir_recursive lists files (not directories) recursively from path

    :param path: the path to the directory whose files should be listed recursively
    :type path: FilePath
    :return: a list of filepaths relative to path
    :rtype: List[FilePath]
    """
    files = []
    walk = os.walk(path)
    for (directory_pointer, _, file_nodes) in walk:
        files += [
            os.path.join(directory_pointer, file_node)
            for file_node in file_nodes
        ]
    return files

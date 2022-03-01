"""
    SlideIO Adapter

    An adapter that uses the SlideIO library to implement image reading behavior
    Adapter currently mapped to reading .svs files
"""
import numpy as np

try:
    import slideio
except Exception as e:
    print("You have an issue with your SlideIO installation, it may be because of the dependency on Openslide. Contact Adin at adinbsolomon@gmail.com with any questions!")
    raise e

from .adapter import Adapter

class SlideIO(Adapter):

    def __init__(self, filepath):
        """
        Initialize SlideIO adapter object

        Parameters:
            filepath (str): Filepath to image file to be opened 
        """
        self._image = slideio.open_slide(filepath, "SVS").get_scene(0)

    def get_width(self): return self._image.size[0]

    def get_height(self): return self._image.size[1]

    def get_region(self, region_identifier, region_dims) -> np.ndarray:
        """ Calls the read_block method of a SlideIO Scene object to create an unscaled rectangular region of the image as a numpy array """
        np_array = self._image.read_block((*region_identifier, *region_dims))
        return np_array

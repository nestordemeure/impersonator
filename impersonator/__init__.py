from .persona import Persona
from .chat import Chat

#----------------------------------------------------------------------------------------
# CUT IMAGE DETECTION

from layoutparser.models.detectron2 import Detectron2LayoutModel
from layoutparser.elements import Layout

def dummy_detect(self, image):
    """
    dummy function that returns an empty layout instead of running the object detector
    """
    return Layout()

# we cut image detection from the model used by unstructured as we only care about text
Detectron2LayoutModel.detect = dummy_detect

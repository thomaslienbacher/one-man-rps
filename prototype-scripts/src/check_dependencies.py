"""
Diese Script kann genutzt werden, um zu überprüfen ob alle Python Bibliotheken installiert wurden.
Wenn am Ende ein Smiley kommt ist höchst wahrscheinlich alles korrekt installiert.
"""

print("Loading...")

import numpy
import matplotlib
import cv2
from picamera import mmal
import tensorflow

print("Versions installed:")
print("  numpy:", numpy.__version__)
print("  matplotlib:", matplotlib.__version__)
print("  cv2:", cv2.__version__)
print("  picamera (MMAL version):", "{}.{}".format(mmal.MMAL_VERSION_MAJOR, mmal.MMAL_VERSION_MINOR))
print("  tensorflow:", tensorflow.__version__)
print("\nIt seems that everything is installed :)")

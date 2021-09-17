# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import numpy as np
import PIL
import requests
import tensorflow as tf


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def loadImage(filepath):
   '''
   DESCRIPTION
         This function loads an image content whose file hook is given by <imgFile>.
   ARGUMENT(S)
         filepath
            the full path name of the file.
   RETURN
         A PIL.Image object.
   '''
   return PIL.Image.open(fp = filepath, mode = 'r')



def loadImageFromUrl(url):
   return PIL.Image.open(requests.get(url, stream=True).raw)



def prepareImageData(
      image
   ,  target_size
   ,  interpolation = 'bilinear'
):
   # Converting the image type if necessary: objective to get an image of type numpy.ndarray
   if isinstance(image, PIL.Image.Image):
      # Converting <image> to a numpy ndarray
      image = tf.keras.preprocessing.image.img_to_array(image)
   elif isinstance(image, np.ndarray):
      # Nothing more to do here: the image already has the valid type
      pass
   else:
      raise TypeError('Invalid type for argument <image>: actual type: {type(image)}')

   # Resizing the image
   image = tf.keras.preprocessing.image.smart_resize(
         x             = image
      ,  size          = target_size
      ,  interpolation = interpolation
   )
   # Adding a dimension to transform our array into a "batch" of size (1, X, X, 3)
   image = np.expand_dims(image, axis = 0)

   return image

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import streamlit as st

# Import User libraries
from apps.base_app                     import CBaseApp
from session_state.session_state_utils import CSSKeys as ss
from components.image_selector         import CImageSelector
from components.image_recognition      import CImageRecognition
from session_state.image_state         import CImageClassificationState

from model.all_models              import mushroomDetector, efficientNetB0, efficientNetB1, efficientNetB2  \
                                          , efficientNetB3, efficientNetB4, efficientNetB5, efficientNetB6  \
                                          , efficientNetB7, vgg16, vgg19                                    \
                                          , ensembleClassifier




def app():

      # Retrieving the image used for the classification
      imageState = CImageClassificationState()
      imageState.setFromRegistry()

      # component: ImageSelector
      compOpts = dict(
            imageSelectMode_key                   = ss.SIR__IMAGE_SELECT_MODE.value
         ,  localFileUploader_label               = 'Upload a local image:'
         ,  localFileUploader_allowedTypes        = ['png', 'jpg', 'jpeg']
         ,  localFileUploader_acceptMultipleFiles = False
         ,  localFileUploader_key                 = ss.SIR__LOCAL_FILE_UPLOADER.value
         ,  localFileUploader_help                = 'Upload here an image containing a mushroom.'
         ,  remoteFileUploader_label              = 'URL:'
         ,  remoteFileUploader_maxChars           = 2048
         ,  remoteFileUploader_help               = 'Enter an URL pointing to an image containing a mushroom.'
         ,  remoteFileUploader_key                = ss.SIR__REMOTE_FILE_UPLOADER.value
      )
      imageSelector = CImageSelector(compOpts = compOpts, compState = imageState)
      imageSelector.render()

      # Go further only if we have a valid image
      #
      imageState.setFromRegistry()
      image = imageState.getData()
      if image:

         # Displaying the image
         st.write('Displaying the uploaded image:')
         st.image(image, caption = 'uploaded image')

         # component: imageRecognition
         compOpts = dict(
            title = 'Image Recognition'
         )
         imageRecognition = CImageRecognition(
               compOpts           = compOpts
            ,  image              = image
            ,  mushroomDetector   = mushroomDetector
            ,  mushroomClassifier = ensembleClassifier
         )
         imageRecognition.render()

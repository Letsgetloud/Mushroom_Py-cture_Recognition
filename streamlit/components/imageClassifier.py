# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import tensorflow as tf
import time as t

# Import User Libraries
from components.base_component         import CBaseComponent
from session_state.session_state_utils import CSSKeys as ssKeys, CSessionState as ss
from session_state.model_state         import CModelState
from session_state.image_state         import CImageState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMP_DFLT_OPTS = dict(
      title = 'Image Selector'
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CImageClassifier(CBaseComponent):

   def __init__(self
      ,  compOpts
   ):
      super().__init__(compOpts)



   def dataPreprocessing(self
      ,  image
      ,  imageTargetShape
   ):

      if image is None:
         return None

      targetHeight, targetWidth, targetChannel = imageTargetShape[:3]

      # Make a copy
      imgData = image.copy()

      # As a numpy array
      imgData = np.asarray(image)

      # Applying data preprocessing
      # using tensor
      X = tf.constant(imgData)
      # add a dimension (for batchs)
      X = tf.expand_dims(X, axis = 0)
      # Resizing
      X = tf.image.resize_with_pad(
            image         = X
         ,  target_height = targetHeight
         ,  target_width  = targetWidth
         ,  method        = 'nearest'
      )

      return X




   def predict(self
      ,  model
      ,  image
      ,  console
   ):
      try:
         res = None
         if model is not None \
            and image is not None:
            # Performs the prediction
            begTime = t.time()
            res = model.predict(
                  x          = image
               ,  batch_size = None
               ,  verbose    = 1
            )
            endTime = t.time()
            durationSec = endTime - begTime
      except Exception as e:
         st.write(e)
         console.exception(e)
         res = None

      finally:
         return (res, durationSec)





   def recognition(self, console):

      try:
         result = None

         console.info('Recognition in progress...')

         # Retrieving the model
         modelState = CModelState()
         modelState.setFromRegistry()
         if modelState.getLoadSuccess() != True:
            raise RuntimeError('No model available ! Please load a model and try again.')
         modelInstance = modelState.getModelInstance()
         if modelInstance is None:
            raise RuntimeError('<None Type> is not a valid model ! Please load a model and try again.')
         classNames = modelState.getClassNames()

         # Retrieving the expected input shape for the model
         modelInputShape  = modelInstance.input_shape
         imageTargetShape = modelInputShape[1:]

         # Retrieving the image
         imageState = CImageState()
         imageState.setFromRegistry()
         if not imageState.getLoadSuccess():
            raise RuntimeError('No image available ! Please load an image and try again.')
         imgData = imageState.getData()
         if imgData is None:
            raise ValueError('<None Type> is not a valid image ! Please load an image and try again.')

         # Data Preprocessing
         imgData = self.dataPreprocessing(
               image            = imgData
            ,  imageTargetShape = imageTargetShape
         )
         console.info('prediction in progress...')
         rawPreds, durationSec = self.predict(modelInstance, imgData, console)
         console.info(f'prediction done (in {round(durationSec * 1000, 2)} ms)')

         # Here we have valid results
         if (rawPreds is not None) and rawPreds.shape[0] > 0:
            preds = pd.DataFrame(
                  data = {
                     'Probas': rawPreds[0]
                  }
               ,  index = classNames
            )
            preds.index.name = 'Class'
            result = preds

      except Exception as e:
         console.exception(e)
         result = None

      finally:
         return result




   def render(self):

      with st.container():

         #
         # Component Title
         #
         # Display the component title
         self.showTitle(self.getOpt('title'))

         #
         # Button: "Launch recognition"
         #
         btn_LaunchRecognition = st.button(
               label    = 'Launch recognition'
            ,  help     = 'Click on this button to launch the recognition on the selected image'
         )

         # Placeholder for Recognition status
         console = st.empty()

         # Button: "Launch recognition" has been clicked
         if btn_LaunchRecognition:
            preds = self.recognition(console)

            if preds is not None:

               # Format the DataFrame
               data = preds.copy() \
                        .reset_index(inplace = False) \
                        .sort_values(
                              by           = ['Probas']
                           ,  ascending    = False
                           ,  inplace      = False
                           ,  ignore_index = False
                        )

               # GUI component properties
               topColor = '#f63366'
               if data.shape[0] <= 10:
                  height = 400
               else:
                  height = 800

               # Displaying the prediction results
               #
               # Genus
               genusName = f'The model thinks the genus of the mushroom on the image is: <span style="border-radius: 0.4rem; color: white; padding: 0.3rem; margin-bottom: 2rem; padding-left: 1rem; font-weight: 700; background-color: {topColor};">{data.iloc[0]["Class"]}</span>'
               st.markdown(genusName, unsafe_allow_html = True)

               st.write('Find below more details on the predictions done by the model:')

               # Graphic (altair)
               st.write('**Graphic:**')
               chart = alt.Chart(data) \
                  .mark_bar() \
                  .encode(
                        x       = alt.X('Probas:Q')
                     ,  y       = alt.Y('Class', title = 'Genus', sort = '-x')
                     ,  opacity = alt.value(1)
                     ,  color   = alt.condition(
                              alt.datum.Class == data.iloc[0]['Class']  # If it's the top ranked prediction
                           ,  alt.value('#f63366')                      # sets the color for the top ranked prediction
                           ,  alt.value('#1F74B4')                      # sets the color for all other non top ranked prediction
                        )
                  ) \
                  .properties(
                        width  = 650
                     ,  height = height
                  )
               text = chart.mark_text(
                     align    = 'left'
                  ,  baseline = 'middle'
                  ,  dx = 3                # Nudges text to right so it doesn't appear on top of the bar
               ) \
                  .encode(
                     text = alt.Text('Probas', format = '.2r')
                  )
               graph = (chart + text).configure_axis(
                     labelFontSize = 13
                  ,  titleFontSize = 16
               )
               # Displaying the graphic
               st.altair_chart(graph)

               # Full table of predictions
               st.write('**Full table of predictions:**')
               st.dataframe(
                     data   = data.reset_index(drop = True)
                  ,  height = height
               )



   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')
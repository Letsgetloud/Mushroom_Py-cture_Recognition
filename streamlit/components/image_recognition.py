# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Import User Libraries
from components.base_component                     import CBaseComponent
from session_state.session_state_utils             import CSSKeys as ssKeys
from session_state.mushroom_detection_state        import CMushroomDetectionState
from session_state.mushroom_classification_state   import CMushroomClassificationState
from image.image_utils                             import prepareImageData
from model.model                                   import EnsembleClassifier
from model.all_models                              import MushroomDetectorClasses
from model.interpretability                        import make_gradcam_heatmap


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CImageRecognition(CBaseComponent):

   def __init__(self
      ,  compOpts
      ,  image
      ,  mushroomDetector   = None
      ,  mushroomClassifier = None
   ):
      super().__init__(compOpts)
      self.image = image
      self.mushroomDetector   = mushroomDetector
      self.mushroomClassifier = mushroomClassifier



   def isMushroomDetected(self
      ,  model
      ,  image
      ,  console
      ,  threshold = 0.65
   ):

      def isDetected(pred):
         print(f'model[ Mushroom detector ] predictions: {pred}')
         idxMax = np.argmax(pred)
         resDetection = model.getClass(idxMax)
         if resDetection.value == MushroomDetectorClasses.PRESENT.value:
            return float(pred[idxMax]) >= threshold
         elif resDetection.value == MushroomDetectorClasses.NOT_PRESENT.value:
            return False
         else:
            raise ValueError('Failed to find the corresponding class to the model prediction. Please contact the administrator.')

      # Get the model name
      modelName = model.getName()

      # Get the model ready (loading it if necessary)
      console.info(f'Loading {modelName} model...')
      model.load()

      # Get the model input shape
      modelInputShape = model.getModelInputShape()

      # Prepare the data for the model
      console.info('Image preprocessing...')
      data = prepareImageData(
            image         = image
         ,  target_size   = modelInputShape[1:3]
         ,  interpolation = 'bilinear'
      )

      # Launch the prediction
      pred = model.predict(
            x       = data
         ,  verbose = 1
      )

      return isDetected(pred[0])

   def doModelInterpretability(self, console):
           console.info("Grad-CAM in progress..")
           grad_cam = self.perform_GradCAM(models=self.mushroomClassifier, image=self.image, console=console )



   def _classify(self
      ,  classifierModel
      ,  image
      ,  console
      ,  progressBar
   ):

      def doPrediction():
         '''
         print(f'model[ Mushroom detector ] predictions: {pred}')
         idxMax = np.argmax(pred)
         resDetection = model.getClass(idxMax)
         if resDetection.value == MushroomDetectorClasses.PRESENT.value:
            return pred[idxMax] >= threshold
         elif resDetection.value is MushroomDetectorClasses.NOT_PRESENT:
            return False
         else:
            raise ValueError('Failed to find the corresponding class to the model prediction. Please contact the administrator.')
         '''
         pass

      if not isinstance(classifierModel, EnsembleClassifier):
         raise NotImplementedError('Classification is only supported for the moment if the model has been inherited from class <EnsembleClassifier>. Using other kind of classifier is not yet implemented !')

      ensembleModel = classifierModel

      stackX        = None
      membersNames  = list()
      membersCnt    = len(ensembleModel.getMembers())
      classNames    = ensembleModel.getClasses()

      for cnt, model in enumerate(ensembleModel.getMembers()):

         # Get the model name
         modelName = model.getName()

         # Get the model ready (loading it if necessary)
         console.info(f'Loading {modelName} model...')
         model.load()

         progressBar.progress((cnt + 1/3) / membersCnt)

         # Get the model input shape
         modelInputShape = model.getModelInputShape()

         # Prepare the data for the model
         console.info(f'Image preprocessing (for model: {modelName})...')
         data = prepareImageData(
               image         = image
            ,  target_size   = modelInputShape[1:3]
            ,  interpolation = 'bilinear'
         )

         progressBar.progress((cnt + 2/3) / membersCnt)

         # Launch the prediction
         console.info(f'Computing classification (for model: {modelName})...')
         proba = model.predict(
               x       = data
            ,  verbose = 1
         )

         membersNames.append(modelName)
         if stackX is None:
            stackX = proba
         else:
            stackX = np.dstack((stackX, proba))

         progressBar.progress((cnt + 1) / membersCnt)

      progressBar.progress(1.0)

      # modelState.register()

      df_membersProbas = pd.DataFrame(
            data    = stackX[0]
         ,  index   = [ name.value for name in classNames ]
         ,  columns = membersNames
      )

      stackX = np.reshape(stackX, newshape = (stackX.shape[0], stackX.shape[1] * stackX.shape[2]))

      # Get the model ready (loading it if necessary)
      ensembleModel.load()
      #modelState.register()

      # Compute the predictions for the Ensemble model
      model       = ensembleModel.getInstance()
      modelProbas = model.predict_proba(stackX)

      print('modelProbas.shape: ', modelProbas.shape)

      # Set the classifier results in a DataFrame
      df_modelProbas = pd.DataFrame(
            data    = modelProbas[0]
         ,  index   = [ name.value for name in classNames ]
         ,  columns = [ 'Probas' ]
      )

      # Format the DataFrame
      df_modelProbas.index.name = 'Class'
      df_results = df_modelProbas \
         .reset_index(drop = False, inplace = False) \
         .sort_values(
               by           = ['Probas']
            ,  ascending    = False
            ,  inplace      = False
            ,  ignore_index = False
         )

      # Displaying the prediction results
      #
      # GUI component properties
      topColor = '#f63366'
      # Genus
      resultHTML = f'The model thinks the genus of the mushroom on the image is: <span style="border-radius: 0.4rem; color: white; padding: 0.3rem; margin-bottom: 2rem; padding-left: 1rem; font-weight: 700; background-color: {topColor};">{df_results.iloc[0]["Class"]}</span>'
      st.markdown(resultHTML, unsafe_allow_html = True)

      #st.write('Predictions were done by an Ensemble Model.')
      st.write('Below are more details regarding the predictions:')

      #
      # Ensemble Model results
      #

      st.markdown('**Results** :')
      processCol1, processCol2 = st.columns([1, 2])
      with processCol1:
        st.markdown('* Probabilities:')
        st.dataframe(df_results)

      with processCol2:
        st.markdown('* Graphic:')
        # Graphic (altair)
        chart = alt.Chart(df_results) \
            .mark_bar() \
            .encode(
                x       = alt.X('Probas:Q')
                ,  y       = alt.Y('Class', title = 'Genus', sort = '-x')
                ,  opacity = alt.value(1)
                ,  color   = alt.condition(
                        alt.datum.Class == df_results.iloc[0]['Class']  # If it's the top ranked prediction
                    ,  alt.value('#f63366')                      # sets the color for the top ranked prediction
                    ,  alt.value('#1F74B4')                      # sets the color for all other non top ranked prediction
                )
            ) \
            .properties(
                width  = 650
                ,  height = 260
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

      #
      # Members models results
      #
      with st.expander('Details for each underlying model :'):
        col1, col2 = st.columns([1, 2])

        col1.dataframe(df_membersProbas.style.format("{:.2}"))

        #show box plot

        chart = alt.Chart(df_membersProbas.T.melt()).mark_boxplot().encode(y='variable', x='value')\
                    .properties(width  = 650  ,  height = 260)

        chart.configure_axis( labelFontSize = 13 ,  titleFontSize = 16)

        # Displaying the graphic

        col2.altair_chart(chart)

      #with st.expander('Explainability with Grad-CAM algorithm : '):
        #self.doModelInterpretability(console = console)




   def doMushroomClassification(self
      ,  console
   ):
      try:
         # mushroom classification state instanciation
         mushroomClassificationState = CMushroomClassificationState()
         console.info('Mushroom classification in progress... this may take a while... please wait !')

         progressBar = st.progress(0)

         # Ensure that an image is available
         if self.image is None:
            raise RuntimeError('No image available ! Please load an image and try again.')

         # Ensure that a model for the mushroom detection is available
         if self.mushroomClassifier is None:
            raise RuntimeError('No model available for the mushroom detection ! Please contact the administrator.')

         # Classify the mushroom present in the image
         self._classify(
               classifierModel = self.mushroomClassifier
            ,  image           = self.image
            ,  console         = console
            ,  progressBar     = progressBar
         )


      except Exception as e:
         console.exception(e)
         # Updating the mushroom detection state
         mushroomClassificationState.setData(data = None)




   def recognition(self, console):
      pass

   

   def doMushroomDetection(self
      ,  console
   ):
      try:
         # mushroom detection state instanciation
         mushroomDetectionState = CMushroomDetectionState()

         console.info('Mushroom detection in progress...')

         # Ensure that an image is available
         if self.image is None:
            raise RuntimeError('No image available ! Please load an image and try again.')
         # Ensure that a model for the mushroom detection is available
         if self.mushroomDetector is None:
            raise RuntimeError('No model available for the mushroom detection ! Please contact the administrator.')

         # Detecting if a Mushroom is present in the image
         detected = self.isMushroomDetected(
               model          = self.mushroomDetector
            ,  image          = self.image
            ,  console        = console
         )

         # Updating the mushroom detection state
         mushroomDetectionState.setData(data = detected)

      except Exception as e:
         console.exception(e)
         # Updating the mushroom detection state
         mushroomDetectionState.setData(data = None)

      finally:
         # Registering the Mushroom detection state
         mushroomDetectionState.register()


   def perform_GradCAM(self
      ,  models
      ,  image
      ,  console
   ):
      try:
         # Ensure that a model is available
         #if models is None or len(models) < 1:
         #   raise RuntimeError('No model available ! Please select a model try again.')
         # Ensure that an image is available
         #if image is None:
         #   raise RuntimeError('No image available ! Please load an image and try again.')

         i=0
         j=0
         fig, ax = plt.subplots(2,5,figsize=(15,6))

         # Ensure that the models are loaded
         for cnt, model in enumerate(models.getMembers()):

            # Get the model name
            modelName = model.getName()

            console.info(f'Load the model {modelName}...')
            model.load()

            # Get the model input shape
            modelInputShape = model.getModelInputShape()

            # Prepare the data for the model
            console.info('Image preprocessing...')
            data = prepareImageData(
                  image         = image
               ,  target_size   = modelInputShape[1:3]
               ,  interpolation = 'bilinear'
            )

            # Print what the top predicted class is
            #pred = model.predict(data)

            # Compute the gardcam heatmap
            console.info('Compute the gradcam heatmap...')
            heatmap = make_gradcam_heatmap(
                  model = model.getInstance()
               ,  image = data
            )

            # Display heatmap
            console.info('Display the heatmap...')
            ax[i,j].matshow(heatmap)
            ax[i,j].axis("off")
            ax[i,j].set_title(modelName)
            j += 1
            if j == 5:
               i += 1
               j = 0

         st.pyplot(fig)
         console.empty()

      except Exception as e:
         console.exception(e)
         

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
               label = 'Launch recognition'
            ,  help  = 'Click on this button to launch the recognition on the selected image'
         )

         enableClassification = False

         # Button: "Launch recognition" has been clicked
         if btn_LaunchRecognition:

            st.write('[Phase 1]: Mushroom detection on the image')

            # Placeholder for Mushroom Detection
            console = st.empty()

            self.doMushroomDetection(console = console)

            # Displaying the "mushroom detection" status
            #
            # Retrieving the mushroom detection state
            mushroomDetectionState = CMushroomDetectionState()
            mushroomDetectionState.setFromRegistry()

            detectionState = mushroomDetectionState.getData()

            if detectionState is None:
               enableClassification = False
            elif detectionState == True:
               console.success('Mushroom detected ! (according to the model)')
               enableClassification = True
            else:
               console.error('NO mushroom detected on the image according to the model.')
               # Radio: Force recognition
               radio_forceRecognition = st.radio(
                     label       = 'Do you want to force the mushroom recognition anyway ?'
                  ,  key         = ssKeys.IR__FORCE_RECOGNITION.value
                  ,  options     = [False, True]
                  ,  index       = 0                  # False by default
                  ,  format_func = lambda x: 'Yes' if x else 'No'
               )

               # Radio "Force recognition" has changed
               if radio_forceRecognition == True:
                  # Enable the Mushroom Recognition
                  enableClassification = True
               elif radio_forceRecognition == False:
                  # Nothing more to do here
                  enableClassification = False


            # Launch the Mushroom Recognition (if requested)
            if enableClassification:

               st.markdown('''<p>         </p>  ''', unsafe_allow_html=True)

               st.write('[Phase 2]: Mushroom genus recognition')

               # Placeholder for Mushroom Detection
               console = st.empty()

               self.doMushroomClassification(console = console)

               st.markdown('''<p>         </p>  ''', unsafe_allow_html=True)
               st.write('[Phase 3]: Perform Grad-CAM algorithm')

               # Placeholder for Mushroom Detection
               console = st.empty()

               with st.expander('Explainability with Grad-CAM algorithm : '):
                    self.doModelInterpretability(console = console)


               
               




   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')








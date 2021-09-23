# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import streamlit as st
import numpy as np 
import pandas as pd
import time
import altair as alt
import matplotlib.pyplot as plt
import os 
import inspect


# Import User libraries
from base_app                          import CBaseApp
from session_state.session_state_utils import CSSKeys as ss
from components.image_selector         import CImageSelector
from components.image_recognition      import CImageRecognition
from session_state.image_state         import CImageClassificationState

from model.all_models_colab                  import mushroomDetector, efficientNetB0, efficientNetB1, efficientNetB2  \
                                          , efficientNetB3, efficientNetB4, efficientNetB5, efficientNetB6  \
                                          , efficientNetB7                                  \
                                          , ensembleClassifier

from model.all_models_colab                  import MushroomDetectorClasses

from image.image_utils                 import prepareImageData
from model.interpretability            import make_gradcam_heatmap, save_and_display_gradcam

#===============================================================================
# Chargement du model (mise en cache)
#===============================================================================
#@st.cache(allow_output_mutation=True)
def load_mushroomDetector(mushroomDetector):
    with st.spinner("Downloading mushroom detector model..."):
        mushroomDetector.load()
    return mushroomDetector

#===============================================================================
# Chargement du model (mise en cache)
#===============================================================================
#@st.cache(allow_output_mutation=True)
def load_ensembleClassifier(ensembleClassifier):
    with st.spinner("Downloading mushroom model... this may take a while! \n Don't stop it!"):
        ensembleClassifier.load()
    return ensembleClassifier


def doMushroomDetection(image, model, console, threshold=0.65):

     # mushroom detection state instanciation

     console.info('Mushroom detection in progress...')
     
     modelInputShape = model.getModelInputShape()

     # Prepare the data for the model
     console.info('Image preprocessing...')
     data = prepareImageData(
            image         = image
         ,  target_size   = modelInputShape[1:3]
         ,  interpolation = 'bilinear')

     # Launch the prediction
     pred = model.predict(
            x       = data
         ,  verbose = 1)

     if pred[0][0] > threshold:
         return True 
     else:
        return False

def doMushroomClassification(image, models, console, progressBar):

     stackX        = None
     membersNames  = list()
     membersCnt    = len(models.getMembers())
     classNames    = models.getClasses()

     for cnt, model in enumerate(models.getMembers()):

         # Get the model name
         modelName = model.getName()

         # Get the model ready (loading it if necessary)
         #console.info(f'Loading {modelName} model...')
         #model.load()

         #progressBar.progress((cnt + 1/3) / membersCnt)

         # Get the model input shape
         modelInputShape = model.getModelInputShape()

         # Prepare the data for the model
         console.info(f'Image preprocessing (for model: {modelName})...')
         data = prepareImageData(
               image         = image
            ,  target_size   = modelInputShape[1:3]
            ,  interpolation = 'bilinear'
         )

         progressBar.progress((cnt + 1/2) / membersCnt)

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

      #progressBar.progress(1.0)

      # modelState.register()

     df_membersProbas = pd.DataFrame(
            data    = stackX[0]
         ,  index   = [ name.value for name in classNames ]
         ,  columns = membersNames
      )
      
     df_membersClass = df_membersProbas.apply(
            func = np.argmax
         ,  axis = 0
        )

     stackX = np.reshape(stackX, newshape = (stackX.shape[0], stackX.shape[1] * stackX.shape[2]))

      # Get the model ready (loading it if necessary)
      #ensembleModel.load()
      #modelState.register()

     # Compute the predictions for the Ensemble model
     model       = models.getInstance()
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

     classification = df_membersClass.value_counts()
     classification.index.name = 'Class'
     classification = classification.rename(lambda x: classNames[x].value)
     classification.name = 'Count'

     df5 = df_membersClass.apply(func = lambda x: classNames[x].value)

     df_results.to_csv("df1.csv")
     df_membersProbas.to_csv("df2.csv")
     classification.to_csv("df4.csv")
     df5.to_csv("df5.csv")



def doGradCAM(image, models, console, progressBar):

     i=0
     j=0
     fig, ax = plt.subplots(2,4,figsize=(15,6))

     # Ensure that the models are loaded
     for cnt, model in enumerate(models.getMembers()):

        # Get the model name
        modelName = model.getName()

        console.info(f'Load the model {modelName}...')
        model.load()

        progressBar.progress((cnt + 1/3) / len(models.getMembers()))

        # Get the model input shape
        modelInputShape = model.getModelInputShape()

        # Prepare the data for the model
        console.info('Image preprocessing...')
        data = prepareImageData(
                    image         = image
                ,  target_size   = modelInputShape[1:3]
                ,  interpolation = 'bilinear'
                )

        progressBar.progress((cnt + 2/3) / len(models.getMembers()))

        # Print what the top predicted class is
        #pred = model.predict(data)

        # Compute the gardcam heatmap
        console.info('Compute the gradcam heatmap for ' + modelName)
        heatmap = make_gradcam_heatmap(
                    model = model.getInstance()
                ,  image = data
                )
        save_and_display_gradcam(image, heatmap, idx=cnt)

        progressBar.progress((cnt + 1) / len(models.getMembers()))

        # Display heatmap
        console.info('Display the heatmap...')
        ax[i,j].matshow(heatmap)
        ax[i,j].axis("off")
        ax[i,j].set_title(modelName)
        j += 1
        if j == 4:
            i += 1
            j = 0

     #st.pyplot(fig)
     progressBar.progress(1.0)
     console.empty()


def showMushroomClassification(container):
    try:
        df1 = pd.read_csv("df1.csv", index_col=0)
        df2 = pd.read_csv("df2.csv", index_col=0)
        df4 = pd.read_csv("df4.csv", index_col=0)
        df5 = pd.read_csv("df5.csv", index_col=0)

        # Displaying the prediction results
        # GUI component properties
        topColor = '#f63366'
        # Genus
        resultHTML = f'The model thinks the genus of the mushroom on the image is: <span style="border-radius: 0.4rem; color: white; padding: 0.3rem; margin-bottom: 2rem; padding-left: 1rem; font-weight: 700; background-color: {topColor};">{df1.iloc[0]["Class"]}</span>'
        container.markdown(resultHTML, unsafe_allow_html = True)
        container.write('Below are more details regarding the predictions:')

        container.markdown('**Results** :')
        Col1, Col2 = container.columns([1, 2])

        Col1.markdown('* Probabilities:')
        Col1.dataframe(df1)

        Col2.markdown('* Graphic:')
        # Graphic (altair)
        chart = alt.Chart(df1) \
            .mark_bar() \
            .encode(
            x       = alt.X('Probas:Q')
            ,  y       = alt.Y('Class', title = 'Genus', sort = '-x')
            ,  opacity = alt.value(1)
            ,  color   = alt.condition(
                    alt.datum.Class == df1.iloc[0]['Class']  # If it's the top ranked prediction
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
        Col2.altair_chart(graph)

        #
        # Members models results
        #

        expander = container.expander('Details for each underlying model :')
        col1, col2 = expander.columns([1, 2])

        col1.dataframe(df2.style.format("{:.2}"))

        #show box plot
        chart = alt.Chart(df2.T.melt()).mark_boxplot().encode(y='variable', x='value')\
                    .properties(width  = 650  ,  height = 260)

        chart.configure_axis( labelFontSize = 13 ,  titleFontSize = 16)

        # Displaying the graphic
        col2.altair_chart(chart)

        col3, col4 =expander.columns([2,2])

        col3.markdown('* Classification Overview:')
        col3.write(df4)

        col4.markdown('* Classification per member:')
        col4.write(df5)

    except:
        pass

def showGradCAM(container):
    if os.path.exists("cam_0.jpg"):
        col1, col2, col3, col4 = container.columns(4)
        col1.text("EfficientNetB0")
        col1.image("cam_0.jpg")
        col2.text("EfficientNetB1")
        col2.image('cam_1.jpg')
        col3.text("EfficientNetB2")
        col3.image('cam_2.jpg')
        col4.text("EfficientNetB3")
        col4.image('cam_3.jpg')

        col5, col6, col7, col8 = container.columns(4)
        col5.text("EfficientNetB4")
        col5.image("cam_4.jpg")
        col6.text("EfficientNetB5")
        col6.image('cam_5.jpg')
        col7.text("EfficientNetB6")
        col7.image('cam_6.jpg')
        col8.text("EfficientNetB7")
        col8.image('cam_7.jpg')


def app():

      currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
      st.image(os.path.join(currentdir,  '_assets_/images/Mushroom_py-cture_recognition.png'))

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
         
         Form1 = st.form(key="Recognition")
         Form2 = st.form(key="Grad-CAM")

         Recognition = Form1.container()
         submit_1 = Recognition.form_submit_button('Launch Recognition')

         Explainability = Form2.container()
         submit_2 = Explainability.form_submit_button('Launch Grad-CAM')

         with Form1:
            
            enableClassification = False

            if submit_1:
                console = Recognition.empty()
                model = mushroomDetector
                load_mushroomDetector(model)

                Recognition.write('[Phase 1]: Mushroom detection on the image')
                # Placeholder for Mushroom Detection
                detectionState = doMushroomDetection(image, mushroomDetector, console)

                if detectionState is None:
                    enableClassification = False
                elif detectionState == True:
                    Recognition.success('Mushroom detected !')
                    enableClassification = True
                else:
                    Recognition.error('Warning : Apparently NO mushroom detected on the image..')
                    enableClassification = True


            # Launch the Mushroom Recognition
            if enableClassification:
               models = ensembleClassifier
               Recognition.markdown('''<p>         </p>  ''', unsafe_allow_html=True)
               Recognition.write('[Phase 2]: Mushroom genus recognition')
               #st.write(len(models.getMembers()))
               load_ensembleClassifier(models)
               #st.write(len(models.getMembers()))
               # Placeholder for Mushroom Detection
               progressBar = Recognition.progress(0)
               doMushroomClassification(image, models, console, progressBar)
               progressBar.empty()
               Recognition.empty()

               showMushroomClassification(Recognition)
               
               showGradCAM(Explainability)

               Recognition.markdown('''<p>         </p>  ''', unsafe_allow_html=True)

         with Form2:
             if submit_2:
                 console = Explainability.empty()
                 progressBar = Explainability.progress(0)

                 console.info("Grad-CAM in progress..")
                 models = ensembleClassifier
                 load_ensembleClassifier(models)

                 doGradCAM(image, models, console, progressBar)
                 progressBar.empty()
                 console.empty()
                 showGradCAM(Explainability)

                 showMushroomClassification(Recognition)
                


         
         
  

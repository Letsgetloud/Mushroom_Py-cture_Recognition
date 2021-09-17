# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import os
import sys
import json
import numpy as np
import tensorflow as tf
import streamlit as st

# Import User Libraries
from components.base_component         import CBaseComponent
from session_state.session_state_utils import CSSKeys as ssKeys, CSessionState as ss
from session_state.model_state         import CModelState


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMP_DFLT_OPTS = dict(
      title          = 'Model Selector'
   ,  classifierFile = ''
)

CLASSIFIER_JSON_FILENAME      = 'classifiers.json'
APP_ROOT_PATH                 = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]), '..'))
CLASSIFIER_ROOT_RELATIVE_PATH = os.path.join('resources', 'classifiers')
DFLT_MODEL_PATH               = os.path.join(APP_ROOT_PATH, 'resources', 'classifiers', 'models')

# Models
MODEL_EFFICIENTNETB0 = "EfficientNetB0"




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CModelSelector(CBaseComponent):

   def __init__(self
      ,  compOpts
   ):
      super().__init__(compOpts)
      self.dfltOpts = COMP_DFLT_OPTS
      # Model
      self.model            = None



   def _getProfileData(self, profile):

      nbClasses = profile.get('nb_classes')
      classes   = profile.get('classes')
      models    = profile.get('models')

      if nbClasses is None:
         raise ValueError('Invalid classifier profile: this profile does not contain <nb_classes> attribute.')

      if (classes is None) or (len(classes) == 0):
         raise ValueError('Invalid classifier profile: this profile does not contain <classes> attribute.')

      if (models is None):
         raise ValueError('Invalid classifier profile: this profile does not contain <models> attribute.')

      return (nbClasses, classes, models)


   @st.cache
   def getClassifiers(self
      ,  jsonFileName     = CLASSIFIER_JSON_FILENAME
      ,  rootRelativePath = CLASSIFIER_ROOT_RELATIVE_PATH
   ):
      '''
      DESCRIPTION
            Loads available classifiers from input file: <jsonFileName>.
            jsonFileName should correspond to the file name.
            This function expects to find the file in the following relative path (relative to the root path of this
            streamlit application): <rootRelativePath>
      '''
      # Retrieving the application root directory
      rootPath = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]), '..'))

      # Constructing file path
      filePath = os.path.join(rootPath, rootRelativePath, jsonFileName)

      # Checking file existence
      if os.path.exists(filePath):
         # Reading the input file
         with open(filePath) as file:
            data = json.load(file)
      else:
         raise FileNotFoundError(f'Unable to load classifiers: File not found: {filePath}')

      return data.get('multiclass')



   def _loadModel(self
      ,  model
      ,  modelFilePath = DFLT_MODEL_PATH
   ):
      '''
      DESCRITPION
            This function loads the model that has been selected by the user.
      ARGUMENT
            model:
                  the model selected by the user.
                  A dictionary is expected for this argument.
                  The dictionary must contain the key 'filename' that should contain the file name of the selected model.
            modelFilePath:
                  the path where the file containing the selected model is expected to be found.
                  If None, then the default path will be used.
      '''
      # Retrieve the filename
      filename = model.get('filename')
      if filename is None:
         raise ValueError('The filename is missing for the selected model. Please contact the administrator')

      # Building the filepath
      filepath = os.path.join(modelFilePath, filename)
      if not os.path.exists(filepath):
         raise FileNotFoundError(f'File not found: {filepath}')

      # Returning the model instance
      return tf.keras.models.load_model(
            filepath       = filepath
         ,  custom_objects = None
         ,  compile        = True
         ,  options        = None
      )



   def render(self):

      with st.container():

         #
         # Component Title
         #
         # Display the component title
         title = self.getOpt('title')
         if title:
            st.subheader(title)

         # Retrieving available classifiers
         classifiers = st.session_state.get('CLASSIFIERS')
         if classifiers is None:
            classifiers = self.getClassifiers()
            st.session_state['CLASSIFIERS'] = classifiers

         #
         # Selectbox: classifier profile - selector
         #
         profileIdx = int(st.selectbox(
               label       = 'Choose a classifier profile:'
            ,  key         = ssKeys.PROFILE_IDX.value
            ,  options     = np.arange(len(classifiers))
            ,  index       = 0
            ,  format_func = lambda idx: f'Profile - {str(idx) + " - (" + str(classifiers[idx].get("nb_classes")) + " classes)"}'
            ,  help        = 'Choose the classifier profile you want to use.'
         ))

         if profileIdx is not None:

               # Retrieving models available for this selected profile
               models = classifiers[profileIdx].get('models')
               if len(models) < 1:
                  raise ValueError('No model associated to this profile ! Please contact the administrator.')

               modelNames = [ model.get('name') for model in models ]

               if len(modelNames) < 1:
                  raise ValueError('No model associated to this profile ! Please contact the administrator.')

               #
               # Selectbox: model - selector
               #
               modelIdx = st.selectbox(
                     label       = 'Model Selection'
                  ,  key         = ssKeys.MODEL_IDX.value
                  ,  options     = np.arange(len(modelNames))
                  ,  index       = 0
                  ,  format_func = lambda idx: modelNames[idx]
                  ,  help        = 'Choose the model you want to use for classification.'
               )

               #
               # Expander: Profile Description
               #
               # Here we will display the class names that this classifier profile can classify
               classes = classifiers[profileIdx].get('models')[modelIdx].get('classes')
               if classes is None or len(classes) < 1:
                  raise ValueError('No class associated to this profile ! Please contact the administrator.')

               with st.expander('Profile Description', expanded = True):
                  classesListStr = ''
                  for className in classes:
                     classesListStr += '   - ' + str(className) + '\n'
                  profileDesc = f'You have choosen a model that is able to classifiy the following genuses:\n{classesListStr}'
                  st.write(profileDesc)

               #
               # Button: "Load model"
               #
               btn_loadModel = st.button(
                     label    = 'Load Model'
                  ,  help     = 'Click on this button to load the selected model'
               )

               # Placeholder for Load status
               console = st.empty()

               # Model state instanciation
               modelState = CModelState()

               # Button: "Load model" has been clicked
               if btn_loadModel:
                  try:
                     console.info('Loading the selected model...')
                     # Retrieving the model selected by the user
                     classifiers = ss.get(ssKeys.CLASSIFIERS.value)
                     profileIdx  = ss.get(ssKeys.PROFILE_IDX.value)
                     modelIdx    = ss.get(ssKeys.MODEL_IDX.value)
                     selectedModel = classifiers[profileIdx].get('models')[modelIdx]
                     # Load the model
                     modelInstance = self._loadModel(selectedModel)
                     if modelInstance is None:
                        raise ValueError('<None Type> is not a valid model.')
                     # From here the model loading is OK
                     # Updating the model state
                     modelState.set(
                           loadSuccess   = True
                        ,  modelInstance = modelInstance
                        ,  modelName     = selectedModel.get('name')
                        ,  classNames    = selectedModel.get('classes')
                     )
                     # Registering the model state
                     modelState.register()

                  except:
                     e = sys.exc_info()[0]
                     modelState.set(
                           loadSuccess   = False
                        ,  modelInstance = None
                        ,  modelName     = None
                        ,  exception     = e
                     )
                     # Registering the model state
                     modelState.register()

               # Displaying the "load model" status
               #
               # Retrieving the model state
               modelState.setFromRegistry()
               if modelState.get() == None:
                  console.info('No model loaded yet')
               else:
                  loadSuccess = modelState.getLoadSuccess()
                  if loadSuccess is None:
                     console.info('No model loaded yet')
                  elif loadSuccess == True:
                     console.success('Model loading: [ OK ]')
                  else:
                     console.error('Model loading: [ FAILED ]')
                     e = modelState.getException()
                     if e:
                        st.exception(e)



   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')


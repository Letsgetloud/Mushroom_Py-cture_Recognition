# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import joblib                       # to load and save sklearn models
import os
import tensorflow as tf
import gdown


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#DFLT_MODEL_PATH = os.path.join('..', 'resources', 'classifiers', 'models')
DFLT_MODEL_PATH = "https://drive.google.com/uc?id="

DFLT_LOAD_MODEL_OPTS = dict(
      custom_objects = None
   ,  compile        = True
   ,  options        = None
)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Model:

   def __init__(self
      ,  modelName
      ,  instance     = None
      ,  filepath     = None
      ,  preprocessFn = None
   ):
      self.modelName    = modelName
      self.instance     = instance
      self.filepath     = filepath
      self.preprocessFn = preprocessFn


   def load(self
      ,  loadOpts = None
      ,  force    = False
   ):
      if force or self.instance is None:
         print(f'Loading the Model: {self.modelName} ...')
         if self.filepath is None:
            raise ValueError('Invalid value for parameter <filepath>: <None> is not an expected value.')
         # Set the load options
         if loadOpts is None:
            loadOpts = DFLT_LOAD_MODEL_OPTS
         # Load the model and return it
         
         output = self.modelName + ".Prod"
         gdown.download(DFLT_MODEL_PATH + self.filepath, output, quiet=False)
         
         loadedModel = tf.keras.models.load_model(
               filepath = output
            ,  **loadOpts
         )
         self.instance = loadedModel
         print('Loading done successfully')
         return self.instance


   def getName(self):
      return self.modelName


   def getInstance(self):
      return self.instance


   def getClasses(self):
      return self.classes


   def getClass(self, idx):
      if idx >= len(self.classes):
         raise IndexError('<idx>: index out of range.')
      return self.classes[idx]


   def getModelInputShape(self):
      if self.instance is not None:
         return self.instance.input.get_shape()
      raise RuntimeError('Unable to retrieve the input layer shape: the model is not loaded. Load the model and try again.')


   def setPreProcessFn(self, preprocessFn):
      self.preprocessFn = preprocessFn


   def predict(self
      ,  x
      ,  loadOpts     = None
      ,  **kwargs
   ):
      if self.instance is None:
         self.load(**loadOpts)
      if self.preprocessFn is not None:
         x = self.preprocessFn(x)
      return self.instance.predict(x, **kwargs)





class Classifier(Model):

   def __init__(self
      ,  classes
      ,  modelName
      ,  instance     = None
      ,  filepath     = None
      ,  preprocessFn = None
   ):
      super().__init__(
            modelName    = modelName
         ,  instance     = instance
         ,  filepath     = filepath
         ,  preprocessFn = preprocessFn
      )
      self.classes   = classes



class EnsembleClassifier(Classifier):

   def __init__(self
      ,  classes
      ,  modelName
      ,  instance  = None
      ,  filepath  = None
      ,  members   = None
   ):
      super().__init__(
            classes   = classes
         ,  modelName = modelName
         ,  instance  = instance
         ,  filepath  = filepath
      )
      if members is None:
         self.members = list()
      else:
         self.members = members


   def getMembers(self):
      return self.members


   def load(self
      ,  loadMembersOpts = None
      ,  force           = False
   ):
      # Set the load options for members
      if loadMembersOpts is None:
         loadMembersOpts = DFLT_LOAD_MODEL_OPTS

      # Loading the members
      for member in self.members:
         member.load(
               loadOpts = loadMembersOpts
            ,  force    = force
         )

      # Loading the ensemble model
      if force or self.instance is None:
         print(f'Loading the EnsembleClassifier: {self.modelName} ...')
         output = self.modelName + ".Prod"
         gdown.download(DFLT_MODEL_PATH + self.filepath, output, quiet=False)
         self.instance = joblib.load(output)
         print('Loading done successfully')

      return self.instance




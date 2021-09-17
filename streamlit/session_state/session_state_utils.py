# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
from enum import Enum, auto, unique
import streamlit as st





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@unique
class CSSKeys(Enum):
   MODELS_STATE                  = 'MODELS_STATE'
   MUSHROOM_CLASSIFICATION_STATE = 'MUSHROOM_CLASSIFICATION_STATE'
   IMAGE_CLASSIFICATION_STATE    = 'IMAGE_CLASSIFICATION_STATE'
   MUSHROOM_DETECTION_STATE      = 'MUSHROOM_DETECTION_STATE'
   # For app: Single Image Recognition
   SIR__IMAGE_SELECT_MODE        = 'SIR__IMAGE_SELECT_MODE'
   SIR__LOCAL_FILE_UPLOADER      = 'SIR__LOCAL_FILE_UPLOADER'
   SIR__REMOTE_FILE_UPLOADER     = 'SIR__REMOTE_FILE_UPLOADER'
   # For app: Model Interpretability
   MI__IMAGE_SELECT_MODE         = 'MI__IMAGE_SELECT_MODE'
   MI__LOCAL_FILE_UPLOADER       = 'MI__LOCAL_FILE_UPLOADER'
   MI__REMOTE_FILE_UPLOADER      = 'MI__REMOTE_FILE_UPLOADER'
   IMAGE_INTERPRETABILITY_STATE  = 'IMAGE_INTERPRETABILITY_STATE'
   INTERPRET_CHOICE_MODEL_IDX    = 'INTERPRET_CHOICE_MODEL_IDX'
   # For comp: Image Recognition
   IR__FORCE_RECOGNITION         = 'IR__FORCE_RECOGNITION'
   #
   CLASSIFIERS       = 'CLASSIFIERS'
   PROFILE_IDX       = 'PROFILE_IDX'
   MODEL_STATE       = 'MODEL_STATE'
   KEEP_LOADED_IMAGE = 'KEEP_LOADED_IMAGE'




class CSessionState():

   @staticmethod
   def remove(key):
      st.session_state.pop(key, None)

   @staticmethod
   def set(key, value):
      st.session_state[key] = value

   @staticmethod
   def get(key):
      return st.session_state.get(key)


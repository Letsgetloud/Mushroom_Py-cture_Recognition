# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import streamlit as st
import tensorflow as tf

# Import User Libraries
from session_state.base_state import CObjectStateType, CObjectState
from session_state.session_state_utils import CSSKeys as ssKeys


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CStateType(CObjectStateType):

   def __init__(self, data):
      super().__init__(data)


   @classmethod
   def isValidValue(cls
      ,  data
      ,  type
   ):
      if data is None:
         return True
      return isinstance(data, tf.keras.Model)


   @classmethod
   def isValid(cls, state):
      if state is None:
         return True
      if isinstance(state, CStateType):
         return cls.isValidValue(state.getData())
      return False




class CModelState(CObjectState):

   def __init__(self
      ,  modelKey
      ,  data = None
   ):
      state = CStateType(data = data)
      CObjectState.__init__(self, objectKey = modelKey, state = state)




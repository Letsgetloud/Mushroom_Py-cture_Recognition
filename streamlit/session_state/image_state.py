# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
from abc import abstractclassmethod
from PIL.Image import Image
import streamlit as st

# Import User Libraries
from session_state.base_state          import CObjectState
from session_state.session_state_utils import CSSKeys as ssKeys


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class CStateType():

   def __init__(self, data):
      self.setData(data)


   @classmethod
   def _isValidValue(cls, data):
      if data is None:
         return True
      return isinstance(data, Image)


   @classmethod
   def isValid(cls, state):
      if state is None:
         return True
      if isinstance(state, CStateType):
         return cls._isValidValue(state.getData())
      return False


   def getData(self):
      return self.data


   def setData(self, data):
      if not self._isValidValue(data):
         raise ValueError('Invalid value for parameter <data> in CStateType class constructor.')
      self.data = data



class CImageState(CObjectState):

   def __init__(self
      ,  imageKey
      ,  data = None
   ):
      state = CStateType(data = data)
      CObjectState.__init__(self, objectKey = imageKey, state = state)



   def isValidState(self
      ,  state = None
   ):
      return CStateType.isValid(state)


   def setData(self
      ,  data
   ):
      state = CStateType(data = data)
      super().set(state)


   def getData(self):
      state = super().get()
      if state is None:
         return None
      return state.getData()




class CImageClassificationState(CImageState):

   def __init__(self
      ,  data = None
   ):
      super().__init__(imageKey = ssKeys.IMAGE_CLASSIFICATION_STATE.value, data = data)




class CImageInterpretabilityState(CImageState):

   def __init__(self
      ,  data = None
   ):
      super().__init__(imageKey = ssKeys.IMAGE_INTERPRETABILITY_STATE.value, data = data)




'''



   def getLoadSuccess(self):
      state = self.get()
      if state:
         return state.get('loadSuccess')
      else:
         return None
'''




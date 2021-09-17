# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
      return isinstance(data, bool)


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




class CMushroomDetectionState(CObjectState):

   def __init__(self, data = None):
      state = CStateType(data = data)
      super().__init__(objectKey = ssKeys.MUSHROOM_DETECTION_STATE.value, state = state)


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


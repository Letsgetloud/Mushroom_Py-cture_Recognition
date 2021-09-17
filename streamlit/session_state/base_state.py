# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
from abc import ABC, abstractmethod
import streamlit as st

# Import User Libraries
from session_state.session_state_utils import CSessionState as ss


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CObjectStateType():

   def __init__(self, data):
      self.setData(data)


   @abstractmethod
   def isValidValue(cls
      ,  data
      ,  type
   ):
      raise NotImplementedError('This method is an abstract method and must be implemented in the child classes !')


   @classmethod
   def isValid(cls, state):
      if state is None:
         return True
      if isinstance(state, CObjectStateType):
         return cls.isValidValue(state.getData())
      return False


   def getData(self):
      return self.data


   def setData(self, data):
      if not self.isValidValue(data):
         raise ValueError('Invalid value for parameter <data> in CStateType class constructor.')
      self.data = data



class CObjectState(ABC):

   def __init__(self
      ,  objectKey
      ,  state = None
   ):
      self.key   = objectKey
      self.set(state)


   @abstractmethod
   def isValidState(self
      ,  state
   ):
      raise NotImplementedError('This method is an abstract method !')


   def get(self):
      return self.state


   def set(self, state):
      if self.isValidState(state):
         self.state = state
      else:
         raise ValueError('The parameter <state> does not correspond to a valid state for this class instance.')


   def register(self):
      ss.set(self.key, self.state)


   def unregister(self):
      ss.remove(self.key)


   def setFromRegistry(self):
      CObjectState.set(self, ss.get(self.key))

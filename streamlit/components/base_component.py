# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
from abc import ABC, abstractmethod
import streamlit as st



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CBaseComponent(ABC):

   def __init__(self
      ,  compOpts
   ):
      self.opts = compOpts


   @abstractmethod
   def getOptDflt(self, optName):
      raise NotImplementedError('This method is not implemented in the Base Class: it must be implemented in the child class.')


   @abstractmethod
   def render(self):
      pass


   def getOpt(self, optName):
      if optName in self.opts.keys():
         return self.opts.get(optName)
      return self.getOptDflt(optName)


   def showTitle(self, title):
      # Display the component title
      if title:
         st.subheader(title)





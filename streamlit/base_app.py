# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries

from abc import ABC, abstractmethod
import streamlit as st



class CBaseApp(ABC):

   def __init__(self
      ,  title = None
   ):
      self.title = title



   def showTitle(self):
      '''
      DESCRIPTION
            Display the title of the application.
            Skipped if the title has not been defined.
      '''
      if self.title:
         st.title(self.title)



   @abstractmethod
   def main(self):
      raise NotImplementedError('This method is not implemented because this is an abstract method. It must be implemented in the child class.')



   def run(self):
      self.showTitle()
      self.main()
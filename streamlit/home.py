import streamlit as st 
import os                      
import inspect                

def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    st.image(os.path.join(currentdir,  '_assets_/images/Mushroom_py-cture_recognition.png'))

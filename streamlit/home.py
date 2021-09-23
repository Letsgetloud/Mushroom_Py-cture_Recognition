import streamlit as st 
import os                      
import inspect                

def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    st.image(os.path.join(currentdir,  '_assets_/images/Mushroom_py-cture_recognition.png'))

    st.markdown(f"""
                <style>
                  .reportview-container .main .block-container{{
                    padding-top: 0 rem;
                    marging-top: 0 rem;
                  }}
                  .reportview-container .main{{
                    padding-top: 0 rem;
                    marging-top: 0 rem;
                  }}                  
                </style>
               """, unsafe_allow_html=True)
  
    st.markdown('''
          <h2>ABOUT MUSHROOM Py-CTURE RECOGNITION PROJECT</h2>
          <p>
          This project aimed at classifying a mushroom according to its genus. 
          Our model has been trained on more than 18k pictures filtered and can recognized 10 different genus with a 85% global average accuracy. 
          </p>
          <p>
          Pictures and related mushroom taxonomy have been downloaded from <a href="https://mushroomobserver.org/">mushroomobserver.org
          </p>
          <p>
          The following genus are included : </p>

                'Amanita'
                'Armillaria
                'Cortinarius'
                'Entoloma'
                'Gymnopus'
                'Hygrocybe'
                'Lactarius'
                'Marasmius'
                'Russula'
          <p>
          Our model is a combination of the 8 Efficient net CNN family model proved to perform better than individually. 
          This application is a proof of concept than can be replicated and scaled to many more genus or species if necesary.
          </p>
          It contains two main functions : 
                <h3><b><i>Classification</i></b></h3>
                <p>
                This function gives the genus predictions from the model with the corresponding probabilities. It also gives 
                details for the 8 underlying models that can illustrate possible high or low uncertainty given the picture. 
                </p>
                <h3><b><i>Explainability</i></b></h3> 
                <p>
                The Gradient Class Activation Map or Grad-CAM algorithm is implemented for the 8 Efficient Net models to show what part of the pictures 
                the models are using for their predictions. This helps understand if the correct patterns are used. If not, it can mean that
                the model has not learned properly, that the training phase should be improved, or more pictures could be needed.
                </p> 

          </p>
          ''', unsafe_allow_html=True)

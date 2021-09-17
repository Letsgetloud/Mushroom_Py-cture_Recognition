import streamlit as st 

def app():

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
          <h2>ABOUT MUSHROOM PICTURE RECOGNITION</h2>
          <p>

          </p>
          ''', unsafe_allow_html=True)
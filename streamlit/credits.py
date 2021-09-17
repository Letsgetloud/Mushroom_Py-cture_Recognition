import streamlit as st 
import os
import base64
import streamlit.components.v1 as components
import os                      
import inspect                

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url, size=50):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" height={size}px/>
        </a>'''
    return html_code


def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    logo_dataScientest = get_img_with_href(os.path.join(currentdir, '_assets_/images/datascientestLogo.png'), 'https://datascientest.com/')
    logo_MPR = get_img_with_href(os.path.join(currentdir, '_assets_/images/Mushroom_py-cture_recognition.png'), 'https://github.com/DCEN-tech/Mushroom_Py-cture_Recognition')

    c1, c2 = st.columns([0.5, 2])
    c1.markdown(logo_dataScientest, unsafe_allow_html=True) 
    c2.markdown(f'''The Mushroom Pyc-ture Recognition project was carried out as part of a Data Scientist training course at the DataScientest institute. (<a href="https://datascientest.com">datascientest.com</a>)''', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3  = st.columns([0.5, 1, 1])
    with c1:
        st.markdown(f'''<u>Project members</u> :''', unsafe_allow_html=True)  
    with c2:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, '_assets_/images/linkedin.png'), 'https://www.linkedin.com/', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/" style="text-decoration: none;color:black">David CHARLES-ELIE-NELSON</a> {logo_linkedin}''', unsafe_allow_html=True) 
    with c3:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, '_assets_/images/linkedin.png'), 'https://www.linkedin.com/in/olivier-constantin-63b1b078', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/in/olivier-constantin-63b1b078" style="text-decoration: none;color:black">Olivier CONSTANTIN</a> {logo_linkedin}''', unsafe_allow_html=True)       
  

    c1, c2 = st.columns([0.5, 2])
    c1.markdown(f'''<u>Project mentor</u> :''', unsafe_allow_html=True)  
    logo_linkedin = get_img_with_href(os.path.join(currentdir, '_assets_/images/linkedin.png'), 'https://www.linkedin.com/in/theophile-le-clerc/', 20)
    c2.markdown(f'''<a href="https://www.linkedin.com/in/theophile-le-clerc//" style="text-decoration: none;color:black">Théophile LE CLERC (DataScientest)</a> {logo_linkedin}''', unsafe_allow_html=True)    

    c1, c2 = st.columns([0.5, 2])
    c1.markdown(f'''<u>Github</u> :''', unsafe_allow_html=True)  
    c2.markdown(f'''<a href="https://github.com/DCEN-tech/Mushroom_Py-cture_Recognition">Mushroom Py-cture Recognition project</a>''', unsafe_allow_html=True) 


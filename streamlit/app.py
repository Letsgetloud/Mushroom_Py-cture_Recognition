# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard libraries
import os
import inspect
import streamlit as st
import streamlit.components.v1 as stc

# Import User libraries
import home
import about
import single_image_recognition
import multiple_image_recognition 
import credits



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


DFLT_PAGE_CONFIG = dict(
      page_title            = '[MPR] - Demo App'
   ,  page_icon             = '🍄'
   ,  layout                = 'wide'
   ,  initial_sidebar_state = 'expanded'
)

TITLE_MODE_TEXT=0
TITLE_MODE_IMAGE=1
APP_TITLE = 'MUSHROOM PY-CTURE RECOGNITION'
APP_TITLE_HTML = f'''
   <div style="background-color:#3872fb; padding:5px; border-radius:10px">
		<h1 style="color:white;text-align:center;">{APP_TITLE}</h1>
	</div>
'''

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

APP_TITLE_IMAGE = os.path.join(currentdir, '_assets_/images/Mushroom_py-cture_recognition.png')

st.set_page_config(**DFLT_PAGE_CONFIG)

MENU = {
    "Home": home,
    "About" : about,
    "Single Image Recognition" : single_image_recognition,
    "Multiple Image Recognition" : multiple_image_recognition,
    "Credits" : credits
}

choice = st.sidebar.radio('Menu', list(MENU.keys()))

page = MENU[choice]
page.app()



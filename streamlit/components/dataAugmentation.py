# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import Standard Libraries
import streamlit as st
import streamlit.components.v1 as stc

# Import User Libraries
from components.base_component import CBaseComponent



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COMP_DFLT_OPTS = dict(
   title = 'Data Augmentation'
)

DFLT_ENABLE = 1


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CDataAugmentation(CBaseComponent):

   def __init__(self
      ,  compOpts
   ):
      super().__init__(compOpts)
      self.dfltOpts = COMP_DFLT_OPTS
      self.enable   = None



   def render(self):

      with st.container():

         #
         # Component Title
         #
         # Display the component title
         title = self.getOpt('title')
         if title:
            st.subheader(title)

         #
         # Radio: enable
         #
         self.enable = st.radio(
               label       = 'Status'
            ,  key         = 'DATA_AUGMENTATION_ENABLE'
            ,  options     = [True, False]
            ,  format_func = lambda val: 'Active' if val else 'Inactive'
            ,  index       = DFLT_ENABLE
         )

         if self.enable:

            # [APPLY BRIGHTNESS SHIFT] settings
            with st.expander(label = '[ Apply BRIGHTNESS SHIFT ]', expanded = False):
               # tf.keras.preprocessing.image.apply_brightness_shift
               st.slider(
                     label = 'Brightness Shift'
                  ,  min_value = 0.1
                  ,  max_value = 1.0
                  ,  value     = 0.5
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = None
                  ,  help      = None
               )

            # [APPLY CHANNEL SHIFT] settings
            with st.expander(label = '[ Apply CHANNEL SHIFT ]', expanded = False):
               # tf.keras.preprocessing.image.apply_channel_shift
               st.slider(
                     label = 'Channel Shift - (Red)'
                  ,  min_value = 0
                  ,  max_value = 255
                  ,  value     = 0
                  ,  step      = 1
                  ,  format    = '%f'
                  ,  key       = None
                  ,  help      = 'Set a value for shiftting the Red Channel'
               )
               st.slider(
                     label = 'Channel Shift - (Green)'
                  ,  min_value = 0
                  ,  max_value = 255
                  ,  value     = 0
                  ,  step      = 1
                  ,  format    = '%f'
                  ,  key       = None
                  ,  help      = 'Set a value for shiftting the Green Channel'
               )
               st.slider(
                     label = 'Channel Shift - (Blue)'
                  ,  min_value = 0
                  ,  max_value = 255
                  ,  value     = 0
                  ,  step      = 1
                  ,  format    = '%f'
                  ,  key       = None
                  ,  help      = 'Set a value for shiftting the Blue Channel'
               )

            # [RANDOM_ROTATION] settings
            with st.expander(label = '[ Random ROTATION ]', expanded = False):
               # Left Bound
               st.slider(
                     label = 'Left Rotation'
                  ,  min_value = -0.5
                  ,  max_value = 0.0
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Rotation_LBound'
                  ,  help      = None
               )
               # Right Bound
               st.slider(
                     label = 'Right Rotation'
                  ,  min_value = 0.0
                  ,  max_value = 0.5
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Rotation_RBound'
                  ,  help      = None
               )

            # [RANDOM_SHEAR] settings
            with st.expander(label = '[ Random SHEAR ]', expanded = False):
            # tf.keras.preprocessing.image.random_shear
               # Value
               st.slider(
                     label = 'Value'
                  ,  min_value = 0.0
                  ,  max_value = 0.45
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Random_Shear Value'
                  ,  help      = None
               )

            # [RANDOM_SHIFT] settings
            with st.expander(label = '[ Random SHIFT ]', expanded = False):
            # tf.keras.preprocessing.image.random_shift
               # Width Shift Value
               st.slider(
                     label = 'WIDTH shift value'
                  ,  min_value = 0.0
                  ,  max_value = 0.40
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Width shift'
                  ,  help      = None
               )
               # Height Shift Value
               st.slider(
                     label = 'HEIGHT shift value'
                  ,  min_value = 0.0
                  ,  max_value = 0.40
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Height shift'
                  ,  help      = None
               )


            # [RANDOM_ZOOM] settings
            with st.expander(label = '[ Random ZOOM ]', expanded = False):
            # tf.keras.preprocessing.image.random_zoom
               # Width Zoom Value
               st.slider(
                     label = 'WIDTH zoom value'
                  ,  min_value = 0.0
                  ,  max_value = 0.40
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Width zoom'
                  ,  help      = None
               )
               # Height Zoom Value
               st.slider(
                     label = 'HEIGHT zoom value'
                  ,  min_value = 0.0
                  ,  max_value = 0.40
                  ,  value     = 0.0
                  ,  step      = 0.01
                  ,  format    = '%f'
                  ,  key       = 'Height zoom'
                  ,  help      = None
               )


   def getOptDflt(self, optName):
      if optName in self.dfltOpts.keys():
         return self.dfltOpts.get(optName)
      raise ValueError(f'Invalid option name: "{optName}". This option does not exist for this component.')



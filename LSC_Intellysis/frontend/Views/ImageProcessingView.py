import os
import streamlit as st
from PIL import Image

class ImageProcessingView:
    def __init__(self):
      css_path = os.path.join(os.path.dirname(__file__), "../styles.css")
      absolute_css_path = os.path.abspath(css_path)
      st.markdown(f"<style>{open(absolute_css_path).read()}</style>", unsafe_allow_html=True)

    def display(self,result=None):
      # If we have a result to display
      if result is not None:
        self.display_result(result)
    
    def display_result(self, result):
      name, extension, accuracy, error_rate, classification = result
      res_path = 'runs/detect/predict'+str(st.session_state.ctr)+'/'+ name +"."+ extension

      # Display analyzed video/image
      if extension == "mp4":
          st.subheader("Analyzed Video")
          st.video(res_path)
      else:
          res_img = Image.open(res_path)
          st.subheader("Analyzed Image")
          st.image(res_img, use_column_width=True)

      # Creates a button for exporting the image result
      export_btn = st.button("Export")
       

      col1, col2, col3, col4 = st.columns(4)

      with col1:
        st.markdown("**:blue[File Name]**")
        st.write(name + extension)
        
      with col2:
        st.markdown("**:blue[Classification]**")
        if(classification < 1):
          st.write("Good")
        else:
          st.write("No Good")
        
      with col3:
        st.markdown("**:blue[Accuracy Rate]**")
        st.write(str(accuracy) + "%")
        
      with col4:
        st.markdown("**:blue[Error Rate]**")
        st.write(str(error_rate) + "%")

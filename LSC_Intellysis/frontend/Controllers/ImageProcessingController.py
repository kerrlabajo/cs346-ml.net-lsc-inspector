import os
import streamlit as st
import datetime
import gridfs
from PIL import Image
from streamlit_option_menu import option_menu

from render_dashboard import render_dashboard
from render_home import render_home
from render_history import render_history
from render_archived import render_archived
from render_settings import render_settings

class ImageProcessingController:
  def __init__(self, model, view):
    self.model = model
    self.view = view
    self.pages = {
      "Dashboard": render_dashboard,
      "Home": render_home,
      "History": render_history,
      "Archived": render_archived,
      "Settings": render_settings,
    }
    self.file_path = None
    self.file_extension = None
    self.selected = None
    if 'ctr' not in st.session_state:
      st.session_state.ctr = 2

  def run(self):
    with st.sidebar:
      self.selected = option_menu(
        menu_title=None,
        options=list(self.pages.keys()),
        icons=["clipboard", "house", "clock-history", "archive", "gear"],
        menu_icon="cast",
        default_index=1,
        styles={
          "container": {"background-color": "#48BF91", "border-radius": "0px"},
          "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#DFDFDF"},
          "nav-link-selected": {"background-color": "#0076BE"}
        }
      )
    if self.selected in self.pages:
          self.pages[self.selected]()
    if self.selected == "Home":
        self.main()

  def main(self):
    st.subheader("Detect laser soldering condition in real time.")
    rt_detection_btn = st.button("External Camera")

    if rt_detection_btn:
      st.session_state.ctr += 1
      self.model.predict(source="http://192.168.43.50:4747/video", show=True, conf=0.25, save=False)

    # Image upload button
    st.subheader("Upload a file")
    # + InputFile: InputFile
    uploaded_file = st.file_uploader("", type=["mp4", "png", "jpg", "jpeg"])

    # Process the uploaded image if available
    if uploaded_file is not None:
      # Check the file extension
      self.file_extension = uploaded_file.name.split(".")[-1].lower()
      self.file_path = os.path.join("../test/", uploaded_file.name)
      with open(self.file_path, 'wb') as out:
        out.write(uploaded_file.read())
      if self.file_extension == "mp4":
        st.subheader("Uploaded Video")
        st.video(uploaded_file)
      else:
        image = Image.open(uploaded_file)
        st.subheader("Uploaded Image")
        st.image(image, use_column_width=True)

      # Analyze Button
      analyze_btn = st.button("Analyze")

      if analyze_btn:
        self.analyze_uploaded_file(uploaded_file)
        self.view.display(self.model.getFile())

  # + analyze(File): void
  def analyze_uploaded_file(self, file):
    st.session_state.ctr += 1
    self.model.analyze_image(self.file_path)

    print("---------------------------------------------------------------------")
    name, extension, accuracy, error_rate, classification = self.model.getFile()
    print("---------------------------------------------------------------------")
    print(name, extension)
    with open(self.file_path, "rb") as file:
      image_data = file.read()
    data = {
      "file_path": self.file_path,
      "file_name": name,
      "extension": extension,
      "classification": classification,
      "accuracy": accuracy,
      "error_rate": error_rate,
      "timestamp": datetime.datetime.now(),
      "image_data": image_data
    }

    self.model.insertIntoDB(data)

  # Missing store Data

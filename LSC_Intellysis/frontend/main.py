import os
import cv2
import streamlit as st
from PIL import Image
from ultralytics import YOLO  
from streamlit_option_menu import option_menu
# from ultralytics.yolo.v8.detect.predict import DetectionPredictor

from render_dashboard import render_dashboard
from render_home import render_home
from render_history import render_history
from render_archived import render_archived
from render_settings import render_settings

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
absolute_css_path = os.path.abspath(css_path)

st.markdown(f"<style>{open(absolute_css_path).read()}</style>", unsafe_allow_html=True)

st.title("LSC Quality Evaluator")

model = YOLO("../runs/detect/train7/weights/best.pt")
# model.predict(source="http://192.168.1.2:4747/video", show=True, conf=0.25, save=True)

# Display the video
# video_file = open('runs/detect/predict4/test.mp4', "rb")
# video_bytes = video_file.read()

# st.video('runs/detect/predict4/test.mp4')
# res_path = "runs/detect/predict6/Test3.png"
# res_img = Image.open(res_path)
# image_width = 500

# st.image(res_img, width=image_width)

def main():
  if 'ctr' not in st.session_state:
    st.session_state.ctr = 2
  # Create sidebar
  pages = {
    "Dashboard": render_dashboard,
    "Home": render_home,
    "History": render_history,
    "Archived": render_archived,
    "Settings": render_settings,
  }
  
  st.subheader("Detect laser soldering condition in real time.")
  rt_detection_btn = st.button("External Camera")

  if rt_detection_btn:
    model.predict(source="http://192.168.1.2:4747/video", show=True, conf=0.25, save=True)

  # Image upload button
  st.subheader("Upload a file")
  uploaded_file = st.file_uploader("", type=["mp4", "png", "jpg", "jpeg"])

  # Process the uploaded image if available
  if uploaded_file is not None:
    # Check the file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()
    file_path = os.path.join("../test/", uploaded_file.name)
    with open(file_path, 'wb') as out:
        out.write(uploaded_file.read())

    if file_extension == "mp4":
      st.subheader("Uploaded Video")
      st.video(uploaded_file)
    else:
      image = Image.open(uploaded_file)
      st.subheader("Uploaded Image")
      image_width = 500
      st.image(image, width=image_width)

    # Analyze Button
    analyze_btn = st.button("Analyze")

    if analyze_btn:
      st.session_state.ctr += 1
      print(st.session_state.ctr)
      analyze_image(file_path)
      string=uploaded_file.name
      res_path = 'runs/detect/predict'+str(st.session_state.ctr)+'/'+string
      if file_extension == "mp4":
        st.subheader("Analyzed Video")
        st.video(res_path)

      else:
        res_img = Image.open(res_path)
        image_width = 500
        st.subheader("Analyzed Image")
        st.image(res_img, width=image_width)

      # Analyze Button
      export_btn = st.button("Export")

      if export_btn:
        export_image(res_img)

    
def analyze_image(file):
  return model.predict(source=file, show=False, conf=0.20, save=True)

  # Save the image to a file
def export_image(image):
  image.save(image, format='png')
  st.success("Image exported successfully!")

with st.sidebar:
            selected = option_menu(
                menu_title=None,  # required
                options=["Dashboard", "Home", "History", "Archived", "Settings"],  # required
                icons=["clipboard", "house", "clock-history", "archive", "gear"],  # optional
                menu_icon="cast",  # optional
                default_index=1,  # optional
                styles={
        "container": {"background-color": "#48BF91", "border-radius": "0px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#DFDFDF"},
        "nav-link-selected": {"background-color": "#0076BE"}
    }
            )
if selected == "Dashboard":
    render_dashboard()
if selected == "Home":
    render_home()
    main()
if selected == "History":
    render_history()
if selected == "Archived":
    render_archived()
if selected == "Settings":
    render_settings()
if __name__ == "__main__":
  selected = "Home"
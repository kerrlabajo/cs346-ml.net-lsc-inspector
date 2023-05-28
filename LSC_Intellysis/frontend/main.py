import os
import cv2
import streamlit as st
from PIL import Image
from ultralytics import YOLO  
from streamlit_option_menu import option_menu

from render_dashboard import render_dashboard
from render_home import render_home
from render_history import render_history
from render_archived import render_archived
from render_settings import render_settings

# This code is creating a file path for a CSS file named "styles.css" located in the same directory as
# the current Python file.
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
absolute_css_path = os.path.abspath(css_path)

# This code is adding a custom CSS file named "styles.css" to the Streamlit app using the
# `st.markdown()` function. It first reads the contents of the CSS file using the `open()` function
# and the `read()` method, and then wraps the contents in a `<style>` tag using an f-string. The
# resulting string is then passed as the first argument to `st.markdown()`, which renders the CSS
# styles in the Streamlit app. The `st.title()` function is also used to display a title for the
# Streamlit app.
st.markdown(f"<style>{open(absolute_css_path).read()}</style>", unsafe_allow_html=True)
st.title("LSC Quality Evaluator")

# This creates an instance of the YOLO class
# from the ultralytics library and loading a pre-trained YOLOv5 model from the file path
# "../runs/detect/train7/weights/best.pt". This model can be used to make predictions on images or
# videos.
model = YOLO("../runs/detect/train7/weights/best.pt")

def main():
  if 'ctr' not in st.session_state:
    st.session_state.ctr = 2
    
  # This code block is creating a dictionary called `pages` that maps the names of different pages in
  # the Streamlit app to their corresponding rendering functions. Each key in the dictionary
  # represents the name of a page, and each value represents the function that should be called to
  # render that page. This dictionary is likely used to switch between different pages in the
  # Streamlit app based on user input.  
  pages = {
    "Dashboard": render_dashboard,
    "Home": render_home,
    "History": render_history,
    "Archived": render_archived,
    "Settings": render_settings,
  }
  
  # This code is displaying a subheader in the Streamlit app with the text "Detect laser soldering
  # condition in real time." and creating a button with the label "External Camera". When the
  # "External Camera" button is clicked, it tries to make a prediction using the pre-trained YOLOv5
  # model on a video stream from an external camera with the specified IP address and port number. If
  # there is an error during the prediction, it displays an error message in the Streamlit app.
  st.subheader("Detect laser soldering condition in real time.")
  rt_detection_btn = st.button("External Camera")

  # This code block is checking if the "External Camera" button has been clicked in the Streamlit app.
  # If the button has been clicked, it tries to make a prediction using the pre-trained YOLOv5 model
  # on a video stream from an external camera with the specified IP address and port number. If there
  # is an error during the prediction, it displays an error message in the Streamlit app.
  if rt_detection_btn:
        try:
          model.predict(source="http://192.168.43.50:4747/video", show=True, conf=0.20, save=False)
        except Exception as e:
          st.error(f"Error: {e}")
        
  # Displays a subheader in the Streamlit app with the text
  # "Upload a file".
  st.subheader("Upload a file")
  uploaded_file = st.file_uploader("null", type=["mp4", "png", "jpg", "jpeg"])

  # Checks if a file has been uploaded by the user. If a file has
  # been uploaded, the code inside the if statement will be executed, otherwise it will be skipped.
  if uploaded_file is not None:
        
    # This code block is extracting the file extension of the uploaded file using the `split()` method
    # and converting it to lowercase using the `lower()` method. It then creates a file path for the
    # uploaded file in the "../test/" directory using `os.path.join()`. Finally, it opens the file in
    # binary write mode using `open()` and writes the contents of the uploaded file to the file path
    # using `out.write(uploaded_file.read())`.
    file_extension = uploaded_file.name.split(".")[-1].lower()
    file_path = os.path.join("../test/", uploaded_file.name)
    with open(file_path, 'wb') as out:
        out.write(uploaded_file.read())

    # This code block is checking the file extension of the uploaded file. If the file extension is
    # "mp4", it displays a subheader in the Streamlit app with the text "Uploaded Video" and shows the
    # uploaded video using `st.video(uploaded_file)`. If the file extension is not "mp4", it opens the
    # uploaded file as an image using `Image.open(uploaded_file)`, displays a subheader in the
    # Streamlit app with the text "Uploaded Image", and shows the uploaded image using
    # `st.image(image, width=image_width)`.
    if file_extension == "mp4":
      st.subheader("Uploaded Video")
      st.video(uploaded_file)
    else:
      image = Image.open(uploaded_file)
      st.subheader("Uploaded Image")
      image_width = 500
      st.image(image, width=image_width)

    # `analyze_btn = st.button("Analyze")` creates a button in the Streamlit app with the label
    # "Analyze". When the button is clicked, the code inside the `if analyze_btn:` block is executed.
    # This code increments the `ctr` variable in the `st.session_state` dictionary by 1, prints the
    # value of `ctr` to the console, and calls the `analyze_image()` function with the `file_path`
    # argument. It then creates a file path for the analyzed image or video in the
    # "../runs/detect/predict{ctr}/" directory using `os.path.join()`. Finally, it displays the
    # analyzed image or video in the Streamlit app using `st.image()` or `st.video()`, depending on
    # the file extension of the uploaded file, and creates an "Export" button that calls the
    # `export_image()` function when clicked. The `export_image()` function saves the analyzed image
    # to a file in PNG format and displays a success message in the Streamlit app.
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

      # `export_btn = st.button("Export")` creates a button in the Streamlit app with the label
      # "Export".
      export_btn = st.button("Export")
      if export_btn:
        export_image(res_img)

def analyze_image(file):
  """
  This function takes an image file as input and uses a pre-trained model to predict its contents with
  a confidence threshold of 0.20, while also saving the results.
  
  :param file: The file parameter is the input image file that needs to be analyzed. It could be a
  local file path or a URL to an image
  :return: the result of the `model.predict()` method, which is likely a prediction or analysis of the
  image file passed as the `file` parameter. The `show`, `conf`, and `save` parameters are likely
  options for how the prediction is displayed or saved. Without more information about the `model`
  object and its methods, it is difficult to determine the exact nature of the
  """
  return model.predict(source=file, show=False, conf=0.20, save=True)

def export_image(image):
  # This code is saving the `image` object in PNG format using the `save()` method and then displaying
  # a success message in the Streamlit app using the `st.success()` function. The `image` object is
  # likely the result of an image analysis or prediction made by the `analyze_image()` function. The
  # `format='png'` argument specifies that the image should be saved in PNG format.
  image.save(image, format='png')
  st.success("Image exported successfully!")

# This code block is creating a sidebar in the Streamlit app that contains a dropdown menu with
# options for different pages in the app. The `option_menu()` function is used to create the dropdown
# menu, and it takes several arguments, including the title of the menu (`menu_title`), the options to
# be displayed in the menu (`options`), and the default index of the selected option
# (`default_index`). The `icons` argument is optional and allows you to specify icons to be displayed
# next to each option in the dropdown menu. The `styles` argument is also optional and allows you to
# specify CSS styles for different elements of the dropdown menu. The `selected` variable is assigned
# the value of the selected option in the dropdown menu. Depending on the value of `selected`,
# different rendering functions for different pages in the app will be called.
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
  
# This code block is checking the value of the `selected` variable, which is determined by the user's
# selection in the dropdown menu in the sidebar. Depending on the value of `selected`, it calls a
# different rendering function to display a different page in the Streamlit app. The `if __name__ ==
# "__main__":` line ensures that the code inside the block is only executed if the Python script is
# being run as the main program, rather than being imported as a module into another program. Finally,
# it sets the default value of `selected` to "Home".  
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
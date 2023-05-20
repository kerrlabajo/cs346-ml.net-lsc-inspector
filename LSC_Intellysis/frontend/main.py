import streamlit as st
import os
from PIL import Image
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
absolute_css_path = os.path.abspath(css_path)

st.markdown(f"<style>{open(absolute_css_path).read()}</style>", unsafe_allow_html=True)

st.title("LSC Quality Evaluator")

# image_path = "../test/Test1.png"
# img = Image.open(image_path)

model = YOLO("../runs/detect/train7/weights/best.pt")
# result = model.predict(source="../test/test6.png", show=False, conf=0.5, save=True)

# print(img)
# Get the original image
# res_path = "runs/detect/predict6/Test6.png"
# res = Image.open(res_path)

# st.image(res)

def main():
    # Create sidebar

    pages = {
      "Dashboard": render_dashboard,
      "Home": render_home,
      "History": render_history,
      "Archived": render_archived,
      "Settings": render_settings,
    }

    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["Home"])[0]

    for page_name, page_func in pages.items():
      button = st.sidebar.button(page_name, key=page_name, use_container_width=True)
      if button:
        query_params["page"] = page_name
        st.experimental_set_query_params(**query_params)
        page_func()


    # Image upload button
    uploaded_file = st.file_uploader("Upload an image")
    print(uploaded_file)
    # Process the uploaded image if available
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        print(uploaded_file)
        st.subheader("Uploaded Image")
        image_width = 500
        aspect_ratio = image.width / image.height
        image_height = int(image_width / aspect_ratio)
        st.image(image, width=image_width)
        analyze_button = st.button("Analyze")
        if analyze_button:
            analyze_image(uploaded_file)

        # result = model.predict(source=image, show=False, conf=0.5, save=True)

        # # Get the original image
        # res_path = "runs/detect/predict/Test1.png"
        # res = Image.open(res_path)

        # st.image(res)


def analyze_image(file):
    res_img = Image.open(file)
    print("Image here: ")
    print(res_img.info)
    st.subheader("Analyzed Image")
    image_width = 500
    aspect_ratio = res_img.width / res_img.height
    image_height = int(image_width / aspect_ratio)
    # st.image(res_img, width=image_width)  

    result = model.predict(source=res_img.filename + res_img.format, show=False, conf=0.5, save=True)
    # Get the original image
    # res_path = "runs/detect/predict6/Test6.png"
    # res = Image.open(res_path)

    # st.subheader("Analyzed Image")
    # st.image(res)


def render_dashboard():
    st.title("Dashboard")
    st.write("Welcome to the Dashboard page.")


def render_home():
    st.title("Home")
    st.write("Welcome to the Home page.")


def render_history():
    st.title("History")
    st.write("Here is your browsing history.")


def render_archived():
    st.title("Archived")
    st.write("Your archived items are displayed here.")


def render_settings():
    st.title("Settings")
    st.write("Customize your application settings here.")


if __name__ == "__main__":
    main()

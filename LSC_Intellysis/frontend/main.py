import streamlit as st
import os
from PIL import Image
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2
import torch

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
absolute_css_path = os.path.abspath(css_path)

st.markdown(f"<style>{open(absolute_css_path).read()}</style>", unsafe_allow_html=True)

st.title("LSC Quality Evaluator")

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))

# image_path = "../test/Test1.png"
# img = Image.open(image_path)

model = YOLO("../runs/detect/train7/weights/best.pt")
result = model.predict(source="0", show=False, conf=0.5)
# print(img)
# # Get the original image
# res_path = "runs/detect/predict/Test1.png"
# res = Image.open(res_path)

# st.image(res)

def main():
    # Create sidebar

    # Add items to the sidebar
    history_button = st.sidebar.button(
        "Dashboard", key="Dashboard", use_container_width=True
    )
    home_button = st.sidebar.button("Home", key="Home", use_container_width=True)
    history_button = st.sidebar.button(
        "History", key="History", use_container_width=True
    )
    archived_button = st.sidebar.button(
        "Archived", key="Archived", use_container_width=True
    )
    settings_button = st.sidebar.button(
        "Settings", key="Settings", use_container_width=True
    )

    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["home"])[0]

    # Render sidebar items
    if home_button:
        query_params["page"] = "home"
        st.experimental_set_query_params(**query_params)
        render_home()

    elif history_button:
        query_params["page"] = "history"
        st.experimental_set_query_params(**query_params)
        render_history()

    elif archived_button:
        query_params["page"] = "archived"
        st.experimental_set_query_params(**query_params)
        render_archived()

    elif settings_button:
        query_params["page"] = "settings"
        st.experimental_set_query_params(**query_params)


# Image upload button
uploaded_file = st.file_uploader("Upload an image")
print(uploaded_file)
# Process the uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Uploaded Image")
    image_width = 500
    aspect_ratio = image.width / image.height
    image_height = int(image_width / aspect_ratio)
    st.image(image, width=image_width)
  

    # result = model.predict(source=image, show=False, conf=0.5, save=True)

    # # Get the original image
    # res_path = "runs/detect/predict/Test1.png"
    # res = Image.open(res_path)

    # st.image(res)


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

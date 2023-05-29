import streamlit as st

from Controllers.ImageProcessingController import ImageProcessingController
from Models.ImageProcessingModel import ImageProcessingModel
from Views.ImageProcessingView import ImageProcessingView


if __name__ == "__main__":
    # st.title("LSC Qualitative Inspective")

    model = ImageProcessingModel("../runs/detect/train7/weights/best.pt")
    view = ImageProcessingView()
    controller = ImageProcessingController(model, view)
    controller.run()
import streamlit as st
import torch
from torchvision import transforms
from PIL import Image

st.title("LSC Quality Evaluator")


def main():
    # Create sidebar

    # Add items to the sidebar
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
        # Update the URL with the "page" parameter set to "home"
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

# Process the uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Uploaded Image")
    st.image(image)


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

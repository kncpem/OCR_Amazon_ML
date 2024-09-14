import streamlit as st
import base64
import numpy as np
import io
from PIL import Image
from OCR import get_text

# Set up the page configuration
st.set_page_config(page_title="README.ME", page_icon=":memo:", layout="centered")

# Title and Header
st.title("README.ME")
st.header("A CS 6220 Project")
st.subheader("Creators: Mohak Chadha, Edward Chiao, Rishabh Ghora, Thor Keller, Priyansh Srivastava")

# File uploader for the user to upload an image
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

def resize_input(im):
    """
    Helper function that resizes an image
    if it is too big to fit on the screen
    im: image inputted by the user
    resized_im: resized image
    """
    resized_im = im
    if im.size[0] > 1000:
        ratio = im.size[0] / 1000
        resized_im = im.resize((round(im.size[0] / ratio), round(im.size[1] / ratio)))
    return resized_im

def parse_contents(image):
    """
    Takes in the uploaded image, extracts text using OCR,
    and returns the resized image and detected text.
    """
    im = Image.open(image)
    arr = np.asarray(im)
    text = get_text(arr)
    resized_im = resize_input(im)
    
    return resized_im, text

# If a file is uploaded, display the image and extracted text
if uploaded_file is not None:
    # Display progress spinner
    with st.spinner("Processing..."):
        image, detected_text = parse_contents(uploaded_file)
    
    # Display the original filename
    st.write(f"**Original Filename:** {uploaded_file.name}")

    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Display the extracted text
    st.subheader("Detected Text")
    st.write(detected_text)

    # Download the extracted text as a .txt file
    st.download_button(
        label="Download .txt file",
        data=detected_text,
        file_name=f"{uploaded_file.name.split('.')[0]}.txt",
        mime="text/plain",
    )

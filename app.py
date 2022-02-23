import streamlit as st
from PIL import Image
import os
from model import process_image

st.set_page_config(page_title="Color Quantizer", page_icon=':art:', layout='wide')

# Remove streamlit watermark
style = """
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
"""
st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

st.title("Color Quantizer :art:")
st.subheader("Reduce the color palette of your image to any number of colors")

st.sidebar.title("Input here", )

if os.path.exists(os.path.join("image_files","quantized_image.png")):
    os.remove(os.path.join("image_files","quantized_image.png"))
if os.path.exists(os.path.join("image_files","input_file.png")):
    os.remove(os.path.join("image_files","input_file.png"))

input_file_path = os.path.join("image_files","sample_input.png")
output_file_path = os.path.join("image_files","sample_output.png")

with st.sidebar:
    with st.form("user_input"):
        uploaded_file = st.file_uploader(label="Upload your Image for Quantization", type = ['jpg', 'jpeg', 'png'])
        k = st.number_input(label = "Enter the number of colors: ", min_value=2, value=6)
        submit = st.form_submit_button("Submit")
        if submit:
            if uploaded_file is None:
                st.warning("Please upload the picture file before submitting.")
            else:
                st.write("File uploaded successfully!")
                try:
                    input_file_path = os.path.join("image_files", "input_file.png")
                    output_file_path = os.path.join("image_files","quantized_image.png")
                except:
                    st.warning("Internal Server Error")
            st.write("Number of colors chosen: ", k)

try:
    if uploaded_file is not None:
        print("File uploaded successfully!")
        image = uploaded_file
    else:
        image = None
except:
    st.warning("Internal Server Error")

try:
    if image is not None:
        with open(input_file_path, "wb") as f:
            f.write(image.getbuffer())
        img = Image.open(input_file_path)
    else:
        img = None
except:
    st.warning("Internal Server Error")


with st.container():
    left_column,center_column, right_column = st.columns((2,0.5,2))
    with left_column:
        st.write("### Your Original Image: ")
        try:
            if img is not None:
                st.image(img)
            else:
                st.image(Image.open(os.path.join("image_files", "sample_input.png")))
        except:
            st.warning("Internal Server Error")
    with center_column:
        st.write("#")
    with right_column:
        st.write("### Your Quantized Image: ")
        try:
            if submit:
                if uploaded_file is not None:
                    with st.spinner("Your picture is processing..."):
                        if image is not None:
                            process_image(image, k, output_file_path)
                            output_image = Image.open(output_file_path)
                            st.image(output_image)
                            with open(output_file_path,'rb') as file:
                                download_btn = st.download_button(label="Download", data=file, file_name='quantized_image.png', mime="image/png")
            else:
                st.image(Image.open(os.path.join("image_files", "sample_output.png")))
        except:
            st.warning("Internal Server Error")

st.write("#")
st.write("#")
st.write("You can convert you pictures with wide range of colors to any no. of colors you want.")
st.write("This will help you to reduce your color palette, and help you choose important colors if you want to paint the picture.")

# Q&A Chatbot

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()  # Take environment variables from .env

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_text, image_data, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read file bytes and prepare image parts
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # MIME type of the uploaded file
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.title("Gemini Application")

# Define a placeholder at the top for the response
response_placeholder = st.container()
with response_placeholder:
    st.subheader("The Response is")
    response_text = st.empty()  # Placeholder for response text

# User input fields
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
if st.button("Submit"):
    # Ensure both input text and an uploaded image are provided
    if uploaded_file and input_text:
        try:
            # Prepare the input image data
            image_data = input_image_setup(uploaded_file)

            # Prompt for the Gemini model
            input_prompt = """
            You are an expert in understanding invoices.
            You will receive input images as invoices &
            you will have to answer questions based on the input image.
            """

            # Get response from Gemini
            response = get_gemini_response(input_text, image_data, input_prompt)

            # Display the response at the top
            with response_placeholder:
                response_text.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload an image and provide an input prompt.")

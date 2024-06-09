import streamlit as st
import google.generativeai as genai
import os

# Debug: Check if the environment variable is set
credential_path = "C:/Users/insiy/OneDrive/Desktop/SmartPrix/femtech-425900-d7ef88ff9545.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
# st.write(f"GOOGLE_APPLICATION_CREDENTIALS: {credential_path}")

if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    st.error("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set or incorrectly set.")
else:
    try:
        # Configure the Google AI API key
        api_key = "YOUR API KEY HERE"
        if not api_key:
            st.error("API key is not set. Please set your API key.")
        else:
            genai.configure(api_key=api_key)

            # Function to upload the file to Gemini and get the file URI
            def upload_to_gemini(path, mime_type=None):
                try:
                    file = genai.upload_file(path, mime_type=mime_type)
                    return file.uri
                except Exception as e:
                    st.error(f"File upload failed: {e}")
                    return None

            # Function to generate dimensions using Google AI's Gemini API
            def generate_dimensions(file_uri, area):
                try:
                    generation_config = {
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain",
                    }

                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        generation_config=generation_config,
                    )

                    chat_session = model.start_chat(
                        history=[
                            {
                                "role": "user",
                                "parts": [
                                    f"I have an area of {area} sqft. Here is the floor plan: {file_uri}. Give dimensions in int value for the area floor plan.",
                                ],
                            },
                        ]
                    )

                    response = chat_session.send_message(f"I have an area of {area} sqft. Here is the floor plan: {file_uri}. Give dimensions in int value for the area floor plan.")
                    return response.text
                except Exception as e:
                    st.error(f"Dimension generation failed: {e}")
                    return None

            # Streamlit UI
            st.title("Floor Plan Dimension Generator")
            st.write("Upload an image of the floor plan and enter the total area in square feet.")

            uploaded_file = st.file_uploader("Upload Floor Plan Image", type=["jpg", "jpeg", "png"])
            total_area = st.number_input("Total Area (sqft)", min_value=1)
            if st.button("Give Dimensions"):
                if uploaded_file and total_area:
                    with open("temp_image.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    file_uri = upload_to_gemini("temp_image.jpg", mime_type=uploaded_file.type)
                    if file_uri:
                        dimensions = generate_dimensions(file_uri, total_area)
                        if dimensions:
                            st.write("Generated Dimensions:")
                            st.write(dimensions)
    except Exception as e:
        st.error(f"An error occurred: {e}")

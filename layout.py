import streamlit as st
import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'YOUR API KEY'

# Function to generate an image using DALL·E 3
def generate_image(prompt, n=1, size='1024x1024'):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=n,
        size=size
    )
    return response

# Streamlit app
def main():
    st.title("Floor Plan Image Generator")
    
    # Get user inputs
    view = st.radio("Which of the following you require:", ["2D", "3D"], index= None)
    bedrooms = st.number_input("Number of Bedrooms", min_value=1, step=1)
    bathrooms = st.number_input("Number of Bathrooms", min_value=1, step=1)
    kitchen = st.number_input("Number of Kitchen", min_value=1, step=1)
    LivingRoom = st.number_input("Number of living Rooms")
    Guest_Bedroom = st.number_input("No.of Guest Bedroom")

    
    # Generate the prompt
    prompt = f"""Generate a detailed {view} realistic floor plan blueprint for a residential house based on specified requirements.

BedRoom = {bedrooms}
Bathroom = {bathrooms}
kitchen = {kitchen}
LivingvRoom = {LivingRoom}
Output Format:
The floor plan should be presented as a clear, top-down view image with all the specified rooms and features accurately represented. The image should be high resolution and easy to read, with labels for each room and major elements."""
    
    if st.button("Generate Image"):
        try:
            response = generate_image(prompt)
            for i, data in enumerate(response['data']):
                image_url = data['url']
                st.image(image_url, caption=f"Image {i+1}", use_column_width=True)
        except openai.error.OpenAIError as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

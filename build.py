import streamlit as st
import openai
from gtts import gTTS
import os

# Function to get user input
def get_user_input(prompt, options, tooltip=None):
    st.subheader(prompt)
    if tooltip:
        st.info(tooltip)
    choice = st.radio("", options)
    return choice

# Function to generate audio from text
def generate_audio(text, filename="recommendation_plan.mp3"):
    tts = gTTS(text)
    tts.save(filename)

# Function to play audio
def play_audio(filename="recommendation_plan.mp3"):
    st.audio(filename, format="audio/mp3")

def main():
    # Set your OpenAI API key here
    openai.api_key = "YOUR API KEY HERE"

    # Set page title and layout
    st.set_page_config(page_title="Architectural Recommendation System", layout="wide")

    # Set sidebar
    st.sidebar.title("Options")
    st.sidebar.info("This app generates architectural recommendation plans based on user preferences.")
    st.sidebar.markdown("---")

    # Preferences, requirements, and constraints inputs
    st.title("Architectural Recommendation System")
    st.subheader("User Preferences")

    # User input columns
    col1, col2, col3 = st.columns(3)

    # Get user inputs
    with col1:
        aesthetic_style = get_user_input("Aesthetic Style:", ["Minimalist", "Industrial", "Scandinavian"], "The visual theme or appearance desired for the building.")

    with col2:
        spatial_layout = get_user_input("Spatial Layout Preference:", ["Open plan", "Traditional", "Biophilic design"], "Preference for how the interior space is organized and utilized.")

    with col3:
        architectural_style = get_user_input("Architectural Style:", ["Classical", "Modernist", "Contemporary"], "The overarching design approach or historical reference guiding the building's appearance.")

    st.subheader("Requirements and Constraints")

    # Use expanders for detailed inputs
    with st.expander("Structural Requirements", expanded=True):
        structural_requirements = get_user_input("Structural Requirements:", ["High strength", "Lightweight", "Fire-resistant"], "Specific needs regarding the stability and strength of the building's framework and support systems.")

    with st.expander("Environmental Considerations", expanded=True):
        environmental_considerations = get_user_input("Environmental Considerations:", ["Sustainable", "Recyclable", "Locally sourced"], "Factors related to sustainability, energy efficiency, and environmental impact.")

    with st.expander("Cost Constraints", expanded=True):
        cost_constraints = get_user_input("Cost Constraints:", ["Budget-friendly", "Cost-effective alternatives", "High-end"], "Financial limitations impacting the budget for construction and materials.")

    st.subheader("Load and Site Conditions")

    with st.expander("Load Requirements", expanded=True):
        load_requirements = get_user_input("Load Requirements:", ["High-rise", "Residential", "Seismic-prone"], "The expected weight or stress the building must support, including occupants, equipment, and environmental factors.")

    with st.expander("Type of Building", expanded=True):
        building_type = get_user_input("Type of Building:", ["Office building", "Warehouse", "School"], "The purpose or function of the structure, such as residential, commercial, or industrial.")

    with st.expander("Site Conditions", expanded=True):
        site_conditions = get_user_input("Site Conditions:", ["Sloped terrain", "Flood-prone area", "Seismic zone"], "Factors related to the location and environment where the building will be constructed.")

    # Add 'Get Recommendation Plan' button
    if st.button("Get Recommendation Plan", help="Click to generate recommendation plan based on inputs"):
        with st.spinner("Generating recommendation plan..."):
            try:
                # Generate tailored textual descriptions
                prompt = (
                    f"Based on the following inputs, please provide a detailed description and comprehensive recommendation plan in a tabular format:\n\n"
                    f"Aesthetic Style: {aesthetic_style}\n"
                    f"Spatial Layout Preference: {spatial_layout}\n"
                    f"Architectural Style: {architectural_style}\n"
                    f"Structural Requirements: {structural_requirements}\n"
                    f"Environmental Considerations: {environmental_considerations}\n"
                    f"Cost Constraints: {cost_constraints}\n"
                    f"Load Requirements: {load_requirements}\n"
                    f"Type of Building: {building_type}\n"
                    f"Site Conditions: {site_conditions}\n\n"
                    f"Give tips and tricks also.\n"
                    f"Please use easy words and give in a tabular format.\n"
                )

                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=1000
                )

                generated_text = response.choices[0].text.strip()

                # Output generated text
                st.session_state.generated_text = generated_text
                st.subheader("Recommendation Plan")
                st.markdown(f"{generated_text}")  # Render generated text in a code block
                
                # Generate audio from text
                generate_audio(generated_text)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Check if there is generated text in session state
    if 'generated_text' in st.session_state:
        st.subheader("Recommendation Plan")
        st.markdown(st.session_state.generated_text)  # Render generated text in a code block

        # Add 'Read Aloud' button
        if st.button("Read Aloud", help="Click to listen to the generated recommendation plan"):
            play_audio()

if __name__ == "__main__":
    main()

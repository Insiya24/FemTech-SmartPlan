import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="YOUR API KEY HERE")
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)
chat_session = model.start_chat(
  history=[
  ]
)

# Green Material Checker Page
def green_material_page():
    st.title("Green Material Checker")
    st.write("This page will help you identify green materials and suggest alternatives.")

    materials_input = st.text_area("Enter materials (separated by comma or newline):")
    if st.button("Generate Descriptions"):
        # Split the input into separate material values
        materials_list = [material.strip() for material in materials_input.split(",") if material.strip()]

        # Generate tailored textual descriptions for each material
        for material in materials_list:
            prompt = f"Is {material} green building friendly? If not, then give me 3 alternative materials to be used instead of it in 3 points."
            response = chat_session.send_message(prompt)

            # Output materials used
            st.write(f"\nDescriptions for {material}:")
            st.write(response.text)

# Green Building Rating Page
def green_building_rating_page():
    st.title("Green Building Rating")
    
    # Define the questions
    questions = [
        "How was the site selected, and were environmental factors considered during site selection?",
        "What sustainable design features were incorporated into the building's architecture and layout?",
        "Are there renewable energy sources integrated into the building's energy systems?",
        "How is water usage managed, and are there systems for water conservation and reuse?",
        "Were sustainable materials used in construction, and how were they sourced?",
        "What measures were taken to minimize waste generation during construction and operation?",
        "How is indoor air quality maintained, and are there systems for natural ventilation?",
        "What strategies are in place for optimizing energy efficiency in heating, cooling, and lighting systems?",
        "Are there green transportation options or amenities provided for occupants?",
        "How does the building promote occupant health and well-being?",
        "What initiatives are in place for ongoing monitoring and improvement of environmental performance?",
        "Has the building received any green building certifications, and if so, which ones and at what level?",
        "How does the building contribute to reducing its carbon footprint and environmental impact?",
        "Are there measures for biodiversity conservation or habitat enhancement on the site?",
        "How does the building contribute to community engagement and awareness of sustainable practices?"
    ]

    # Initialize rating and scores
    rating = ""
    total_score = 0

    # Define score mapping for each answer
    score_mapping = {
        "Yes": 2,
        "No": 0,
        "Partially": 1,
        "Not Sure": 1
    }

    # Ask user for answers to questions
    for idx, question in enumerate(questions):
        answer = st.radio(f"Q{idx+1}: {question}", ["Yes", "No", "Partially", "Not Sure"])
        total_score += score_mapping[answer]

    # Calculate rating based on total score
    if total_score >= 25:
        rating = "Platinum"
    elif total_score >= 20:
        rating = "Gold"
    elif total_score >= 15:
        rating = "Silver"
    else:
        rating = "Bronze"

    # Display the rating
    if st.button("Generate Rating"):
        st.success(f"The green building rating is: {rating}")

# Energy Efficiency Optimization Page
def energy_efficiency_page():
    st.title("Energy Efficiency Optimization")

    # Inputs for building design
    st.header("Building Design Inputs")

    area = st.number_input("Enter the building area (in square meters):", min_value=10.0, step=10.0)
    floors = st.number_input("Enter the number of floors:", min_value=1, step=1)
    window_area = st.number_input("Enter the total window area (in square meters):", min_value=0.0, step=5.0)
    
    insulation_type = st.selectbox("Select the insulation type:", ["None", "Standard", "High Performance", "Eco-friendly"])
    lighting_type = st.selectbox("Select the lighting type:", ["Incandescent", "CFL", "LED", "Smart LED"])
    hvac_type = st.selectbox("Select the HVAC system type:", ["None", "Standard", "High Efficiency", "Geothermal"])
    roof_type = st.selectbox("Select the roof type:", ["Flat", "Sloped", "Green Roof", "Solar Roof"])
    wall_material = st.selectbox("Select the wall material:", ["Brick", "Concrete", "Wood", "Insulated Panels"])

    appliance_efficiency = st.selectbox("Select the appliance efficiency:", ["Standard", "Energy Star", "Smart Appliances"])

    # Energy consumption model (enhanced)
    def calculate_energy_consumption(area, floors, window_area, insulation, lighting, hvac, roof, wall, appliance):
        base_energy = area * floors * 100  # Arbitrary base value

        insulation_factor = 1.5 if insulation == "None" else 1.2 if insulation == "Standard" else 1.0 if insulation == "High Performance" else 0.9  # Eco-friendly
        lighting_factor = 1.5 if lighting == "Incandescent" else 1.2 if lighting == "CFL" else 1.0 if lighting == "LED" else 0.8  # Smart LED
        hvac_factor = 1.0 if hvac == "None" else 1.2 if hvac == "Standard" else 1.0 if hvac == "High Efficiency" else 0.8  # Geothermal
        roof_factor = 1.0 if roof == "Flat" else 1.1 if roof == "Sloped" else 0.9 if roof == "Green Roof" else 0.8  # Solar Roof
        wall_factor = 1.2 if wall == "Brick" else 1.3 if wall == "Concrete" else 1.0 if wall == "Wood" else 0.9  # Insulated Panels
        appliance_factor = 1.2 if appliance == "Standard" else 1.0 if appliance == "Energy Star" else 0.8  # Smart Appliances

        window_factor = 1 + (window_area / (area * floors))

        total_energy = base_energy * insulation_factor * lighting_factor * hvac_factor * roof_factor * wall_factor * appliance_factor * window_factor
        return total_energy

    if st.button("Calculate Energy Consumption"):
        energy_consumption = calculate_energy_consumption(area, floors, window_area, insulation_type, lighting_type, hvac_type, roof_type, wall_material, appliance_efficiency)
        st.subheader(f"Estimated Annual Energy Consumption: {energy_consumption:.2f} kWh")

        st.header("Recommendations")
        if insulation_type == "None":
            st.write("Consider using standard or high-performance insulation to reduce energy loss.")
        if lighting_type not in ["LED", "Smart LED"]:
            st.write("Switch to LED or Smart LED lighting to significantly reduce energy consumption.")
        if hvac_type not in ["High Efficiency", "Geothermal"]:
            st.write("Upgrade to a high-efficiency or geothermal HVAC system to save energy.")
        if roof_type != "Green Roof":
            st.write("Consider using a green roof to improve insulation and energy efficiency.")
        if wall_material != "Insulated Panels":
            st.write("Using insulated panels for walls can greatly reduce energy loss.")
        if appliance_efficiency != "Smart Appliances":
            st.write("Upgrade to smart appliances for better energy management and lower consumption.")
        if window_area > (area * floors * 0.2):
            st.write("Consider reducing window area or using energy-efficient windows to minimize energy loss.")

# Define the Streamlit pages
pages = {
    "Green Material Checker": green_material_page,
    "Green Building Rating": green_building_rating_page,
    "Energy Efficiency Optimization": energy_efficiency_page
}

# Create Streamlit app
st.title("Green Building Tools")

# Add a dropdown menu to select pages on the left sidebar
selected_page = st.sidebar.selectbox("Select Tool", list(pages.keys()))

# Run the selected page function
pages[selected_page]()
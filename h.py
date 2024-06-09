import os
import streamlit as st
import google.generativeai as genai

# Function to configure the API key
def configure_api():
    # Make sure to set the environment variable or use a hardcoded key (not recommended for production)
    api_key = os.getenv("GEMINI_API_KEY", "YOUR API KEY HERE")
    genai.configure(api_key=api_key)

# Function to create the model
def create_model():
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
    )
    return model

# Function to calculate cost estimation
def calculate_cost(area, construction_cost_per_sqft_inr, material_costs_inr, labor_costs_inr):
    total_cost_inr = (area * construction_cost_per_sqft_inr) + material_costs_inr + labor_costs_inr
    return total_cost_inr

# Streamlit UI
def main():
    st.title("Building Cost Estimation Tool (INR)")
    st.write("Welcome to the Building Cost Estimation Tool! Please input the required information.")

    # User inputs
    area = st.number_input("Area of the building (square feet)", min_value=1.0, step=1.0)
    construction_cost_per_sqft_inr = st.number_input("Construction Cost per Square Foot (INR)", min_value=1.0, step=0.1)
    material_costs_inr = st.number_input("Material Costs (INR)", min_value=0.0, step=1000.0)
    labor_costs_inr = st.number_input("Labor Costs (INR)", min_value=0.0, step=1000.0)

    # Calculate button
    if st.button("Calculate Total Cost (INR)"):
        if area and construction_cost_per_sqft_inr and material_costs_inr and labor_costs_inr:
            total_cost_inr = calculate_cost(area, construction_cost_per_sqft_inr, material_costs_inr, labor_costs_inr)
            st.success(f"The estimated total cost for the building is ₹{total_cost_inr:,.2f}")

            # Configure the API and create the model
            configure_api()
            model = create_model()
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(f"Calculate the cost for building with area {area} sq ft, construction cost {construction_cost_per_sqft_inr} INR per sq ft, material costs {material_costs_inr} INR, and labor costs {labor_costs_inr} INR.")
            st.write("AI Response:")
            st.write(response.text)

if __name__ == "__main__":
    main()

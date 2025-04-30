import os
from dotenv import load_dotenv
import streamlit as st
import requests
from streamlit_extras.let_it_rain import rain
import base64

st.set_page_config(layout="wide")  # Optional: Set layout

# Load and encode image to base64
def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("diamond_image1.jpg")

st.markdown(
    f"""
    <style>
    .watermark-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }}

    .watermark-container img {{
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        opacity: 0.08;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}

    input[type="number"] {{
        background-color: white !important;
        color: #2e2e2e !important;
    }}
    </style>

    <div class="watermark-container">
        <img src="data:image/jpeg;base64,{img_base64}" />
    </div>
    """,
    unsafe_allow_html=True
)
load_dotenv()

# Get the BASE_URL from the environment variables
base_url = os.getenv("BASE_URL", "http://localhost:8000")

# ---- Header Section ----
st.title("💎 Diamond Price Predictor")
st.markdown("""
    This application predicts the price of a diamond based on its characteristics such as carat, cut, color, clarity, and dimensions.
    """)

st.subheader("🛠️ Input Features")

col1, col2, col3 = st.columns(3)
with col1:
    carat = st.number_input("Carat", min_value=0.0, step=0.01)
with col2:
    depth = st.number_input("Depth", min_value=0.0, step=0.01)
with col3:
    table = st.number_input("Table", min_value=0.0, step=0.01)

col4, col5, col6 = st.columns(3)
with col4:
    x = st.number_input("Width (x)", min_value=0.0, step=0.01)
with col5:
    y = st.number_input("Length (y)", min_value=0.0, step=0.01)
with col6:
    z = st.number_input("Height (z)", min_value=0.0, step=0.01)

with st.expander("🛠️ Advanced Quality Parameters", expanded=True):
    cut_col, color_col, clarity_col = st.columns(3)
    with cut_col:
        cut = st.radio("Cut", ['Ideal', 'Premium', 'Very Good', 'Good', 'Fair'])
    with color_col:
        color = st.radio("Color", ['D', 'E', 'F', 'G', 'H', 'I', 'J'])
    with clarity_col:
        clarity = st.radio("Clarity", ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1'])


# Prediction button
st.subheader("🔮 Make a Prediction")
if st.button("Predict Price 💰"):
    # Prepare the data for API request
    input_data = {
        "carat": carat,
        "cut": cut,
        "color": color,
        "clarity": clarity,
        "depth": depth,
        "table": table,
        "x": x,
        "y": y,
        "z": z,
    }

    # Make the API request
    response = requests.post(f"{base_url}/api/predict", json=input_data)

    if response.status_code == 200:
        result = response.json()
        price = result['prediction']# st.write(f"The prediction is {prediction['label']} (Class: {prediction['prediction']})")
        st.success(f"💵 Estimated Price: **${price:.2f}**")
        rain(emoji="💎", font_size=30, falling_speed=5, animation_length=1)
    else:
        print(response)
        st.warning("⚠️ Unable to fetch prediction at this time. Please retry.")

# Run the Streamlit App
# streamlit run app.py

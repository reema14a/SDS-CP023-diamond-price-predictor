import os
from dotenv import load_dotenv
import streamlit as st
import requests
from streamlit_extras.let_it_rain import rain
import base64
import time

st.set_page_config(layout="wide")  # Optional: Set layout

load_dotenv()

# Get the BASE_URL from the environment variables
base_url = os.getenv("BASE_URL", "http://localhost:8000")

# Load and encode image to base64
def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Wake up the API with a /ping request
def wake_api(base_url):
    max_retries = int(os.getenv("API_WAKE_MAX_RETRIES", 3))   # default 3
    wait_time = int(os.getenv("API_WAKE_WAIT_TIME", 10))       # default 10 seconds

    ping_url = f"{base_url}/ping"
    start = time.time()

    with st.spinner("🚀 Warming things up — thank you for your patience!"):
        for i in range(max_retries):
            try:
                response = requests.get(ping_url, timeout=20)  # Increased timeout
                if response.status_code == 200:
                    elapsed = time.time() - start
                    print(f"⏱ API responded in {elapsed:.2f} seconds")
                    return True
                else:
                    print("Response status:", response.status_code)
                    print("Response body:", response.text)
                    time.sleep(wait_time)   
            except requests.exceptions.RequestException as e:
                print(f"Attempt {i+1}: {e}")
                time.sleep(wait_time)
                continue

    print(f"⏱ API timed out after {max_retries * (wait_time + 20)} seconds")
    elapsed = time.time() - start
    print(f"⏱Total time taken to respond in {elapsed:.2f} seconds")
    return False

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
    if not wake_api(base_url):
        st.warning("⚠️ Unable to reach prediction service. Please wait a few seconds and retry.")
    else:
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

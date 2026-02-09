import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Function to predict plant disease
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model.keras")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # Return index of max element

# Sidebar
st.sidebar.title("🌱 Plant Disease Detection System")
app_mode = st.sidebar.selectbox("Select Page", ["HOME",  "ABOUT", "DISEASE RECOGNITION"])

# Home Page
if app_mode == "HOME":
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 48px;
            color: #2E7D32; /* Dark Green */
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='main-header'>🌿 Plant Disease Detection System</div>", unsafe_allow_html=True)

    st.image("Detection.jpg", use_container_width=True, caption="Identify Plant Diseases Accurately")

   
# About Page
elif app_mode == "ABOUT":
    st.header("🌱 About the Plant Disease Detection System")
    st.markdown(
        """
        <style>
        .description {
            font-size: 18px;
            line-height: 1.8;
            color: #1B5E20; /* Deep Green */
            background-color: #C8E6C9; /* Light Green Background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .highlight {
            color: #D32F2F; /* Red for emphasis */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='description'>
        This application leverages cutting-edge <span class='highlight'>Deep Learning</span> technology to identify plant diseases 
        with exceptional accuracy. By analyzing images of plant leaves, the app provides quick and reliable predictions to help farmers 
        and agricultural professionals make informed decisions. 
        <br><br>
        <b>🌟 Features:</b>
        <ul>
            <li>Upload leaf images easily and get predictions instantly.</li>
            <li>Detect diseases across a wide variety of crops.</li>
            <li>Contribute to sustainable agriculture by enabling early intervention.</li>
        </ul>
        <br>
        <b>🌱 Why Use This App?</b>
        Early detection is crucial to saving crops, minimizing pesticide usage, and boosting yields. Empower your farming practices 
        with this AI-powered tool and take a step toward <span class='highlight'>sustainability</span>.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Prediction Page
elif app_mode == "DISEASE RECOGNITION":
    st.header("🔍 Disease Recognition")
    st.subheader("Upload a plant leaf image to detect diseases")

    # Restrict image type
    test_image = st.file_uploader("Choose an Image:", type=["jpg", "jpeg", "png"])

    if test_image:
        # Display uploaded image with size restrictions
        st.image(test_image, caption="Uploaded Image", width=200)

        if st.button("Predict"):
            with st.spinner("Analyzing..."):
                result_index = model_prediction(test_image)

            # Disease class names
            class_name = [
                'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                'Tomato___healthy'
            ]

            st.success(f"🌟 Model Prediction: **{class_name[result_index]}**")

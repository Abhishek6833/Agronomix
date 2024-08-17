import pickle
import numpy as np
import joblib
from PIL import Image
import tensorflow as tf
import pandas as pd


# Global variables
__location = None
__data_columns = None
__seeds_model = None
__disease_model = None
__expenditure_model = None
__le_village = None
__le_climatic = None
__le_crop = None
__seed_data = None  # Add global variable for the seed dataset


def find_suitable_seeds(district_name):
    if __seeds_model is None:
        raise Exception("Seeds model not loaded. Please call load_saved_artifacts() first.")

    # Ensure __seeds_model is a callable function
    if callable(__seeds_model):
        result = __seeds_model(district_name)
        return result
    else:
        raise Exception("__seeds_model is not callable")


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.
    return img_array


def predict_disease(image_path):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = __disease_model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]

    class_names = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Blueberry___healthy',
        'Cherry_(including_sour)___Powdery_mildew',
        'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight',
        'Corn_(maize)___healthy',
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)',
        'Peach___Bacterial_spot',
        'Peach___healthy',
        'Pepper,_bell___Bacterial_spot',
        'Pepper,_bell___healthy',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        'Raspberry___healthy',
        'Soybean___healthy',
        'Squash___Powdery_mildew',
        'Strawberry___Leaf_scorch',
        'Strawberry___healthy',
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy'
    ]

    return class_names[predicted_class_index]


def predict_expenditure(village, year, climatic_condition, crop_type):
    village_encoded = __le_village.transform([village])[0]
    climatic_encoded = __le_climatic.transform([climatic_condition])[0]
    crop_encoded = __le_crop.transform([crop_type])[0]

    features = np.array([[village_encoded, year, climatic_encoded, crop_encoded]])
    predicted_expenditure = __expenditure_model.predict(features)[0]

    return predicted_expenditure


def get_details(district, taluk):
    if __seed_data is None:
        raise Exception("Seed dataset not loaded. Please call load_saved_artifacts() first.")

    result = __seed_data[(__seed_data['District'].str.lower() == district.lower()) &
                         (__seed_data['Taluk'].str.lower() == taluk.lower())]

    if result.empty:
        return "No data found for the given district and taluk."
    else:
        return result.to_dict(orient='records')[0]  # Convert result to dictionary


def load_saved_artifacts():
    print("Loading saved artifacts...")

    global __seeds_model
    with open("./artifact/seed_dataset.pkl", 'rb') as f:
        __seeds_model = pickle.load(f)

    global __disease_model
    __disease_model = tf.keras.models.load_model("./artifact/plant_disease_prediction_model.h5")

    global __expenditure_model, __le_village, __le_climatic, __le_crop
    __expenditure_model = joblib.load('./artifact/expenditure_model.pkl')
    __le_village = joblib.load('./artifact/le_village.pkl')
    __le_climatic = joblib.load('./artifact/le_climatic.pkl')
    __le_crop = joblib.load('./artifact/le_crop.pkl')

    global __seed_data
    with open('./artifact/seed_dataset.pkl', 'rb') as f:
        __seed_data = pickle.load(f)

    print("Loading saved artifacts... done")


# Test the functionality
if __name__ == "__main__":
    load_saved_artifacts()

    # Test find_suitable_seeds
    # seeds = find_suitable_seeds('Coimbatore')
    # print(f"Suitable seeds: {seeds}")

    # Test predict_disease
    disease_prediction = predict_disease('./artifact/test_apple_black_rot.JPG')  # Provide a valid image path
    print(f"Disease prediction: {disease_prediction}")

    # Test predict_expenditure
    expenditure = predict_expenditure('Thiruparankundram', 2022, 'Tropical, Rainy', 'Paddy')
    print(f"Predicted expenditure: {expenditure}")

    # Test get_details
    details = get_details('Tenkasi', 'Courtallam')
    print(f"Details: {details}")

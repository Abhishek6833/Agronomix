from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import util

app = Flask(__name__)

# Route for predicting disease from leaf image
@app.route('/predict_disease', methods=['POST'])

def predict_disease():
    if 'leaf_image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['leaf_image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('./uploads', filename)
        file.save(file_path)

        # Check if the file was actually saved
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found after upload'})

        # Predict disease
        result = util.predict_disease(file_path)

        # Clean up the uploaded file
        os.remove(file_path)

        response = jsonify({
            'predicted_disease': result
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# Route for predicting expenditure based on inputs
@app.route('/predict_expenditure', methods=['POST'])
def predict_expenditure():
    # Extract form data
    village = request.form.get('village')
    year = request.form.get('year')
    climatic_condition = request.form.get('climatic_condition')
    crop_type = request.form.get('crop_type')

    # Validate form data
    if not village or not year or not climatic_condition or not crop_type:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Year must be a valid number'}), 400

    # Call util function to predict expenditure
    expenditure = util.predict_expenditure(village, year, climatic_condition, crop_type)

    # Return predicted expenditure in JSON response
    response = jsonify({
        'predicted_expenditure': expenditure
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route for fetching details based on district and taluk
@app.route('/get_details', methods=['POST'])
def get_details():
    # Extract form data
    district = request.form.get('district')
    taluk = request.form.get('taluk')

    # Validate form data
    if not district or not taluk:
        return jsonify({'error': 'Missing required fields'}), 400

    # Call util function to get details for district and taluk
    details = util.get_details(district, taluk)

    # Return details in JSON response
    response = jsonify({
        'details': details
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server...")
    util.load_saved_artifacts()  # Load any necessary models or files
    app.run(debug=True)

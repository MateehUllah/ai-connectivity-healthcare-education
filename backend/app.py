from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS
from utils.reverse_encode import get_worldbank_data, get_country_from_coordinates_google
from utils.recommendations import generate_education_recommendations,generate_healthcare_recommendations

app = Flask(__name__)
CORS(app)


education_model = joblib.load('models/education_connectivity_model.pkl')
healthcare_model = joblib.load('models/healthcare_connectivity_model.pkl')
scaler = joblib.load('models/scaler_with_clustering.pkl')
scaler_education=joblib.load('models/scaler.pkl')
kmeans = joblib.load('models/kmeans_with_clustering.pkl')

file_path = 'datasets/healthcare-connectivity-dataset.csv'
data = pd.read_csv(file_path)

data = data.dropna(subset=['Latitude', 'Longitude'])

facility_owner_categories = data['Facility_Owner'].astype('category').cat.categories
facility_type_categories = data['Renamed_Facility_Type'].astype('category').cat.categories

facility_owner_mapping = {category: code for code, category in enumerate(facility_owner_categories)}
facility_type_mapping = {category: code for code, category in enumerate(facility_type_categories)}

@app.route('/predict/healthcare', methods=['POST'])
def predict_healthcare():
    """
    Predict Healthcare Demand Score given facility details and coordinates.

    This endpoint takes a JSON payload with Latitude, Longitude, Facility_Owner, 
    and Renamed_Facility_Type, and returns a predicted Healthcare Demand Score.

    Args:
        Latitude (float): The latitude of the facility location.
        Longitude (float): The longitude of the facility location.
        Facility_Owner (str): The owner of the facility.
        Renamed_Facility_Type (str): The type of the facility.

    Returns:
        A JSON response with the predicted Healthcare Demand Score.

    Raises:
        400: If the input is invalid, missing, or contains invalid values.
        500: If there is an unexpected error during prediction.
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided.'}), 400

        required_fields = ['Latitude', 'Longitude', 'facilityType', 'facilityOwnerType']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        try:
            data['Facility_Owner_Encoded'] = facility_owner_mapping[data['facilityOwnerType']]
            data['Facility_Type_Encoded'] = facility_type_mapping[data['facilityType']]
        except KeyError as e:
            return jsonify({'error': f'Invalid value for {str(e)}. Check your input data.'}), 400

        latitude = data['Latitude']
        longitude = data['Longitude']
        facility_type_encoded = data['Facility_Type_Encoded']
        facility_owner_encoded = data['Facility_Owner_Encoded']

        scaled_coords = scaler.transform([[latitude, longitude]])
        latitude_scaled, longitude_scaled = scaled_coords[0]

        cluster = kmeans.predict([[latitude_scaled, longitude_scaled]])[0]
        interaction_term = latitude_scaled * longitude_scaled

        input_features = pd.DataFrame([{
            'Latitude_Scaled': latitude_scaled,
            'Longitude_Scaled': longitude_scaled,
            'Facility_Type_Encoded': facility_type_encoded,
            'Facility_Owner_Encoded': facility_owner_encoded,
            'Cluster': cluster,
            'Interaction_Term': interaction_term
        }])

        demand_score = healthcare_model.predict(input_features)[0]        

        recommendations = generate_healthcare_recommendations(data, demand_score)

        return jsonify({
            'Demand Score': demand_score,
            'Recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict/education', methods=['POST'])
def predict_education():
    """
    Predict Education Demand Score given a latitude and longitude.

    This endpoint takes a JSON payload with Latitude and Longitude and returns a predicted Education Demand Score.

    Args:
        Latitude (float): The latitude of the location.
        Longitude (float): The longitude of the location.

    Returns:
        A JSON response with the predicted Education Demand Score.

    Raises:
        400: If the input is invalid or missing.
        500: If there is an unexpected error.
    """
    try:
        data = request.json
        if not data or 'Latitude' not in data or 'Longitude' not in data:
            return jsonify({'error': 'Missing Latitude or Longitude in the input.'}), 400

        latitude = data['Latitude']
        longitude = data['Longitude']
        country_code = get_country_from_coordinates_google(latitude, longitude)

        feature_data = get_worldbank_data(country_code)
        feature_data['Latitude '] = latitude 
        feature_data['Longitude'] = longitude

        features = [
            "Latitude ", "Longitude",
            "OOSR_Primary_Age_Male", "OOSR_Primary_Age_Female",
            "Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female",
            "Gross_Primary_Education_Enrollment", "Gross_Tertiary_Education_Enrollment",
            "Birth_Rate", "Unemployment_Rate"
        ]

        input_df = pd.DataFrame([feature_data], columns=features) 

        scaled_features = scaler_education.transform(input_df)

        prediction = education_model.predict(scaled_features)

        demand_score = prediction[0]

        recommendations = generate_education_recommendations(feature_data, demand_score)

        return jsonify({
            'Demand Score': demand_score,
            'Recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

education_model = joblib.load('models/education_connectivity_model.pkl')
healthcare_model = joblib.load('models/healthcare_connectivity_model.pkl')
scaler = joblib.load('models/scaler.pkl')  

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict connectivity demand for education or healthcare.
    """
    try:
        data = request.json
        service_type = data.get('service_type') 
        features = ['Latitude', 'Longitude', 'Facility_Type_Encoded', 'Facility_Owner_Encoded']

        if service_type not in ['education', 'healthcare']:
            return jsonify({'error': 'Invalid service type. Use "education" or "healthcare".'}), 400

        input_data = pd.DataFrame([data])

        input_data[['Latitude', 'Longitude']] = scaler.transform(input_data[['Latitude', 'Longitude']])

        if service_type == 'education':
            prediction = education_model.predict(input_data[features])
        elif service_type == 'healthcare':
            prediction = healthcare_model.predict(input_data[features])

        return jsonify({'predicted_demand': prediction.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_dataset():
    """
    Upload a dataset for retraining or analysis.
    """
    try:
        uploaded_file = request.files['file']
        service_type = request.form.get('service_type')  

        # Validate inputs
        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400
        if service_type not in ['education', 'healthcare']:
            return jsonify({'error': 'Invalid service type. Use "education" or "healthcare".'}), 400

        # Save uploaded file
        file_path = f'datasets/{service_type}_uploaded.csv'
        uploaded_file.save(file_path)

        return jsonify({'status': f'Dataset uploaded successfully for {service_type}', 'file_path': file_path})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/retrain', methods=['POST'])
def retrain():
    """
    Retrain a specific model using a new dataset.
    """
    try:
        # Parse JSON input
        data = request.json
        service_type = data.get('service_type')  # 'education' or 'healthcare'
        dataset_path = data.get('dataset_path')  # Path to new dataset

        # Validate inputs
        if service_type not in ['education', 'healthcare']:
            return jsonify({'error': 'Invalid service type. Use "education" or "healthcare".'}), 400

        # Load dataset
        new_data = pd.read_csv(dataset_path)
        features = ['Latitude', 'Longitude', 'Facility_Type_Encoded', 'Facility_Owner_Encoded']
        target = 'Demand_Score'

        X = new_data[features]
        y = new_data[target]

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        model_path = f'models/{service_type}_connectivity_model_updated.pkl'
        joblib.dump(model, model_path)

        return jsonify({'status': f'Model retrained successfully for {service_type}', 'model_path': model_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

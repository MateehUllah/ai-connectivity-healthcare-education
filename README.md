### **Enhancing Infrastructure and Accessibility**

---

## **Project Overview**
This project provides a Flask API for predicting connectivity demand in the **education** and **healthcare** sectors. The models use specific features to generate predictions based on geographic and demographic data, as well as dynamically calculated connectivity scores.

### **Features**
- Predict connectivity demand for:
  - **Education**: Based on enrollment rates, out-of-school rates, and literacy rates.
  - **Healthcare**: Based on hospital bed availability, population density, and facility types.
- Generate dynamic **connectivity scores** for each prediction.
- Provide actionable recommendations for improving connectivity.

---

## **Dataset Sources**
- **Healthcare Dataset**:
  - Taken from **John Snow Labs**.
  - **Sub-Saharan Public Hospitals Database**:
    - This dataset provides a geocoded inventory of public hospitals across 48 countries and islands of sub-Saharan Africa from 100 different sources.
- **Education Dataset**:
  - Taken from **World Bank**.
  - Contains global education statistics including enrollment rates, literacy rates, and education accessibility data.

---

## **Directory Structure**
```
project-root/
│
├── backend/
│   ├── datasets/                # Datasets directory
│   │   ├── education-connectivity-dataset.csv
│   │   ├── healthcare-connectivity-dataset.csv
│   ├── models/                  # Trained models
│   │   ├── education_connectivity_model.pkl
│   │   ├── healthcare_connectivity_model.pkl
│   │   ├── kmeans_with_clustering.pkl
│   │   ├── scaler_with_clustering.pkl
│   │   └── scaler.pkl
│   ├── notebooks/               # Jupyter notebooks for training
│   │   ├── education_connectivity_notebook.ipynb
│   │   └── healthcare_connectivity_notebook.ipynb
│   ├── utils/                   # Utility scripts
│   │   ├── __init__.py
│   │   ├── recommendations.py
│   │   └── reverse_encode.py
│   ├── app.py                   # Main Flask application
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   ├── .env.example             # Example environment variables
│
├── frontend/                    # React frontend
│   ├── public/                  # Static assets
│   ├── src/                     # Source code
│   │   ├── components/      # React components
│   │   │   ├── MapConnectivity/
│   │   │   │   ├── CustomDropdown/
│   │   │   │   │   ├── CustomDropdown.jsx
│   │   │   │   ├── HealthcareForm/
│   │   │   │   │   ├── HealthcareForm.jsx
│   │   │   │   ├── LocationInputs/
│   │   │   │   │   ├── LocationInputs.jsx
│   │   │   │   ├── Tabs/
│   │   │   │   │   ├── Tabs.jsx
│   │   │   ├── MapConnectivity.jsx
│   │   ├── constants/        # Constants
│   │   │   ├── healthcareOptions.jsx
│   │   │   ├── mapSettings.jsx
│   │   ├── hooks/            # Custom hooks
│   │   │   ├── useClickOutside.jsx
│   │   ├── styles/           # Styling
│   │   │   ├── index.css
│   │   ├── utils/            # Utility functions
│   │   │   ├── api.js
│   │   ├── App.jsx           # Main React app
│   │   ├── main.jsx          # Entry point
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite configuration
│   ├── .env                     # Environment variables
│   ├── .env.example             # Example environment variables
│
├── .gitignore                   # Ignore unnecessary files
├── README.md                    # Project documentation
├── Dockerfile                   # Docker configuration
└── docker-compose.yml           # Compose file for multi-container setup
```

---

## **API Endpoints**

### **1. `/predict/healthcare`**
Predict connectivity demand for **healthcare** facilities.

- **Method**: `POST`
- **Request**:
  ```json
  {
    "Latitude": 34.0522,
    "Longitude": -118.2437,
    "facilityType": "Hospital",
    "facilityOwnerType": "Private"
  }
  ```
- **Response**:
  ```json
  {
    "Connectivity Score": 0.83,
    "Status": "good",
    "Recommendations": "Add more healthcare facilities. Improve transportation networks. Increase public health awareness campaigns."
  }
  ```

---

### **2. `/predict/education`**
Predict connectivity demand for **education** facilities.

- **Method**: `POST`
- **Request**:
  ```json
  {
    "Latitude": 40.7128,
    "Longitude": -74.0060
  }
  ```
- **Response**:
  ```json
  {
    "Connectivity Score": 0.85,
    "Status": "needs improvement",
    "Recommendations": "Increase access to primary education. Implement community outreach programs. Enhance teacher training initiatives."
  }
  ```

---

## **Setup and Installation**

### **1. Backend (Flask API)**
#### **Requirements**
- Python 3.13+
- Pip (Python package manager)

#### **Installation Steps**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-root/backend
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
5. Add the required API keys in the `.env` file:
   ```
   GOOGLE_API_KEY=
   HUGGINGFACEHUB_API_TOKEN=
   ```
6. Run the Flask API:
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

### **2. Frontend (React App)**
#### **Installation Steps**
1. Navigate to the `frontend/` directory:
   ```bash
   cd project-root/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Add the required API keys in the `.env` file:
   ```
   VITE_GOOGLE_API_KEY=
   VITE_API_BASE_URL=
   ```
5. Start the development server:
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000`.

---

## **How to Use**
1. **Make Predictions**:
   - Send a POST request to `/predict/healthcare` or `/predict/education` with appropriate input data.

---

## **Contributing**
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

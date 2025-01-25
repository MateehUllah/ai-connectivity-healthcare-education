import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_country_from_coordinates_google(latitude, longitude):
    """
    Takes a latitude and longitude as input and returns the ISO 2-letter country code associated with those coordinates using the Google Maps Geocoding API.

    :param latitude: The latitude coordinate
    :param longitude: The longitude coordinate
    :return: A string representing the ISO 2-letter country code
    """
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={google_api_key}"
    response = requests.get(url)
    data = response.json()
    for component in data['results'][0]['address_components']:
        if 'country' in component['types']:
            return component['short_name'].upper()

def get_worldbank_data(country_code):
    """
    Uses World Bank API to get the values of the following indicators:
    
    - OOSR_Primary_Age_Male
    - OOSR_Primary_Age_Female
    - Youth_15_24_Literacy_Rate_Male
    - Youth_15_24_Literacy_Rate_Female
    - Gross_Primary_Education_Enrollment
    - Gross_Tertiary_Education_Enrollment
    - Birth_Rate
    - Unemployment_Rate
    
    for the given country code.
    
    Returns a dictionary with the indicator names as keys and the values as values.
    """
    indicators = {
        "OOSR_Primary_Age_Male": {"code": "SE.PRM.UNER.MA"},
        "OOSR_Primary_Age_Female": {"code": "SE.PRM.UNER.FE"},
        "Youth_15_24_Literacy_Rate_Male": {"code": "SE.ADT.1524.LT.MA.ZS"},
        "Youth_15_24_Literacy_Rate_Female": {"code": "SE.ADT.1524.LT.FE.ZS"},
        "Gross_Primary_Education_Enrollment": {"code": "SE.PRM.ENRR"},
        "Gross_Tertiary_Education_Enrollment": {"code": "SE.TER.ENRR"},
        "Birth_Rate": {"code": "SP.DYN.CBRT.IN"},
        "Unemployment_Rate": {"code": "SL.UEM.TOTL.ZS"}
    }
    
    data_results = {}
    
    for key, config in indicators.items():
        code = config["code"]
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{code}?format=json"
        response = requests.get(url)
        data = response.json()
        
        value = None
        
        if data and len(data) > 1 and data[1]:
            valid_entries = [
                entry for entry in data[1] 
                if entry.get("value") is not None
            ]
            valid_entries_sorted = sorted(
                valid_entries, 
                key=lambda x: int(x["date"]), 
                reverse=True
            )
            
            if valid_entries_sorted:
                value = valid_entries_sorted[0]["value"]
        
        data_results[key] = value
    
    return data_results


def get_data_from_coordinates(latitude, longitude):
    """
    Given a latitude and longitude, returns a JSON object with the country name,
    country code and a dictionary of values for the specified indicators.
    
    Parameters
    ----------
    latitude : float
        The latitude of the location
    longitude : float
        The longitude of the location
    
    Returns
    -------
    A JSON object with the country name, country code and the indicators data.
    If an error occurs, returns a JSON object with an "error" key.
    """
    try:
        country, country_code = get_country_from_coordinates_google(latitude, longitude)
        print("I am here in get_data_from_coordinates")
        world_bank_data = get_worldbank_data(country_code)

        result = {
            "Country": country,
            "Country_Code": country_code,
            "Data": world_bank_data
        }
        return result
    except Exception as e:
        return {"error": str(e)}
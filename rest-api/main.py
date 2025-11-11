import requests
import json

# API endpoint
url = "http://localhost:8000/predict"

# Sample house data for prediction
sample_data = {
    "MedInc": 4.8036,
    "HouseAge": 4.0,
    "AveRooms": 3.9246575342465753,
    "AveBedrms": 1.0359589041095891,
    "Population": 1050.0,
    "AveOccup": 1.797945205479452,
    "Latitude": 37.39,
    "Longitude": -122.08
    # Removed RoomsPerHousehold to trigger error
}

try:
    # Send a POST request to the API with the sample data as JSON
    response = requests.post(url, json=sample_data)

    # Check if response.status_code == 200
    if response.status_code == 200:
        # Parse the JSON response from the server
        result = response.json()
        # Convert predicted value from units of 100,000s to actual dollar amount
        predicted_value = result['prediction'] * 100000
        # Print the predicted house value in a readable format
        print(f"Predicted house value: ${predicted_value:,.2f}")
        # Print the status returned by the API
        print(f"Status: {result['status']}")
    else:
        # Print error status code and response text
        print(f"Error: Status code {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
except Exception as e:
    print(f"Error: {e}")

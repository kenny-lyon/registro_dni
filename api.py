import requests

BASE_API_URL = 'https://dniruc.apisperu.com/api/v1/dni/'
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'

def get_dni_data(dni):
    url = f"{BASE_API_URL}{dni}?token={API_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        if response_json['success']:
            return {
                "dni": response_json['dni'],
                "nombres": response_json['nombres'],
                "apellidoPaterno": response_json['apellidoPaterno'],
                "apellidoMaterno": response_json['apellidoMaterno']
            }
        else:
            return None
    else:
        return None

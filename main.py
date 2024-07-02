import os
import requests
import webbrowser
from flask import Flask, request
from dotenv import load_dotenv
from urllib.parse import urlencode
import threading
from config import Settings

load_dotenv()
settings = Settings()

class MercadoLibreAuth:

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, response_type: str, state: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.state = state
        self.authorization_code = None
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        self.app = Flask(__name__)
        self.code_received_event = threading.Event()
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route("/")
        def receive_code():
            if request.args.get('state') == self.state:
                self.authorization_code = request.args.get('code')
                if self.authorization_code:
                    print("Código de autorización recibido. Puedes cerrar esta ventana.")
                    self.code_received_event.set()
                    return "Autorización recibida. Puedes cerrar esta ventana.", 200
                else:
                    return "No se recibió el código de autorización.", 400
            else:
                return "Parámetro de estado inválido.", 400

    def start_flask_app(self):
        threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()

    def authorize(self):
        params = {
            "response_type": self.response_type,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": self.state
        }
        auth_url = f"{os.getenv('URL_AUTH')}?{urlencode(params)}"
        threading.Thread(target=lambda: webbrowser.open(auth_url)).start()
        print(f"Navegador abierto para autenticación en: {auth_url}")

    def exchange_code_for_token(self):
        url = os.getenv("TOKEN_URL")
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.authorization_code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.save_tokens()
            print("Token de acceso y token de actualización recibidos.")
        else:
            print(f"Error en el intercambio de código por token: {response.status_code} - {response.text}")

    def refresh_access_token(self):
        url = os.getenv("TOKEN_URL")
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.save_tokens()
            print("Access token renovado.")
        else:
            print(f"Error al renovar el token de acceso: {response.status_code} - {response.text}")

    def save_tokens(self):
        with open('.env', 'a') as env_file:
            env_file.write(f'\nACCESS_TOKEN={self.access_token}')
            env_file.write(f'\nREFRESH_TOKEN={self.refresh_token}')

# Ejemplo de uso
if __name__ == "__main__":
    ml_auth = MercadoLibreAuth(**settings.params_api)
    ml_auth.start_flask_app()
    ml_auth.authorize()
    
    # Esperar a que se reciba el código de autorización
    ml_auth.code_received_event.wait()

    # Continuar con el intercambio del código por un token
    ml_auth.exchange_code_for_token()

    # Renovar el token cuando sea necesario
    ml_auth.refresh_access_token()

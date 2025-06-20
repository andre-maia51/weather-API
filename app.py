import redis.exceptions
import requests
import redis
import json
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
URL_BASE = os.getenv("API_URL_BASE")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

if not API_KEY or not URL_BASE:
    raise ValueError("API_KEY e API_URL_BASE devem ser definidos no arquivo .env")

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    cache.ping()
    print("Conectado ao Redis com sucesso!")
except redis.exceptions.ConnectionError as err:
    print(f"Não foi possível conectar ao Redis: {err}")
    cache = None

@app.route("/weather/<city>")
def get_weather(city):
    cache_key = f"clima: {city.lower()}"

    if cache:
        cache_data = cache.get(cache_key)
        if cache_data:
            print(f"HIT: Retornando dados para '{city}' do cache.")
            return json.loads(cache_data)
    
    print(f"MISS: Buscando dados para '{city}' na API externa")
    complete_url = f"{URL_BASE}{city}?unitGroup=metric&key={API_KEY}&contentType=json"

    try:
        response = requests.get(complete_url)
        response.raise_for_status()

        data_weather = response.json()
        current_data = data_weather["currentConditions"]
        data_today = data_weather["days"][0]

        final_response = {
            "resolvedAddress": data_weather.get("resolvedAddress"),
            "temp": current_data.get("temp"),
            "feelsLike": current_data.get("feelslike"),
            "conditions": current_data.get("conditions"),
            "humidity": current_data.get("humidity"),
            "tempMin": data_today.get("tempmin"),
            "tempMax": data_today.get("tempmax"),
            "sunrise": data_today.get("sunrise"),
            "sunset": data_today.get("sunset")
        }

        if cache:
            cache.setex(cache_key, 300, json.dumps(final_response))

        return final_response
    
    except requests.exceptions.HTTPError as err:
        return f"Erro ao buscar dados da cidade: {city}. Erro: {err}", err.response.status_code
    except Exception as err:
        return f"Ocorreu um erro inesperado: {err}", 500

if __name__ == '__main__':
    app.run(debug=True)
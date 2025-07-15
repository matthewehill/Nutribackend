from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "188d8c8cf6594fb7a130484e55d3b5e2"

@app.route('/')
def home():
    return 'Flask API is live!'

@app.route('/search-recipes', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data.get('keyword', '')

    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": keyword,
        "number": 5,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

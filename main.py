from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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
    offset = int(data.get('offset', 0))
    number = int(data.get('number', 10))

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": keyword,
        "number": number,
        "offset": offset,
        "instructionsRequired": True,
        "addRecipeInformation": True,
        "fillIngredients": True,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        raw = response.json()
        raw_results = raw.get("results", [])
        total_results = raw.get("totalResults", 0)

        results = []
        for r in raw_results:
            results.append({
                "id": r.get("id"),
                "title": r.get("title"),
                "image": r.get("image"),
                "summary": r.get("summary"),
                "instructions": r.get("instructions"),  # Might be empty; fallback with new endpoint
                "readyInMinutes": r.get("readyInMinutes"),
                "servings": r.get("servings"),
                "extendedIngredients": [
                    {
                        "original": ing.get("original")
                    } for ing in r.get("extendedIngredients", [])
                ]
            })

        return jsonify({
            "results": results,
            "totalResults": total_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    recipe_id = data.get("id")

    if not recipe_id:
        return jsonify({"error": "Missing recipe ID"}), 400

    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": True,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

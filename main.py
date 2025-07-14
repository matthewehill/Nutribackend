from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask API is live!'

@app.route('/search-recipes', methods=['POST'])
def search():
    data = request.json
    keyword = data.get('keyword', '')
    return jsonify({"results": [f"{keyword} recipe 1", f"{keyword} recipe 2"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

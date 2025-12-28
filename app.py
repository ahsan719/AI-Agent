from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import agent after Flask app is created
from main import run_agent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        print(f"[INFO] Received query: {query}")
        result = run_agent(query)
        print(f"[INFO] Agent response: {result}")
        return jsonify(result)
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] {error_msg}")
        print(traceback.format_exc())
        return jsonify({"error": error_msg, "raw_response": "Server error occurred"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("[INFO] Starting AI Research Agent server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

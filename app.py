from flask import Flask, render_template, request, jsonify
from main import run_agent

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    result = run_agent(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

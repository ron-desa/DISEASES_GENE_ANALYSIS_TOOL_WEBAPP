from flask import Flask, render_template, request, jsonify
import csv


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')

    # Your search logic here
    # Read the data from the TSV file and search for the keyword

    # Sample response for demonstration
    results = [{"geneName": "Gene1", "diseaseName": "Disease1", "zScore": 1.5, "confidenceScore": 0.8, "url": "example.com"}]
    total_results = len(results)

    return jsonify({"results": results, "totalResults": total_results})

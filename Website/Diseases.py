from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Path to the TSV file
tsv_file_path = "/home/rounak/Desktop/human_disease_textmining_full.tsv"

# Read the TSV file into a pandas DataFrame
df = pd.read_csv(tsv_file_path, sep='\t')

@app.route('/')
def index():
    return render_template('/home/rounak/CODE/Website/TEST1.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    filtered_df = df[df['DOID:9643'] == keyword]  # Adjust column name as needed
    results = filtered_df.to_dict(orient='records')
    total_results = len(results)
    return jsonify({"results": results, "totalResults": total_results})

if __name__ == '__main__':
    app.run(debug=True)

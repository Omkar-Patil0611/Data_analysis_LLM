from flask import Flask, request, render_template, jsonify
import pandas as pd
from data_insights import generate_summary
from query_processor import process_query
from code_executor import run_generated_code
import os
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dataset = None  # Global variable to hold dataset

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global dataset
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if the file extension is allowed (CSV or Excel)
    extension = file.filename.rsplit('.', 1)[1].lower()
    allowed_extensions = ['csv', 'xlsx', 'xls']
    if extension not in allowed_extensions:
        return jsonify({"error": "Invalid file type. Only CSV and Excel files are allowed."}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        if extension == 'csv':
            dataset = pd.read_csv(filepath)
        else:
            dataset = pd.read_excel(filepath)
    except Exception as e:
        return jsonify({"error": f"Error processing file: {e}"}), 500

    data_summary = generate_summary(dataset)
    return jsonify({"message": "File uploaded successfully", "summary": data_summary})


@app.route('/insights', methods=['GET'])
def insights():
    global dataset
    if dataset is None:
        return jsonify({"error": "No dataset uploaded"}), 400

    insights = {
        "null_values": dataset.isnull().sum().to_dict(),
        "unique_values": {col: int(dataset[col].nunique()) for col in dataset.columns},
        "duplicate_records": int(dataset.duplicated().sum()),
        "descriptive_stats": dataset.describe().applymap(lambda x: float(x)).to_dict(),
        "numeric_summary": dataset.select_dtypes(include='number').describe().applymap(lambda x: float(x)).to_dict()
    }
    return jsonify(insights)

@app.route('/query', methods=['POST'])
def query_data():
    global dataset
    if dataset is None:
        return jsonify({"error": "No dataset uploaded"}), 400
    
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        # Generate code based on the user's query and dataset summary
        generated_code = process_query(query, generate_summary(dataset))
        # Execute the generated code (which may produce a Matplotlib plot)
        execution_results, execution_output = run_generated_code(generated_code, dataset)
        
        # Check for any Matplotlib figures and convert the last one to a Base64 string
        plot_image = None
        figs = [plt.figure(num) for num in plt.get_fignums()]
        if figs:
            fig = figs[-1]  # Use the most recent figure
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            plot_image = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
        
        response = {
            "generated_code": generated_code,
            "execution_output": execution_output,
            "plot_image": plot_image
        }
        if isinstance(execution_results, str):
            response["error"] = execution_results
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Execution error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

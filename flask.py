from flask import Flask, render_template, request
import pandas as pd
from data_insights import generate_summary
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            
            # Load dataset
            if uploaded_file.filename.endswith('.csv'):
                dataset = pd.read_csv(file_path)
            else:
                dataset = pd.read_excel(file_path, engine='openpyxl')
            
            # Generate data summary
            data_summary = generate_summary(dataset)
            
            # Convert DataFrame to HTML tables
            dataset_preview = dataset.head().to_html(classes='table table-striped', index=False)
            null_values = dataset.isnull().sum().to_frame('Null Count').to_html(classes='table table-striped')
            unique_values = pd.DataFrame({col: [dataset[col].nunique()] for col in dataset.columns}).to_html(classes='table table-striped')
            duplicate_count = dataset.duplicated().sum()
            
            return render_template('index.html', dataset_preview=dataset_preview, null_values=null_values, unique_values=unique_values, duplicate_count=duplicate_count)
    
    return render_template('index.html', dataset_preview=None)

if __name__ == '__main__':
    app.run(debug=True)
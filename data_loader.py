import pandas as pd

def load_dataset(uploaded_file):
    """Loads a dataset and formats date columns as 'Apr-24' instead of '2024-04-01'."""
    try:
        if uploaded_file.name.endswith('.csv'):
            dataset = pd.read_csv(uploaded_file, parse_dates=True)
        else:
            dataset = pd.read_excel(uploaded_file, engine='openpyxl', parse_dates=True)

        # Format datetime columns as 'Apr-24'
        for col in dataset.select_dtypes(include=['datetime']):
            dataset[col] = dataset[col].dt.strftime('%b-%y')

        return dataset

    except Exception as e:
        raise RuntimeError(f"Error processing file: {e}")

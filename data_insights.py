import pandas as pd
 
def generate_summary(df):
    # General information
    total_rows = len(df)
    data_types = {col: str(dtype)[:3] for col, dtype in df.dtypes.items()}  # Shorten dtype names
    missing_values = df.isnull().sum().to_dict()
    
    # Summaries
    unique_values = {}
    numeric_summary = {}

    for column in df.columns:
        if df[column].dtype == 'object' or df[column].dtype.name == 'category':
            unique_counts = df[column].nunique()
            top_values = df[column].value_counts().index[:5].tolist()  # Top 5 unique values
            unique_values[column] = {"unique_count": unique_counts, "top_values": top_values}
        elif pd.api.types.is_numeric_dtype(df[column]):
            numeric_summary[column] = {
                "mean": round(df[column].mean(), 2),
                "median": round(df[column].median(), 2),
                "min": round(df[column].min(), 2),
                "max": round(df[column].max(), 2),
            }
    
    # Compact summary
    summary = {
        "Total Rows": total_rows,
        "Data Types": data_types,
        "Missing Values": missing_values,
        "Unique Values (Categorical)": unique_values,
        "Numeric Summary": numeric_summary
    }
    
    return summary



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

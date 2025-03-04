import pandas as pd

def generate_summary(df):
    # Get general information
    columns = list(df.columns)
    data_types = df.dtypes.to_dict()
    total_rows = len(df)
    memory_usage = df.memory_usage(deep=True).sum()
    
    # Initialize summaries
    missing_values = df.isnull().sum().to_dict()
    unique_values = {}
    numeric_summary = {}

    for column in df.columns:
        if df[column].dtype == 'object' or df[column].dtype.name == 'category':
            # Unique values for categorical columns
            unique_values[column] = {
                "unique_count": df[column].nunique(),
                "unique_values": df[column].unique().tolist()
            }
        elif 'datetime' in str(df[column].dtype):
            # Infer date format
            date_sample = df[column].dropna().iloc[0] if not df[column].isnull().all() else None
            if date_sample:
                inferred_format = pd.to_datetime([date_sample]).strftime('%Y-%m-%d')[0]
                unique_values[column] = f"Date format: {inferred_format}"
            else:
                unique_values[column] = "No valid dates"
        elif pd.api.types.is_numeric_dtype(df[column]):
            # Basic statistics for numeric columns
            numeric_summary[column] = {
                "mean": df[column].mean(),
                "median": df[column].median(),
                "min": df[column].min(),
                "max": df[column].max()
            }

    # Create summary text
    summary = (
        f"Total Rows: {total_rows}\n"
        f"Columns: {columns}\n"
        f"Data Types: {data_types}\n"
        f"Memory Usage: {memory_usage / 1024:.2f} KB\n\n"
        f"Missing Values:\n{missing_values}\n\n"
        f"Unique Values for Categorical/Date Columns:\n{unique_values}\n\n"
        f"Numeric Column Summary:\n{numeric_summary}"
    )
    
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

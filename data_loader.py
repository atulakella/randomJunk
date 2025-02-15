import pandas as pd
import os

def load_data(file_path):
    """
    Load data from a CSV or Excel file into a Pandas DataFrame.
    
    Parameters:
        file_path (str): Path to the data file.
    
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[-1].lower()
    
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")


def preprocess_data(df):
    """
    Perform basic data preprocessing, such as handling missing values and renaming columns.
    
    Parameters:
        df (pd.DataFrame): Input data.
    
    Returns:
        pd.DataFrame: Preprocessed data.
    """
    df = df.dropna()  # Remove missing values
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')  # Standardize column names
    return df

if __name__ == "__main__":
    file_path = "data/sample_data.csv"  # Example file path
    try:
        data = load_data(file_path)
        clean_data = preprocess_data(data)
        print("Data Loaded and Preprocessed Successfully!")
        print(clean_data.head())
    except Exception as e:
        print(f"Error: {e}")

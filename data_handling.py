import pandas as pd

def load_data(filepath):
    # Load Excel data into a pandas DataFrame
    df = pd.read_excel(filepath, sheet_name='Training')
    
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set 'Date' as the index of the DataFrame
    df.set_index('Date', inplace=True)
    
    return df

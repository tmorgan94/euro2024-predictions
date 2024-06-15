import pandas as pd

def load_data():
    # Define the paths to your CSV files
    csv_files = {
        'results': 'data/results.csv',
        
        'md1_responses': 'data/md1_responses.csv',
        'md2_responses': 'data/md2_responses.csv'
        #'md3_responses': 'data/md3_responses.csv'
    }
    
    # Read the CSV files into DataFrames
    data_frames = {name: pd.read_csv(path) for name, path in csv_files.items()}
    
    return data_frames

load_data
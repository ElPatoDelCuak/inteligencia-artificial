import pandas as pd
import os

def open_file(directory_name: str, file: str):
    
    path = os.path.join(os.path.dirname(__file__), directory_name, file)
    if not os.path.exists(path):
        print("Error: no file found")
        return 0

    return pd.read_csv(path)

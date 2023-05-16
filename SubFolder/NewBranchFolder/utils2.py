import boto3 
import traceback
import botocore

def read_config_val(file_path: str, key: str) -> str:
    
    from json import load
     
    with open(file_path) as f:
        data = load(f)
    
    return data[key]
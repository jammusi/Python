import boto3 
import traceback
import botocore
import os 
def start():

    working_dir = os.getcwd()    
    print(f"Strt: {working_dir}")
    
    # from SubFolder.utils import read_config_val
    from utils import read_config_val

    file_path = "./config.json"
    file_path = "./SubFolder/config.json"

    val = read_config_val(file_path, "v1")    

    print(val)


if __name__ == '__main__':
   
    start()

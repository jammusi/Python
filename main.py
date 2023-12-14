from datetime import datetime
from awsApp import upload
from awsApp import download
from awsApp import delete as delete_aws_file
import awsApp
import pandas as pd
from datetime import timezone, timedelta


import traceback
import os


def delete_aws_file():
    bucket_name = "ojbucket-2"
    aws_folder = "CandlesRepositoryCSVs/BTCUSD"
    file_name = "Log5.txt"

    result = awsApp.delete(bucket_name,aws_folder, file_name)
    print(f'awsApp.delete result: {result}')



def _test1(parameter: int):
    print(f"test1 para1: {parameter}" )

    parameter = parameter * 2

    print(f"test1 para2: {parameter}" )

def main(args):

    delete_aws_file()
    return



if __name__ == '__main__':

    main(None)


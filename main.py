from datetime import datetime
from awsApp import upload
from awsApp import download
import pandas as pd
from datetime import timezone, timedelta
from CandleRecord import CandleDataRecord
from CandleRecord import DateTimeInterval
from enum import Enum

import traceback
import os

class Enum1(Enum):
    val1 = 1,
    val2 = 1,
    val3 = 3,
    val4 = 4,

def test_panda():
    file_name = "data.csv"
    file = pd.read_csv(file_name)


    #read last line
    df=pd.DataFrame(file.iloc[-1:,:].values)
    row = df.loc[0] #single row
    res = row.loc[0] # time first column

    last_ts = file.iloc[-1,0]
    last_ts_2 = file.iloc[-2,0]
    if res == last_ts:
        print("YESSSSSSSSS")
    else:
        print("NOOOOOOOOOOOOOO")

    minus_last = file.iloc[:-1]
    last_ts_minus = minus_last.iloc[-1,0]

    print(f"last: {last_ts}")
    print(f"last-2: {last_ts_2}")
    print(f"last_minus: {last_ts_minus}")
def _test_enum():
    e1 = Enum1.val1
    print(e1.value == Enum1.val2.value) 

    print("enum1 values")

    for e in Enum1:
        print(e)
        
def main(args):

    _test_enum()
    # test_panda()
    return


if __name__ == '__main__':

    main(None)


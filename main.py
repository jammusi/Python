from datetime import datetime
from awsApp import upload
from awsApp import download
import pandas as pd
from datetime import timezone, timedelta
from CandleRecord import CandleDataRecord
# from CandleRecord import DateTimeInterval
from enum import Enum

import traceback
import os

class BaseClass:
    def __init__(self) -> None:
        self.exchange: Enum1 = None
        pass

    def do_somthing(self):
        print(f"my Exchange: {self.exchange}")
        pass

class ChildClass(BaseClass):
    def __init__(self) -> None:
        self.exchange = Enum1.val1
        pass

    # def do_somthing(self):
    #     print(f"my Exchange: {self.exchange}")
    #     pass

class Enum1(Enum):
    val1 = 1,
    val2 = 1,
    val3 = 3,
    val4 = 7,
    addedByBranch = 7,


class DateTimeinterval:
    def __init__(self, name: str, val: int) -> None:
        self.name = name
        self.value = val
        # self.file_name_str = file_name_str
    def __repr__(self) -> str:
        return f"{self.name}"
    
    def __eq__(self, __value: object) -> bool:

        if isinstance(__value, DateTimeinterval):
            return (self.value, self.name) == (__value.value, __value.name)
        else:
            return False
        
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



def test_dti():

    dt1 = DateTimeinterval("5m",5)
    dt2 = DateTimeinterval("5m",5)

    print (dt1 == dt2)
    print (3 == dt2)

def _test_enum():
    e1 = Enum1.val1
    print(e1.value == Enum1.val2.value) 

    print("enum1 values")

    for e in Enum1:
        print(e)

def _test_logger():
    from Logger import logger2

    num_on_lines = 1000
    num_on_char_in_line = 1024

    for i in range(num_on_lines):
        log_line = ",".join(str(i) for i in range(num_on_char_in_line))
        logger2.write_to_log(log_line)


def _run_in_another_thread():
    from time import sleep
    print(f"new thread started...")

    for i in range(5):
        print(f"count: {++i}")
        sleep(2)

def _test_thread():
    from threading import Thread

    thread = Thread(target=_run_in_another_thread)
    thread.start()
    print(f"_test_thread: after start child thread")


def main(args):

    #added in main to be margeed
    #     
    _test_thread()
    print(f"main out")

    return


    d1 = {
        "k1": {"min": 1,"str": "1m"},
        "k2": {"min": 5,"str": "5m"},
    }

    mins = [val["min"] for val in d1.values()]

    print(mins)
    return

    import time

    unix1 = time.time()

    da = datetime.now(tz=timezone.utc)
    unix2 = da.timestamp()
    
    print(unix1)
    print(unix2)


    dt = datetime.now(timezone.utc)
    
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    print(utc_timestamp)


    return
    _test_enum()
    # test_panda()
    return


if __name__ == '__main__':

    main(None)


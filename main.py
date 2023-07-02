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
        
def _map_df_row_to_candle(row, interval: DateTimeinterval) -> CandleDataRecord:
    ts = 12345678900
    ts1 = row.timestamp
    return CandleDataRecord(interval,ts,row.open,row.close,row.high, row.low, row.volume,row.trades)


def test_panda():
    file_name = "data.csv"
    # file_df = pd.read_csv(file_name, header=None,index_col=False)
    file_df = pd.read_csv(file_name)

    interval = DateTimeinterval("5m",5)
    candles = [_map_df_row_to_candle(row, interval) for row in file_df.itertuples()]

    return

    #read last line
    df=pd.DataFrame(file_df.iloc[-1:,:].values)
    row = df.loc[0] #single row
    res = row.loc[0] # time first column

    last_ts = file_df.iloc[-1,0]
    last_ts_2 = file_df.iloc[-2,0]
    if res == last_ts:
        print("YESSSSSSSSS")
    else:
        print("NOOOOOOOOOOOOOO")

    minus_last = file_df.iloc[:-1]
    last_ts_minus = minus_last.iloc[-1,0]

    print(f"last: {last_ts}")
    print(f"last-2: {last_ts_2}")
    print(f"last_minus: {last_ts_minus}")



def _is_candle_start_interval(candle: CandleDataRecord, interval: DateTimeinterval) -> bool:

    answer = False
    if interval.value == 10080:
        #week interval 

        candle_date = candle.get_date_time()

        answer = candle_date.weekday() == 6 \
                and candle_date.hour == 0 \
                and candle_date.minute == 0 \
                and candle_date.second == 0 
    else:    
        cur_can_sec = candle.time_stamp_sec
        target_interval_sec = interval.value * 60 

        # check reminder
        answer = cur_can_sec % target_interval_sec == 0
        
    return answer

def _test_converter_week():
    
    candle_date = datetime(2017,1,1,0,0,0, tzinfo=timezone.utc) #sunday 00:00
    # candle_date = datetime(1970,1,1,0,0,0, tzinfo=timezone.utc) #sunday 00:00

    can_interval = DateTimeinterval("1m",1)
    candle_ts = candle_date.timestamp()
    candle = CandleDataRecord(can_interval, candle_ts,0,0,0,0,0,0)

    target_interval = DateTimeinterval("1w",10080)

    more = True

    while more:
        
        res = _is_candle_start_interval(candle,target_interval)
        candle_d = candle.get_date_time()
        print (f"{candle_d.weekday()} {candle_d} starts {target_interval.name}: {res}")

        #assign new date to candle
        next_week_date = candle.time_stamp_sec + target_interval.value * 60
        candle.time_stamp_sec = next_week_date
        
        now = datetime.now(timezone.utc).timestamp()

        if next_week_date > now:
            more = False


def _test_converter():
    # d.replace(tzinfo=timezone.utc).timestamp()
    

    candle_date = datetime(2023,6,4,0,0,0, tzinfo=timezone.utc) #sunday 00:00
    can_interval = DateTimeinterval("1m",1)
    # ts = candle_date.replace(tzinfo=timezone.utc).timestamp()
    ts = candle_date.timestamp()
    candle = CandleDataRecord(can_interval, ts,0,0,0,0,0,0)


    target_interval = DateTimeinterval("1w",10080)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("1d",1440)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("12h",720)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("4h",240)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("2h",120)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("1h",60)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("45m",45)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("30m",30)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("15m",15)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("10m",10)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

    target_interval = DateTimeinterval("5m",5)
    res = _is_candle_start_interval(candle,target_interval)
    print (f"{candle_date} starts {target_interval.name}: {res}")

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

CSV_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S" #2021-12-06 04:00:00

def _get_missing_row(last_saved: datetime, next_available: datetime, intervel: DateTimeinterval) -> dict:

    # last_saved_sec = last_saved.replace(tzinfo=timezone.utc).timestamp()
    # next_available_sec = next_available.replace(tzinfo=timezone.utc).timestamp()
     
    
    # first_misssing_sec = last_saved_sec + intervel.value * 60

    # last_misssing_sec = next_available_sec - intervel.value * 60

    # count = (last_misssing_sec - first_misssing_sec) / 60

    last_saved_dt_str = last_saved.strftime(CSV_DATE_TIME_FORMAT)
    next_available_dt_str = next_available.strftime(CSV_DATE_TIME_FORMAT)
    
    first_misssing_dt = last_saved + timedelta(minutes=intervel.value)
    first_misssing_dt_str = first_misssing_dt.strftime(CSV_DATE_TIME_FORMAT)

    last_misssing_dt = next_available - timedelta(minutes=intervel.value)
    last_misssing_dt_str = last_misssing_dt.strftime(CSV_DATE_TIME_FORMAT)

    diff_sec = (next_available - last_saved).total_seconds() 
    count =  int(((diff_sec / 60) -1) / intervel.value)

    return{
        "last_saved_sec": last_saved_dt_str,
        "first_misssing_sec": first_misssing_dt_str,
        "last_misssing_sec": last_misssing_dt_str,
        "count": count,
        "next_available_sec": next_available_dt_str,
    }

    return{
        "last_saved_sec": last_saved_sec,
        "first_misssing_sec": first_misssing_sec,
        "last_misssing_sec": last_misssing_sec,
        "count": count,
        "next_available_sec": next_available_sec,
    }

def _create_json(full_file_name: str):

    import json


    missings = []

    interval = DateTimeinterval("1m",1)
    last_saved_date = datetime(2023, 1, 1, 20, 55, 00)
    next_available_date = datetime(2023, 1, 1, 20, 57, 00)
    missings.append(_get_missing_row(last_saved_date, next_available_date, interval))

    # missings.append(_get_missing_row(2))


    with open(full_file_name,"w") as _target_file:
        json.dump(missings,_target_file)

def _test_delata_min():
    # datetime(year, month, day, hour, minute, second)
    later_date = datetime(2017, 6, 22, 18, 25, 30)
    eralier_date = datetime(2017, 6, 21, 18, 24, 10)
    
    # returns a timedelta object
    c = later_date-eralier_date
    print('Difference: ', c)
    
    minutes = c.total_seconds() / 60
    print('Total difference in minutes: ', minutes)
    
    # returns the difference of the time of the day
    minutes = c.seconds / 60
    print('Difference in minutes: ', minutes)

def _get_interval_last_closed_date(interval: DateTimeinterval) -> datetime:
    
    #region INIT
    last_closed_interval_dt = None
    base_date = datetime(2017,1,1,0,0,0,tzinfo=timezone.utc)
    now_utc = datetime.now(tz=timezone.utc)
    #endregion

    if interval.value != 10080:
        
        #region ALL BUT WEEK INTERVALS
        delta_from_base = now_utc - base_date
        minutes_from_base = delta_from_base.total_seconds() / 60

        last_close_min_from_start = minutes_from_base - interval.value - minutes_from_base % interval.value 
        #endregion

        last_closed_interval_dt = base_date + timedelta(minutes=last_close_min_from_start)

    else:
        #region WEEKLY INTERVALS (STARTS ON Monday)
        
        #region HOW MANY DAYS BACK TO LAST MONDAY
        ts_days = None
        day_in_week = now_utc.weekday()
        if day_in_week > 0:
            #all other days but Monday
            ts_days = (day_in_week) % 7
        else:
            ts_days = 0
        #endregion

        #region TIME SPAN BACK

        #add 7 days for 1 week back (last closed)
        ts_days +=7 
        ts_min = now_utc.minute
        ts_sec = now_utc.second
        ts_mili_sec = now_utc.microsecond // 1000 # (// -> floor)
        ts_micro_sec = now_utc.microsecond % 1000
        time_span = timedelta( days = ts_days, minutes=ts_min, seconds=ts_sec, milliseconds=ts_mili_sec,microseconds=ts_micro_sec)
        #endregion

        #endregion

        last_closed_interval_dt = now_utc - time_span
        
    return last_closed_interval_dt


def _read_json(full_file_name: str) -> object:
    
    import json
    with open(full_file_name, "r") as _open_file:
        data = json.load(_open_file)
    
    # print (data)
    # print(type(data))
    return data

def _dates():

    base_d = datetime(1970,1,1,0,0,0,tzinfo=timezone.utc)
    native_base_converted = base_d.replace(tzinfo=None)
    native_base_d = datetime(1970,1,1,0,0,0)

    
    print(f"native_base: {native_base_converted}")
    print(f"equal: {native_base_converted == native_base_d}")
    return

    print(base_d.weekday())
    print(base_d.isoweekday())
    print(base_d.strftime('%A'))
    return

    d1 = datetime(1970,1,1,0,0,0)
    d11 = d1.replace(tzinfo=timezone.utc)
    d12 = datetime.utcfromtimestamp(0)
    d13 = datetime.utcfromtimestamp(base_d.timestamp())

    d3 = base_d.astimezone(timezone.utc)
    d4 = datetime.fromtimestamp(0)

    d1_sec = d1.timestamp()
    d2_sec = base_d.timestamp()

    # if d1 > d2:
    #     print ("YEsssssssss")

    print(f"d1: {d1} - {d1_sec}")
    print(f"d2: {base_d} - {d2_sec}")

def _get_file_name_from_full_path(full_name: str) -> str:

    #for windows
    i = full_name.rfind(os.path.sep)
    file = full_name[i+1::] 
    
    return file

    if i < 0:
        i = full_name.rfind("/")

def _test_interval_last_closed_date():

    # interval = DateTimeinterval("10m",10)
    # now_demo = datetime(2017,1,1,0,11,32,tzinfo=timezone.utc)
    # last_close = _get_interval_last_closed_date(interval)
    # print(f"Now:{now_demo} interval:{interval.name} last_closed:{last_close}")


    # now_demo = datetime(2023,6,6,0,11,32,tzinfo=timezone.utc)
    interval = DateTimeinterval("1w",10080)

    for i in range(7):

        now_demo = datetime(2023,6,i+ 1,0,11,32,tzinfo=timezone.utc)
        last_close = _get_interval_last_closed_date(interval)
    
        closed_day_name = last_close.strftime('%A')
        print(f"interval:{interval.name} last_closed:{last_close} {closed_day_name}")
        # print(f"Now:{now_demo} {day_name} interval:{interval.name} last_closed:{last_close} {closed_day_name}")


def _test1(parameter: int):
    print(f"test1 para1: {parameter}" )

    parameter = parameter * 2

    print(f"test1 para2: {parameter}" )

def main(args):

    parameter_main = 2
    _test1(parameter_main)
    print(f"main returned: {parameter_main}" )

    return

    values = [1,2,3,4]

    val = values[:0:]
    print (val)
    return
    last_allowed = 4

    last_index = None
    for i in reversed(len(values)):
        if values[i] <= last_allowed:
            last_index = i
            break
    
    result_list = values[:last_index + 1:]
    #_test_interval_last_closed_date()

    _dates()
    return

    #to be stashed
    # _test_converter()
    _test_converter_week()
    return

    full_file_name = "missing.json"

    _create_json(full_file_name)
    missings = _read_json(full_file_name)

    for missing in missings:
        print(f"missing row: {missing}")

    # _test_thread()

    # print(f"main out")

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


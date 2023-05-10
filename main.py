from datetime import datetime
from awsApp import upload
from awsApp import download
import pandas as pd
from datetime import timezone, timedelta
from CandleRecord import CandleDataRecord
from CandleRecord import DateTimeInterval


binsizes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120, "4h": 240, "12h": 720, "1d": 1440, "1w": 10080}
def _find_most_cloesest_supported_interval(current_interval_minutes): # 17m
    
    
    reversed_bin_sizes = list(binsizes.items())
    reversed_bin_sizes.reverse() 
    nearsest_interval = reversed_bin_sizes[0] # 1w
 
    for index, (supported_interval, supported_interval_minutes) in enumerate(reversed_bin_sizes):
        if supported_interval_minutes < current_interval_minutes and current_interval_minutes % supported_interval_minutes == 0:
            nearsest_interval = supported_interval
            break
    
    return nearsest_interval

def _testUploadAWS():
    files = []
    files.append("D:\\kraken balance\\test.json")
    files.append("D:\\kraken balance\\testsnapshots.json")
    files.append("D:\\kraken balance\\test.log")

    destFolder = "Folder3/NewFolderToGet/"
    bucket_name="ojbucket-2"
    res = upload(files, destFolder, bucket_name)

def _testDownloadFromAWS():
    files = []
    files.append("D:\\kraken balance\\test.json")
    files.append("D:\\kraken balance\\testsnapshots.json")
    files.append("D:\\kraken balance\\test.log")

    # aws_folder = "Folder3/NewFolderToGet"
    aws_folder = "Folder3/"
    donwload_folder = "c:\\Temp\\"
    # donwload_folder = ""
    bucket_name="ojbucket-2"
    suffix = "json"
    download(bucket_name, aws_folder, suffix, donwload_folder) 

global_var = 3
def test_func():
    global_var = 4
    i = 0
    for n in range(10):
    
        try:
            raise Exception("issue")
            i = 10
        except Exception as e:
            print("exception cauth")

        print("another one")

        if i == 10:
            break
        else:
            continue
        
    return
    arr = ["data-201712","data-201801","data-201711","data-201802"]

    arr.sort()

    print(arr)

    return
    
    s = "abc-data.csv"
    index = len(s) - 4

    s2 = s[:index]
    print (len(s))
    print (index)
    print (s2)
    return
    d = datetime(2020,2,1)
    d2 = d - timedelta(seconds=1)

    print(f"d:{d} d2:{d2} -> {d.month == d2.month}")

    return

    
def _create_candle(v: int) -> CandleDataRecord:
    dt1 = DateTimeInterval("5m",5)
    c1 = CandleDataRecord(dt1, 1111111111 * v, 200 * v, 200 * v, 200 * v, 200 * v, 200 * v, 200 * v)

    return c1
def _test_dump_json():
    import json
    candles = []
    candles.append(_create_candle(1))
    candles.append(_create_candle(2))

    res = json.dumps([obj.to_json() for obj in candles])

    print(res)

def call1():
    call2()

def call2():
    import inspect
    frame = inspect.currentframe()
    print(f"func name: {frame.f_code.co_name}") 

    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print('caller name:', calframe[1][3])


def main(args):

    start = 1381095240
    first_c = datetime.utcfromtimestamp(start)
    end = 1672531140
    last_c = datetime.utcfromtimestamp(end)

    days_pass = (last_c - first_c).days
    min_pass = (last_c - first_c).total_seconds() / 60

    print(f"start: {first_c}")
    print(f"end: {last_c}")
    print(f"days passed: {days_pass}")
    print(f"days passed: {min_pass}")

    # call1()
    
    return

    t1 = {"k1": 2}

    
    t2 = t1
    t2["k1"] = 3
    print(t1)
    print(t2)

    _test_dump_json()

    # s = f"rr\ntt"
    # print(s)

    # test_func()
    # print("from main")

    # _testUploadAWS()
    
    # _testDownloadFromAWS()

    return

    # string = "orderType=lmt&side=buy&size=0.0001&symbol=PF_XBTUSD&cliOrdId=11InstanceID110021&triggerSignal=last&limitPrice=20000"
    string = "orderType=lmt&side=buy"
    URLEncode(string)
    # _testExe()

    return

if __name__ == '__main__':
   
    main(None)
  

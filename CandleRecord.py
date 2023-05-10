from datetime import datetime

CSV_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S" #2021-12-06 04:00:00

class DateTimeInterval:
    def __init__(self, name: str, val: int) -> None:
        self.name = name
        self.value = val
        # self.file_name_str = file_name_str

class CandleDataRecord:
    def __init__(self,interval: DateTimeInterval, time_stamp_sec: int, open: float, close: float
                ,high: float, low: float, volume: float, trades: int):
        #timestamp,open,high,low,close,volume,
        # close_time,
        # quote_av,trades, tb_base_av, tb_quote_av, ignore
        ## 2021-12-06 04:00:00
        self.interval = interval
        self.time_stamp_sec = time_stamp_sec
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.trades = trades

        self.close_time = time_stamp_sec * 1000 + 999 # milisec
        self.quote_av = 0
        self.tb_base_av = 0
        self.tb_quote_av = 0
        self.ignore = 0

    def get_date_time(self) -> datetime:
        return datetime.utcfromtimestamp(self.time_stamp_sec)

    def to_csv_array(self):
        candle = []
        # target csv candle:
        # [0] timestamp - #12/6/2021  4:00:00 AM
        # [1] open
        # [2] high
        # [3] low
        # [4] close
        # [5] volume
        # [6] close_time
        # [7] quote_av
        # [8] trades
        # [9] tb_base_av
        # [10] tb_quote_av
        # [11] ignore

        #calculate next candle start time (sec) 2. convert to milisec 3. reduce  1milisec
        close_time = (self.time_stamp_sec + self.interval.value * 60) * 1000 - 1

        candle.append(self._get_date_time_str())  # time[0]
        # next 4 (indexes 1-4) values order are the same
        candle.append(self.open) #1
        candle.append(self.high) #2
        candle.append(self.low) #3
        candle.append(self.close) #4
        candle.append(self.volume) #5
        candle.append(close_time) #6
        candle.append(0)  # [7] quote_av
        candle.append(self.trades)  # [8] trades
        candle.append(0)  # [9] tb_base_av
        candle.append(0)  # [10] tb_quote_av
        candle.append(0)  # [11] ignore

        return candle

    def get_csv_header(self) -> list:
        return ['timestamp', 'open', 'high', 'low', 'close', 'volume','close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']

    def _get_date_time_str(self) -> str:
        dt = datetime.utcfromtimestamp(self.time_stamp_sec)
        return dt.strftime(CSV_DATE_TIME_FORMAT)
    
    def to_json(self) -> dict:
        headers = self.get_csv_header()
        me_as_json = {}

        # handle time stamp (attribute name does not match cvs hadear)
        ts = "timestamp"
        headers.remove(ts)
        me_as_json[ts] = self.time_stamp_sec

        # add all other attributes
        for h in headers:
            me_as_json[h] = getattr(self, h)
        
        return me_as_json
        return {
            "interval": self.interval.value,
            "time-stamp-sec": self.time_stamp_sec,
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
            "volume": self.volume,
            "quote_av": self.quote_av,
            "quote_av": self.quote_av,
        }

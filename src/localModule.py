import pandas as pd
import datetime
#----

#pd.set_option('display.unicode.east_asian_width', True)
#pd.set_option('display.max_columns', 100)
#pd.set_option('display.max_rows', 500)
#pd.set_option("display.width", 2000)

#----

TABLE_FILE = '/root/table.csv'
FOLDER_OF_RECORD = '/mnt'
MARGIN_SECOND = 60

#----

URL_OF_R1 = 'https://nhkradioakr1-i.akamaihd.net/hls/live/511633/1-r1/1-r1-01.m3u8'
URL_OF_R2 = 'https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8'
URL_OF_FM = 'https://nhkradioakfm-i.akamaihd.net/hls/live/512290/1-fm/1-fm-01.m3u8'
KEY_OF_API = 'bqTooackky7Av8SCwUr6vjDatfm8qWRX'
URL_OF_API = 'https://api.nhk.or.jp/v2/pg/list'

DICTIONARY_OF_STATION_URL = {
  'r1' : URL_OF_R1,
  'r2' : URL_OF_R2,
  'r3' : URL_OF_FM,
}

#----

AREA = '130'
TABLE_DAYS = 2

#----

UPDATE_TIME_LINE = '04:00:00'
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

#----

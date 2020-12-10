import pandas as pd
#----

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)

#----

URL_OF_R1 = 'https://nhkradioakr1-i.akamaihd.net/hls/live/511633/1-r1/1-r1-01.m3u8'
URL_OF_R2 = 'https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8'
URL_OF_FM = 'https://nhkradioakfm-i.akamaihd.net/hls/live/512290/1-fm/1-fm-01.m3u8'
KEY_OF_API = 'bqTooackky7Av8SCwUr6vjDatfm8qWRX'
URL_OF_API = 'https://api.nhk.or.jp/v2/pg/list'

#----

AREA = '130'
SERVICES = ['r1','r2','r3']

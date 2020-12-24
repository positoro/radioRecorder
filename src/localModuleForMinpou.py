import pandas as pd
import datetime

#----

TABLE_FILE = '/root/table_for_minpou.csv'
FOLDER_OF_RECORD = '/mnt'
MARGIN_SECOND = 30

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

#----

RADIKO_AUTHKEY_VALUE='bcd151073c03b352e1ef2fd66c32209da9ca0afa'

RADIKO_AUTH1_FMS_URL='https://radiko.jp/v2/api/auth1'
RADIKO_AUTH2_FMS_URL='https://radiko.jp/v2/api/auth2'

#----

TABLE_DAYS = 2

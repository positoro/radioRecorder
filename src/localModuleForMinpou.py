import pandas as pd
import datetime
import requests
import base64

#----


#----

#DEBUG = True
DEBUG = False

if DEBUG:
  TABLE_FILE = '~/Desktop/table_for_minpou.csv'
  FOLDER_OF_RECORD = '~/Desktop'
  RECORDER_FOR_MINPOU = '~/Desktop/recorder_for_minpou.py'
else:
  TABLE_FILE = '/root/table_for_minpou.csv'
  FOLDER_OF_RECORD = '/mnt'
  RECORDER_FOR_MINPOU = '/root/recorder_for_minpou.py'


MARGIN_SECOND = 30

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

ATOMICPARSLEY = '/usr/bin/AtomicParsley'

#----

RADIKO_AUTHKEY_VALUE = 'bcd151073c03b352e1ef2fd66c32209da9ca0afa'

RADIKO_AUTH1_FMS_URL = 'https://radiko.jp/v2/api/auth1'
RADIKO_AUTH2_FMS_URL = 'https://radiko.jp/v2/api/auth2'

TABLE_URL = 'http://radiko.jp/v3/program/today/JP13.xml'

#----

GENRE_IN_META_DATA = 'Radio Program'

#----

def get_auth_token():

  headers_for_get_auth1_fms = {
     'pragma' : 'no-cache',
     'X-Radiko-App' : 'pc_html5',
     'X-Radiko-App-Version' : '0.0.1',
     'X-Radiko-User' : 'test-stream',
     'X-Radiko-Device' : 'pc'
  }

  response = requests.get(RADIKO_AUTH1_FMS_URL, headers=headers_for_get_auth1_fms)

  auth_token = response.headers['X-Radiko-AuthToken']
  key_length = int(response.headers['X-Radiko-KeyLength'])
  key_offset = int(response.headers['X-Radiko-KeyOffset'])

  auth_token_slice = RADIKO_AUTHKEY_VALUE[key_offset:key_offset + key_length]
  partial_key = base64.b64encode(auth_token_slice.encode())

#----
  
  headers_for_get_auth2_fms = {
     'pragma' : 'no-cache',
     'X-Radiko-AuthToken' : auth_token,
     'X-Radiko-PartialKey' : partial_key,
     'X-Radiko-User' : 'test-stream',
     'X-Radiko-Device' : 'pc'
  }

  response = requests.get(RADIKO_AUTH2_FMS_URL, headers=headers_for_get_auth2_fms)

  return auth_token

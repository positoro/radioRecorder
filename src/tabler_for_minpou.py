import pandas as pd
#import xml.etree.ElementTree as ET
import xmltodict
import requests
import datetime
import base64

import localModuleForMinpou

#----

date = datetime.date.today()

all_results = pd.DataFrame()

#----

def get_station_url():
  return 0

#
# get stream-url
#

#if [ -f ${channel}.xml ]; then
#  rm -f ${channel}.xml
#fi
#
#curl -s "http://radiko.jp/v2/station/stream_smh_multi/${channel}.xml" -o ${channel}.xml
#stream_url=`xmllint --xpath "/urls/url[@areafree='0'][1]/playlist_create_url/text()" ${channel}.xml`
#
#rm -f ${channel}.xml
#
########


#----

def get_table(): 

  table = pd.DataFrame()

  request_get = requests.get(localModuleForMinpou.TABLE_URL)
#  getted_xml_data = ET.fromstring(request_get.text)
  getted_data = xmltodict.parse(request_get.text)
  print(getted_data)

  TBS_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="TBS"'], sep='_')
  QRR_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="QRR"'], sep='_')
  LFR_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="LFR"'], sep='_')
  RN1_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="RN1"'], sep='_')
  RN2_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="RN2"'], sep='_')
  INT_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="INT"'], sep='_')
  FMT_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="FMT"'], sep='_')
  FMJ_result = pd.json_normalize(getted_xml_data['radiko']['stations']['station id="FMJ"'], sep='_')
  JORF_result = pd.json_normalize(getted_json_data['radiko']['stations']['station id="JORF"'], sep='_')
  BAYFM78_result = pd.json_normalize(getted_json_data['radiko']['stations']['station id="BAYFM78"'], sep='_')
  NACK5_result = pd.json_normalize(getted_json_data['radiko']['stations']['station id="NACK5"'], sep='_')
  YFM_result = pd.json_normalize(getted_json_data['radiko']['stations']['station id="YFM"'], sep='_')
  HOUSOU_DAIGAKU_result = pd.json_normalize(getted_json_data['radiko']['stations']['station id="HOUSOU-DAIGAKU"'], sep='_')

  day_result = pd.concat([
    TBS_result,
    QRR_result,
    LFR_result,
    RN1_result,
    RN2_result,
    INT_result,
    FMT_result,
    FMJ_result,
    JORF_result,
    BAYFM78_result,
    NACK5_result,
    YFM_result,
    HOUSOU_DAIGAKU_result,
  ])

  return day_result

#--------------------------------------------------------------------

auth_token = localModuleForMinpou.get_auth_token()

table = get_table()

print(table)

table['title'] = table['title'].apply(lambda x: '_'.join(x.split()))
table['title'] = table['title'].apply(lambda x: x.replace("\u25BD", '_'))

table = table.reset_index(drop=True)

#----

#all_results['start_time'] = pd.to_datetime(all_results['start_time'])
#all_results['end_time'] = pd.to_datetime(all_results['end_time'])
#all_results['air_time'] = all_results['end_time'] - all_results['start_time']

#----

#select_columns = [
#  'start_time',
#  'end_time',
#  'air_time',
#  'title',
#  'service_id',
#  'service_name',
#  'service_logo_l_url',
#]

#selected_results = all_results[select_columns]
#selected_results.to_csv(localModuleForMinpou.TABLE_FILE, index=None)

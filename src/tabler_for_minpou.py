import pandas as pd
import json
import requests
import datetime

import localModuleForMinpou

#----

date = datetime.date.today()

all_results = pd.DataFrame()

#----

def get_station_url():
  return 0

def get_auth_key():

  headers_for_get_auth1_fms = {
     'pragma' : 'no-cache',
     'X-Radiko-App' : 'pc_html5',
     'X-Radiko-App-Version' : '0.0.1',
     'X-Radiko-User' : 'test-stream',
     'X-Radiko-Device' : 'pc'
  }

  response = requests.get(localModuleForMinpou.RADIKO_AUTH1_FMS_URL, headers=headers_for_get_auth1_fms)
  print(response.headers)

  auth_token = response.headers['X-Radiko-AuthToken']
  key_length = response.headers['X-Radiko-KeyLength']
  key_offset = response.headers['X-Radiko-KeyOffset']

  partial_key=`echo "${RADIKO_AUTHKEY_VALUE}" | dd bs=1 "skip=${offset}" "count=${length}" 2> /dev/null | base64`

#----

  headers_for_get_auth2_fms = {
     'pragma' : 'no-cache',
     'X-Radiko-AuthToken' : auth_token,
     'X-Radiko-PartialKey' : partial_key,
     'X-Radiko-User' : 'test-stream',
     'X-Radiko-Device' : 'pc'
  }

  response = requests.get(localModuleForMinpou.RADIKO_AUTH2_FMS_URL, headers=headers_for_get_auth2_fms)

#######
#echo "authentication success"
areaid=`perl -ne 'print $1 if(/^([^,]+),/i)' auth2_fms_${pid}`
#echo "areaid: $areaid"

rm -f auth2_fms_${pid}

#
# get stream-url
#

if [ -f ${channel}.xml ]; then
  rm -f ${channel}.xml
fi

curl -s "http://radiko.jp/v2/station/stream_smh_multi/${channel}.xml" -o ${channel}.xml
stream_url=`xmllint --xpath "/urls/url[@areafree='0'][1]/playlist_create_url/text()" ${channel}.xml`

rm -f ${channel}.xml

#######


#----
def get_table(adding_day): 

  get_day = date + datetime.timedelta(days=adding_day)
  day_result = pd.DataFrame()
  url = localModule.URL_OF_API + '/{0}/radio/{1}.json?key={2}'.format(localModule.AREA, get_day, localModule.KEY_OF_API) request_get = requests.get(url) 

  if request_get.status_code != 200:
    print('can not get data')

  getted_json_data = request_get.json()

  r1_result = pd.json_normalize(getted_json_data['list']['r1'], sep='_')
  r2_result = pd.json_normalize(getted_json_data['list']['r2'], sep='_')
  r3_result = pd.json_normalize(getted_json_data['list']['r3'], sep='_')

  day_result = pd.concat([r1_result, r2_result, r3_result])

##
  day_result.drop_duplicates(subset='title', inplace=True)
##

  return day_result

#--------------------------------------------------------------------

get_auth_key()
 
#for adding_day in range(localModule.TABLE_DAYS):
#  all_results = pd.concat([all_results, get_table(adding_day)])

#----


#all_results['title'] = all_results['title'].apply(lambda x: '_'.join(x.split()))
#all_results['title'] = all_results['title'].apply(lambda x: x.replace("\u25BD", '_'))

#all_results = all_results.reset_index(drop=True)

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

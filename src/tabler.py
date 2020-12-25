import pandas as pd
import json
import requests
import datetime

import localModule

#----


#----

def get_table():

  date = datetime.date.today()
  day_result = pd.DataFrame()
  url = localModule.URL_OF_API + '/{0}/radio/{1}.json?key={2}'.format(localModule.AREA, date, localModule.KEY_OF_API)
  request_get = requests.get(url)

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

#----
 
table = get_table()

#----

table = table[~table['title'].str.contains('放送休止')]

table['title'] = table['title'].apply(lambda x: '_'.join(x.split()))
table['title'] = table['title'].apply(lambda x: x.replace("\u25BD", '_'))

table = table.reset_index(drop=True)

#----

table['start_time'] = pd.to_datetime(table['start_time'])
table['end_time'] = pd.to_datetime(table['end_time'])
table['air_time'] = table['end_time'] - table['start_time']

#----

select_columns = [
  'start_time',
  'end_time',
  'air_time',
  'title',
  'service_id',
  'service_name',
  'service_logo_l_url',
]

selected_results = table[table['service_id']=='r2']
selected_results = selected_results[select_columns]
selected_results.to_csv(localModule.TABLE_FILE, index=None)

import pandas as pd
import json
import requests
import datetime

import localModule

#----

date = datetime.date.today()

all_results = pd.DataFrame()

#----

def get_table(adding_day):

  get_day = date + datetime.timedelta(days=adding_day)

  day_result = pd.DataFrame()
  url = localModule.URL_OF_API + '/{0}/radio/{1}.json?key={2}'.format(localModule.AREA, get_day, localModule.KEY_OF_API)
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
 
for adding_day in range(localModule.TABLE_DAYS):
  all_results = pd.concat([all_results, get_table(adding_day)])

#----

all_results = all_results[~all_results['title'].str.contains('放送休止')]

all_results['title'] = all_results['title'].apply(lambda x: '_'.join(x.split()))
all_results['title'] = all_results['title'].apply(lambda x: x.replace("\u25BD", '_'))

all_results = all_results.reset_index(drop=True)

#----

all_results['start_time'] = pd.to_datetime(all_results['start_time'])
all_results['end_time'] = pd.to_datetime(all_results['end_time'])
all_results['air_time'] = all_results['end_time'] - all_results['start_time']

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

selected_results = all_results[select_columns]
selected_results.to_csv(localModule.TABLE_FILE, index=None)

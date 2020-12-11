import pandas as pd
import json
import requests
import datetime

import localModule

date = datetime.date.today()

all_results = pd.DataFrame()

url = localModule.URL_OF_API + '/{0}/radio/{1}.json?key={2}'.format(localModule.AREA, date, localModule.KEY_OF_API)
request_get = requests.get(url)

if request_get.status_code != 200:
  print('can not get data')

getted_json_data = request_get.json()

r1_result = pd.json_normalize(getted_json_data['list']['r1'])
r2_result = pd.json_normalize(getted_json_data['list']['r2'])
r3_result = pd.json_normalize(getted_json_data['list']['r3'])

all_results = pd.concat([r1_result, r2_result, r3_result])
all_results.drop_duplicates(subset='title', inplace=True)


#----

all_results = all_results[~all_results['title'].str.contains('放送休止')]

all_results['title'] = all_results['title'].apply(lambda x: '_'.join(x.split()))
all_results['title'] = all_results['title'].apply(lambda x: x.replace("\u25BD", '_'))

all_results = all_results.reset_index(drop=True)

#----

all_results['start_time'] = pd.to_datetime(all_results['start_time'], format='%Y/%m/%d %H:%M')
all_results['end_time'] = pd.to_datetime(all_results['end_time'], format='%Y/%m/%d %H:%M')
all_results['air_time'] = all_results['end_time'] - all_results['start_time']

select_columns = [
  'start_time',
  'end_time',
  'air_time',
  'title',
  'service.id',
  'service.name',
  'service.logo_l.url',
]

selected_results = all_results[select_columns]
selected_results.to_csv('./data/table.csv', index=None)

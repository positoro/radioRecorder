import pandas as pd
import json
import requests
import datetime

import localModule

date = datetime.date.today()

all_results = pd.DataFrame()

for service in localModule.SERVICES:
  url = localModule.URL_OF_API + '/{0}/{1}/{2}.json?key={3}'.format(localModule.AREA, service, date, localModule.KEY_OF_API)
  request_get = requests.get(url)

  if request_get.status_code != 200:
    print('can not get data')
    break

  getted_json_data = request_get.json()
  result = pd.json_normalize(getted_json_data['list'][service])

  all_results = pd.concat([all_results, result])

all_results = all_results[~all_results['title'].str.contains('放送休止')]
all_results = all_results.reset_index(drop=True)


all_results['title'] = all_results['title'].apply(lambda x: '_'.join(x.split()))
all_results['title'] = all_results['title'].apply(lambda x: x.replace("\u25BD", '_'))

#----

all_results['start_time'] = pd.to_datetime(all_results['start_time'], format='%Y/%m/%d %H:%M')
all_results['end_time'] = pd.to_datetime(all_results['end_time'], format='%Y/%m/%d %H:%M')
all_results['air_time'] = all_results['end_time'] - all_results['start_time']

##   Column                 Non-Null Count  Dtype                                
#---  ------                 --------------  -----                                
# 0   id                     197 non-null    object                               
# 1   event_id               197 non-null    object                               
# 2   start_time             197 non-null    datetime64[ns, pytz.FixedOffset(540)]
# 3   end_time               197 non-null    datetime64[ns, pytz.FixedOffset(540)]
# 4   title                  197 non-null    object                               
# 5   subtitle               197 non-null    object                               
# 6   content                197 non-null    object                               
# 7   act                    197 non-null    object                               
# 8   genres                 197 non-null    object                               
# 9   area.id                197 non-null    object                               
# 10  area.name              197 non-null    object                               
# 11  service.id             197 non-null    object                               
# 12  service.name           197 non-null    object                               
# 13  service.logo_s.url     197 non-null    object                               
# 14  service.logo_s.width   197 non-null    object                               
# 15  service.logo_s.height  197 non-null    object                               
# 16  service.logo_m.url     197 non-null    object                               
# 17  service.logo_m.width   197 non-null    object                               
# 18  service.logo_m.height  197 non-null    object                               
# 19  service.logo_l.url     197 non-null    object                               
# 20  service.logo_l.width   197 non-null    object                               
# 21  service.logo_l.height  197 non-null    object                               
# 22  airtime                197 non-null    timedelta64[ns]         

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

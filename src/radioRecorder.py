import pandas as pd
import json
import requests
import datetime

URL_OF_R1 = 'https://nhkradioakr1-i.akamaihd.net/hls/live/511633/1-r1/1-r1-01.m3u8'
URL_OF_R2 = 'https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8'
URL_OF_FM = 'https://nhkradioakfm-i.akamaihd.net/hls/live/512290/1-fm/1-fm-01.m3u8'
KEY_OF_API = 'bqTooackky7Av8SCwUr6vjDatfm8qWRX'


area = '130'
services = ['r1','r2','r3']
date = datetime.date.today()

all_results = pd.DataFrame()

for service in services:
  url = 'https://api.nhk.or.jp/v2/pg/list/{0}/{1}/{2}.json?key={3}'.format(area, service, date, KEY_OF_API)
  request_get = requests.get(url)

  if request_get.status_code != 200:
    print('can not get data')
    break

  getted_json_data = request_get.json(encoding='utf-8')
  result = pd.json_normalize(getted_json_data['list'][service])
  all_results = pd.concat([all_results, result])

all_results = all_results[~all_results['title'].str.contains('放送休止')]
all_results = all_results.reset_index(drop=True)

print(all_results['service.name'])
print(all_results)
print(all_results.info())
print(all_results.shape)

all_results.to_csv('./results.csv', index=None)

#ffmpeg -i https://nhkradiobkr1-i.akamaihd.net/hls/live/512291/1-r1/1-r1-01.m3u8 -t 900 -movflags faststart -c copy -bsf:a aac_adtstoasc r.m4a

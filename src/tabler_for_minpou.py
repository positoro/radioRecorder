import pandas as pd

import xml.etree.ElementTree as ET
import requests
import datetime
import localModuleForMinpou 

#----

date = datetime.date.today()
all_results = pd.DataFrame()

#----

def get_table(): 

  request_get = requests.get(localModuleForMinpou.TABLE_URL.format(date.strftime('%Y%m%d')))
  request_get.encoding = 'utf-8'
  getted_xml = ET.fromstring(request_get.text)

  list_of_table = []

  stations = getted_xml.findall('./stations/station')


  for station in stations:

    station_id = station.attrib['id'] 
    station_name = station.find('name').text
    progs = station.findall('./progs/prog')

    for prog in progs:
      
      prog_start_time = prog.attrib['ft'] 
      prog_end_time = prog.attrib['to'] 

      prog_title = prog.find('title').text
      prog_image_url = prog.find('img').text

      list_of_table.append([station_id, station_name, prog_start_time, prog_end_time, prog_title, prog_image_url])


  table = pd.DataFrame(list_of_table)
  table.columns = [
   'station_id',
   'station_name',
   'start_time',
   'end_time',
   'title',
   'image_url',
  ]
  
  return table

#--------------------------------------------------------------------

table = get_table()

table['title'] = table['title'].apply(lambda x: '_'.join(x.split()))
table['title'] = table['title'].apply(lambda x: x.replace("\u25BD", '_'))

table = table[table['title'] != '番組休止中']
table = table[~table['title'].duplicated()]
table = table[~table['title'].str.contains('放送休止')]

########################################

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
  'station_id',
  'station_name',
  'image_url',
]

selected_results = table[select_columns]
selected_results.to_csv(localModuleForMinpou.TABLE_FILE, index=None)

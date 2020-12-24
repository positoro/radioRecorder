import pandas as pd
import requests
import datetime
import subprocess

import xml.etree.ElementTree as ET

import localModuleForMinpou

#----

def get_station_url(station_id):

  request_get = requests.get(localModuleForMinpou.STATION_URL+'/'+station_id+'.xml')
  request_get.encoding = 'utf-8'
  getted_xml = ET.fromstring(request_get.text)

  station_url = getted_xml.findall('./url')[1].find('playlist_create_url').text
  
  return station_url

def atting_program(row):

  station_url = get_station_url(row.station_id)


  recorder_for_minpou_command_line = 'python recorder_for_minpou.py {0} {1} {2} {3} "{4}" {5} {6}'.format(
    row.start_time,
    station_url,
    int((row.air_time + datetime.timedelta(seconds=localModuleForMinpou.MARGIN_SECOND*2)).total_seconds()),
    row.start_time.strftime('%Y'),
    row.station_name,
    row.title,
    row.image_url,
  )

  command_line = "echo '{0}' | at -t {1}".format(
    recorder_for_minpou_command_line,
    (row.start_time - datetime.timedelta(seconds=localModuleForMinpou.MARGIN_SECOND)).strftime('%Y%m%d%H%M.%S'),
  )


#  res = subprocess.check_output(command_line, shell=True)
  print(command_line)

#----

table = pd.read_csv(localModuleForMinpou.TABLE_FILE)
table['start_time'] = pd.to_datetime(table['start_time'])
table['end_time'] = pd.to_datetime(table['end_time'])
table['start_time'] = pd.to_datetime(table['start_time'])
table['air_time'] = pd.to_timedelta(table['air_time'])

for row in table.itertuples():
  atting_program(row)

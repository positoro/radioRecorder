import pandas as pd
import datetime
import subprocess

import xml.etree.ElementTree as ET

import localModuleForMinpou

#----

def atting_program(row):

  recorder_for_minpou_command_line = 'python '+localModuleForMinpou.RECORDER_FOR_MINPOU+' "{0}" "{1}" "{2}" "{3}" "{4}" "{5}" "{6}"'.format(
    row.station_id,
    int((row.air_time + datetime.timedelta(seconds=localModuleForMinpou.MARGIN_SECOND*2)).total_seconds()),
    row.start_time.strftime('%Y'),
    row.station_name,
    row.title,
    row.image_url,
    row.start_time
  )

  at_launch_time = row.start_time - datetime.timedelta(seconds=localModuleForMinpou.MARGIN_SECOND)

  command_line = "sleep {0}; echo '{1}' | at -t {2}".format(
    at_launch_time.strftime('%S'),
    recorder_for_minpou_command_line,
    at_launch_time.strftime('%Y%m%d%H%M'),
  )

  res = subprocess.check_output(command_line, shell=True)
#  print(command_line)

#----

table = pd.read_csv(localModuleForMinpou.TABLE_FILE)
table['start_time'] = pd.to_datetime(table['start_time'])
table['end_time'] = pd.to_datetime(table['end_time'])
table['air_time'] = pd.to_timedelta(table['air_time'])

for row in table.itertuples():
  atting_program(row)

import pandas as pd
import json
import requests
import datetime

import localModule

#----

def atting_program(row):

  command_line = 'ffmpeg -i {0} -t {1} -movflags faststart -c copy -bsf:a aac_adtstoasc {2}.m4a'.format(
    localModule.DICTIONARY_OF_STATION_URL[row.service_id],
    int(row.air_time.total_seconds()),
    row.title+'-'+row.start_time.strftime('%Y%m%d%H%M'),
  )
  print(command_line)
#  recorder.at_program(
#    row.start_time,
##    row.end_time,
#    row.air_time,
#    row.title,
#    row.service_id,
#    row.service_name,
#    row.service_log_l_url
#  )



#----

table = pd.read_csv('./data/table.csv')
table['start_time'] = pd.to_datetime(table['start_time'])
table['end_time'] = pd.to_datetime(table['end_time'])
table['start_time'] = pd.to_datetime(table['start_time'])
table['air_time'] = pd.to_timedelta(table['air_time'])

update_time_line = datetime.datetime.strptime(localModule.UPDATE_TIME_LINE, '%H:%M:%S')

record_time_start_line = datetime.datetime.now(localModule.JST).replace(
  hour=update_time_line.hour,
  minute=update_time_line.minute,
  second=update_time_line.second,
  microsecond=0,
)

record_time_end_line = datetime.timedelta(days=1) + record_time_start_line

today_recording_program = table[
  (table['start_time'] >= record_time_start_line) &
  (table['start_time'] < record_time_end_line)
]

today_recording_program = today_recording_program.reset_index(drop=True)
print(today_recording_program.info())

for row in today_recording_program.itertuples():
  atting_program(row)

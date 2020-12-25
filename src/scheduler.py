import pandas as pd
import json
import requests
import datetime
import subprocess

import localModule

#----

def atting_program(row):

  ffmpeg_command_line = 'ffmpeg \
    -loglevel error \
    -fflags +discardcorrupt \
    -i {0} \
    -acodec copy \
    -movflags faststart \
    -vn \
    -bsf:a aac_adtstoasc \
    -t {1} \
    -metadata date="{2}" \
    -metadata genre="{3}" \
    -metadata artist="{4}" \
    -metadata title="{5}" \
    {6}/{7}.m4a'.format(

      localModule.DICTIONARY_OF_STATION_URL[row.service_id],
      int((row.air_time + datetime.timedelta(seconds=localModule.MARGIN_SECOND*2)).total_seconds()),
      row.start_time.strftime('%Y'),
      'Radio Program',
      row.service_name,
      row.title,
      localModule.FOLDER_OF_RECORD,
      row.title+'-'+row.start_time.strftime('%Y%m%d%H%M'),

  )
 
  at_launch_time = row.start_time - datetime.timedelta(seconds=localModule.MARGIN_SECOND)

  command_line = "sleep {0}; echo '{1}' | at -t {2}".format(
    at_launch_time.strftime('%S'),
    ffmpeg_command_line,
    at_launch_time.strftime('%Y%m%d%H%M'),
  )

  res = subprocess.check_output(command_line, shell=True)

#----

table = pd.read_csv(localModule.TABLE_FILE)
table['start_time'] = pd.to_datetime(table['start_time'])
table['end_time'] = pd.to_datetime(table['end_time'])
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

for row in today_recording_program.itertuples():
  atting_program(row)

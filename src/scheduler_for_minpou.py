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
    -movflags faststart \
    -vn \
    -acodec copy \
    -bsf:a aac_adtstoasc \
    -fflags +discardcorrupt \
    -i {0} \
    -t {1} \
    -metadata date="{2}" \
    -metadata genre="{3}" \
    -metadata artist="{4}" \
    -metadata title="{5}" \
    -headers "X-Radiko-Authtoken: {6}" \
    {7}/{8}.m4a'.format(

      row.station_url,
      int((row.air_time + datetime.timedelta(seconds=localModule.MARGIN_SECOND*2)).total_seconds()),
      row.start_time.strftime('%Y'),
      'Radio Program',
      row.service_name,
      row.title,
      row.auth_token,
      localModule.FOLDER_OF_RECORD,
      row.title+'-'+row.start_time.strftime('%Y%m%d%H%M'),

  )

  command_line = "echo '{0}' | at -t {1}".format(
    ffmpeg_command_line,
    (row.start_time - datetime.timedelta(seconds=localModule.MARGIN_SECOND)).strftime('%Y%m%d%H%M.%S'),
  )

  res = subprocess.check_output(command_line, shell=True)

#----

table = pd.read_csv(localModule.TABLE_FILE)
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

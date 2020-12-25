import sys
import localModuleForMinpou
import datetime
import requests
import subprocess
import re

station_id      = sys.argv[1]
duration_second = sys.argv[2]
date            = sys.argv[3]
genre           = localModuleForMinpou.GENRE_IN_META_DATA
artist          = sys.argv[4]
title           = sys.argv[5]
auth_token      = localModuleForMinpou.get_auth_token()
image_url       = sys.argv[6]
start_time      = sys.argv[7]

start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
data_file_name  = localModuleForMinpou.FOLDER_OF_RECORD+'/'+title+'-'+start_time.strftime('%Y%m%d%H%M')+'.m4a'

#---------------
def download_img(url, file_name):

    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


def tagging_cover_art(image_url, file_name):

  tmp_file = file_name + '.tmp'

  download_img(image_url, tmp_file)
  
  command_line = localModuleForMinpou.ATOMICPARSLEY + ' {0} --artwork {1}; rm {1}'.format(
    file_name,
    tmp_file,
  )

  res = subprocess.check_output(command_line, shell=True)

def get_station_url(station_id, auth_token):

  url_for_station_get = 'http://f-radiko.smartstream.ne.jp/{0}/_definst_/simul-stream.stream/playlist.m3u8'.format(station_id)

  headers =  {
    "X-Radiko-AuthToken": auth_token,
  }

  request_get = requests.get(url_for_station_get, headers=headers)
  request_get.encoding = 'utf-8'
  lines = re.findall('^https?://.+m3u8$', request_get.text, flags=(re.MULTILINE))

  return lines[0]

#---------------

station_url = get_station_url(station_id, auth_token)

ffmpeg_command_line = 'ffmpeg \
    -loglevel error \
    -fflags +discardcorrupt \
    -i "{0}" \
    -acodec copy \
    -movflags faststart \
    -vn \
    -bsf:a aac_adtstoasc \
    -t {1} \
    -metadata date="{2}" \
    -metadata genre="{3}" \
    -metadata artist="{4}" \
    -metadata title="{5}" \
    -headers "X-Radiko-Authtoken: {6}" \
    {7}'.format(

      station_url,
      duration_second,
      date,
      genre,
      artist,
      title,
      auth_token,
      data_file_name,
  )
command_line = "{0}".format(ffmpeg_command_line)
res = subprocess.check_output(command_line, shell=True)

tagging_cover_art(image_url, data_file_name)

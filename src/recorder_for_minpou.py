import sys
import localModuleForMinpou
import datetime
import urllib.request
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
def tagging_cover_art(image_url, file_name):
  
  command_line = "fmpeg -i {0} -i {1} -map 0 -map 1 -c copy -disposition:v:1 attached_pic {0}; rm {0}+'.uncoverd'".format(
    file_name,
    cover_artfile_name,
  )

def get_station_url(station_id, auth_token):

  url_for_station_get = 'http://f-radiko.smartstream.ne.jp/{0}/_definst_/simul-stream.stream/playlist.m3u8'.format(station_id)

  headers =  {
    "X-Radiko-AuthToken": auth_token,
  }

  request = urllib.request.Request(url_for_station_get, None, headers)
  response = urllib.request.urlopen(request)
  body = response.read().decode()
  lines = re.findall('^https?://.+m3u8$', body, flags=(re.MULTILINE))

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
#  res = subprocess.check_output(command_line, shell=True)
print(command_line)

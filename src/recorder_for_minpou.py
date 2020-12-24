import sys
import localModuleForMinpou

start_time      = sys.argv[1]
station_url     = sys.argv[2]
duration_second = sys.argv[3]
date            = sys.argv[4]
genre           = localModuleForMinpou.GENRE_IN_META_DATA
artist          = sys.argv[5]
title           = sys.argv[6]
auth_token      = localModuleForMinpou.get_auth_token()
image_url       = sys.argv[7]

data_file_name  = localModuleForMinpou.FOLDER_OF_RECORD+'/'+title+'-'+start_time.strftime('%Y%m%d%H%M')+'.m4a'

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
    {7}'.format(

      station_url,
      duration_second,
      date,
      genre,
      artist,
      title,
      auth_token,
      data_file_name+'.uncoverd',

  )


  command_line = "echo '{0}'".format(ffmpeg_command_line)
#  res = subprocess.check_output(command_line, shell=True)
  print(command_line)
  tagging_cover_art(image_url, data_file_name)

def tagging_cover_art(image_url, file_name):
  
  command_line = "fmpeg -i {0} -i {1} -map 0 -map 1 -c copy -disposition:v:1 attached_pic {0}; rm {0}+'.uncoverd'".format(
    file_name,
    cover_artfile_name,
  )

#res = subprocess.check_output(command_line, shell=True)
  print(command_line)

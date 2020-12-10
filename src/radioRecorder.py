import pandas as pd

all_results.to_csv('./results.csv', index=None)

#ffmpeg -i https://nhkradiobkr1-i.akamaihd.net/hls/live/512291/1-r1/1-r1-01.m3u8 -t 900 -movflags faststart -c copy -bsf:a aac_adtstoasc r.m4a

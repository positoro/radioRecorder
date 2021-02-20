# radioRecorder
radiko と らじる☆らじる を録音するものです。
 
番組表を得て基本的には全番組を自動的に録音します。
 
# Requirement
 
Docker の環境上で動くようにしています。
 
# Installation
 
 
```bash
$ git clone https://github.com/positoro/radioRecorder
$ cd radioRecorder
$ docker build . -t positoro/radio_recorder:0.1
$ docker run -h vladivostok -it -d positoro/radio_recorder:0.1
```
 
# Usage
 
インストール後、システムの cron 及び at で番組表の取得や録音が行われます。
 
```bash
root@vladivostok:/# crontab -l
SHELL=/bin/bash
PATH=/usr/local/bin:/bin:/usr/bin
HOME=/root
30 4 * * * python /root/tabler.py
35 4 * * * python /root/scheduler.py
45 4 * * * python /root/tabler_for_minpou.py
50 4 * * * python /root/program_selector_for_minpou.py
55 4 * * * python /root/scheduler_for_minpou.py
```
 
# Note
 
録音をする番組の選択などの際には
- tabler.py
- program_selector_for_minpou.py
を適宜編集してください。
 
# Author

positoro@gmail.com
 
# License
 
radioRecorder is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

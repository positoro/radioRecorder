FROM python:3

ENV TZ 'Asia/Tokyo'
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8


RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get -y install locales
RUN locale-gen
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN apt-get install -y vim
RUN apt-get install -y less
RUN apt-get install -y ffmpeg
RUN apt-get install -y at
RUN apt-get install -y cron
RUN apt-get clean

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pandas
RUN pip install requests

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN git clone https://github.com/positoro/radioRecorder /root/radioRecorder
RUN cp /root/radioRecorder/src/*.py /root

ENTRYPOINT service cron start
ENTRYPOINT service atd start
ENTRYPOINT (            echo "SHELL=/bin/bash")                                        | crontab -
ENTRYPOINT (crontab -l; echo "PATH=/usr/local/bin:/bin:/usr/bin")                      | crontab -
ENTRYPOINT (crontab -l; echo "HOME=/root")                                             | crontab -
ENTRYPOINT (crontab -l; echo "30 4 * * * python /root/tabler.py")                      | crontab -
ENTRYPOINT (crontab -l; echo "35 4 * * * python /root/scheduler.py")                   | crontab -
ENTRYPOINT (crontab -l; echo "45 4 * * * python /root/tabler_for_minpou.py")           | crontab -
ENTRYPOINT (crontab -l; echo "50 4 * * * python /root/program_selector_for_minpou.py") | crontab -
ENTRYPOINT (crontab -l; echo "55 4 * * * python /root/scheduler_for_minpou.py")        | crontab -
ENTRYPOINT /bin/bash

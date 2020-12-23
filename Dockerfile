FROM python:3

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ 'Asia/Tokyo'

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get -y install locales
RUN locale-gen
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN apt install -y man man-db manpages
RUN apt install -y vim
RUN apt install -y less
RUN apt install -y ffmpeg
RUN apt install -y at
RUN apt install -y cron
RUN apt clean

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pandas
RUN pip install requests

ENTRYPOINT service atd start ;\
           service cron start ;\
           (crontab -l; echo "30 7 * * * 'python3 /root/tabler.py'")    | crontab - ;\
           (crontab -l; echo "45 7 * * * 'python3 /root/scheduler.py'") | crontab - ;\
           /bin/bash

FROM ubuntu:20.04

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ 'Asia/Tokyo'

RUN apt update
RUN apt -y upgrade
run yes | unminimize
RUN apt install -y language-pack-ja
RUN apt install tzdata
RUN apt install -y man man-db manpages
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y vim
RUN apt install -y less
RUN apt install -y ffmpeg
RUN apt install -y at
RUN apt install -y cron
RUN apt clean

RUN pip3 install pandas
RUN pip3 install requests

RUN update-locale LANG=ja_JP.UTF-8

ENTRYPOINT service atd start ;\
           service cron start ;\
           (crontab -l; echo "30 7 * * * 'python3 /root/tabler.py'")    | crontab - ;\
           (crontab -l; echo "45 7 * * * 'python3 /root/scheduler.py'") | crontab - ;\
           /bin/bash

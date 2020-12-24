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

RUN apt-get install -y man man-db manpages
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
RUN pip install xmltodict

ENTRYPOINT service atd start ;\
           service cron start ;\
           (crontab -l; echo "30 3 * * * 'python /root/tabler.py'")    | crontab - ;\
           (crontab -l; echo "45 3 * * * 'python /root/scheduler.py'") | crontab - ;\
           /bin/bash

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

COPY ./src/localModule.py /root
COPY ./src/tabler.py /root
COPY ./src/scheduler.py /root
COPY ./src/localModuleForMinpou.py /root
COPY ./src/tabler_for_minpou.py /root
COPY ./src/program_selector_for_minpou.py /root
COPY ./src/scheduler_for_minpou.py /root
COPY ./src/recorder_for_minpou.py /root


ENTRYPOINT service cron start ;\
           service atd start ;\
           (            echo "SHELL=/bin/bash") | crontab - ;\
           (crontab -l; echo "PATH=/usr/local/bin:/bin:/usr/bin") | crontab - ;\
           (crontab -l; echo "HOME=/root") | crontab - ;\
           (crontab -l; echo "30 4 * * * python /root/tabler.py") | crontab - ;\
           (crontab -l; echo "35 4 * * * python /root/scheduler.py") | crontab - ;\
           (crontab -l; echo "45 4 * * * python /root/tabler_for_minpou.py") | crontab - ;\
           (crontab -l; echo "50 4 * * * python /root/program_selector_for_minpou.py") | crontab - ;\
           (crontab -l; echo "55 4 * * * python /root/scheduler_for_minpou.py") | crontab - ;\
           /bin/bash

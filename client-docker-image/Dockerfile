FROM debian:buster

RUN echo 'deb http://deb.debian.org/debian buster-backports main' >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get -y install \
    xvfb \
    nano \
    libgtk-3-0 \
    libdbus-glib-1-dev \
    python3 \
    ansible \
    procps \
    python3-pip && \
    apt-get -t buster-backports -y install \
    tor && \
    pip3 install \
    tbselenium \
    stem \
    pyvirtualdisplay && \
    pip3 install --upgrade requests

RUN useradd --system --uid 666 -M --shell /usr/sbin/nologin hidden

ADD ./geckodriver /usr/local/bin/geckodriver
ADD ./tor-browser_en-US /tor-browser_en-US
ADD ./client-docker-image/main.sh /main.sh
ADD ./inventory.cfg /inventory.cfg
ADD ./client-docker-image/experiment.py /experiment.py

RUN chmod +x /main.sh
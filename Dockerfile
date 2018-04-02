# VERSION 1.9
# AUTHOR: Erik Rivera
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t erikriver/docker-airflow .
# SOURCE: https://bitbucket.org/kimetrics/airflow

FROM python:3.6-slim
MAINTAINER erik@rivera.pro

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.9.0
ARG AIRFLOW_HOME=/usr/local/airflow
ARG FIREFOX_VERSION=59.0.2
ARG GECKODRIVER_VERSION=latest

# Define es_MX.
ENV LANGUAGE es_MX.UTF-8
ENV LANG es_MX.UTF-8
ENV LC_ALL es_MX.UTF-8
ENV LC_CTYPE es_MX.UTF-8
ENV LC_MESSAGES es_MX.UTF-8

RUN apt-get update -qqy && apt-get install -y \
    # Headless browser support
    xvfb \
    # Needed to launch firefox
    libasound2 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxcomposite1 \
    wget \
    bzip2


#=========
# Firefox
#=========
RUN FIREFOX_DOWNLOAD_URL=$(if [ $FIREFOX_VERSION = "nightly" ] || [ $FIREFOX_VERSION = "devedition" ]; then echo "https://download.mozilla.org/?product=firefox-$FIREFOX_VERSION-latest-ssl&os=linux64&lang=en-US"; else echo "https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2"; fi) \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

#============
# GeckoDriver
#============
RUN GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo $(wget -qO- "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([0-9.]+)".*/\1/'); else echo $GECKODRIVER_VERSION; fi) \
  && echo "Using GeckoDriver version: "$GK_VERSION \
  && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
  && chmod 755 /opt/geckodriver-$GK_VERSION \
  && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver



RUN set -ex \
    && buildDeps=' \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        python3-pip \
        python3-requests \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# es_MX.UTF-8 UTF-8$/es_MX.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=es_MX.UTF-8 LC_ALL=es_MX.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install Cython \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,s3]==$AIRFLOW_VERSION \
    && pip install celery[redis]==4.0.2 \
    && pip install pyarrow \
    && pip install elasticsearch \
    && pip install espandas \
    && pip install s3fs \
    && pip install beautifulsoup4 \
    && pip install scrapy \
    && pip install selenium \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /var/cache/apt/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN echo "America/Mexico_City" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]

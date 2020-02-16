FROM debian:9

WORKDIR /usr/local

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    mkdir -p /usr/local/temp

COPY mirror_crawler.py /usr/local/
COPY requirements.txt /usr/local/

RUN pip3 install -r /usr/local/requirements.txt

ENTRYPOINT ["/usr/bin/python3", "/usr/local/mirror_crawler.py"]
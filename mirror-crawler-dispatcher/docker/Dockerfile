FROM debian:9

WORKDIR /usr/local

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip

COPY mirror_crawler_dispatcher.py config.yaml requirements.txt /usr/local/

RUN pip install -r /usr/local/requirements.txt

ENTRYPOINT ["/usr/bin/python3", "/usr/local/mirror_crawler_dispatcher.py"]
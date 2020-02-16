FROM debian:9

WORKDIR /usr/local

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip curl apt-transport-https && \
    curl -o google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-278.0.0-linux-x86_64.tar.gz && \
    tar xvzf google-cloud-sdk.tar.gz && \
    (echo y; echo y; echo) | ./google-cloud-sdk/install.sh && \
    mkdir -p /usr/local/temp

RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg -o apt-key.gpg && \
    apt-key add apt-key.gpg && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" >> /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y kubectl

COPY mirror_crawler_dispatcher.py config.yaml requirements.txt mirror-crawler.j2 kube.sh /usr/local/

RUN pip3 install -r /usr/local/requirements.txt && \
    chmod +x /usr/local/kube.sh

ENTRYPOINT ["/usr/bin/python3", "/usr/local/mirror_crawler_dispatcher.py"]
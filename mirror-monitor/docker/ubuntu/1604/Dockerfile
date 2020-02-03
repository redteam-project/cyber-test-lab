FROM ubuntu:16.04

WORKDIR /usr/local

ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/creds.json
ENV PATH=$PATH:/usr/local/google-cloud-sdk/bin

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python curl && \
    curl -o google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-278.0.0-linux-x86_64.tar.gz && \
    tar xvzf google-cloud-sdk.tar.gz && \
    (echo y; echo y; echo) | ./google-cloud-sdk/install.sh

COPY update_mirrors.sh /usr/local/

ENTRYPOINT ["/bin/bash", "/usr/local/update_mirrors.sh"]


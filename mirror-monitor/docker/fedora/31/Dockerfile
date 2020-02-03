FROM fedora:31

WORKDIR /usr/local

ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/creds.json
ENV PATH=$PATH:/usr/local/google-cloud-sdk/bin

RUN curl -o google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-278.0.0-linux-x86_64.tar.gz && \
    tar xvzf google-cloud-sdk.tar.gz && \
    dnf install -y python36 && \
    (echo y; echo y; echo) | ./google-cloud-sdk/install.sh

COPY update_mirrors.sh /usr/local/

ENTRYPOINT ["/bin/bash", "/usr/local/update_mirrors.sh"]
FROM centos:6

WORKDIR /usr/local

ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/creds.json
ENV PATH=$PATH:/usr/local/google-cloud-sdk/bin
ENV CLOUDSDK_PYTHON=/opt/rh/rh-python35/root/usr/bin/python

RUN curl -o google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-278.0.0-linux-x86_64.tar.gz && \
    tar xvzf google-cloud-sdk.tar.gz && \
    yum install -y centos-release-scl && \
    yum install -y rh-python35 && \
    source /opt/rh/rh-python35/enable && \
    (echo y; echo y; echo) | CLOUDSDK_PYTHON=/opt/rh/rh-python35/root/usr/bin/python ./google-cloud-sdk/install.sh

COPY update_mirrors.sh /usr/local/

ENTRYPOINT ["/bin/bash", "/usr/local/update_mirrors.sh"]



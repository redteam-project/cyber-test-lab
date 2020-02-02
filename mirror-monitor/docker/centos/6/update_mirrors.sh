#!/bin/bash

yum update -y
source /opt/rh/rh-python35/enable
gcloud auth activate-service-account --key-file=/secrets/creds.json
gsutil cp /var/cache/yum/x86_64/6/timedhosts.txt gs://${MIRROR_BUCKET}/mirrors/files/${MIRROR_OS}/${MIRROR_VERSION}/

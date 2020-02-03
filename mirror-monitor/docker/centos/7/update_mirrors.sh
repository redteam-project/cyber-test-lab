#!/bin/bash

yum update -y
gcloud auth activate-service-account --key-file=/secrets/creds.json
gsutil cp -r /etc/yum.repos.d gs://${MIRROR_BUCKET}/mirrors/files/${MIRROR_OS}/${MIRROR_VERSION}/
gsutil cp /var/cache/yum/x86_64/7/timedhosts.txt gs://${MIRROR_BUCKET}/mirrors/files/${MIRROR_OS}/${MIRROR_VERSION}/

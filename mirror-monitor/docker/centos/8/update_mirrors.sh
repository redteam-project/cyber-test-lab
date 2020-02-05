#!/bin/bash

set -x
yum update -y
gcloud auth activate-service-account --key-file=/secrets/creds.json
gsutil cp -r /etc/yum.repos.d gs://${MIRROR_BUCKET}/mirrors/files/${MIRROR_OS}/${MIRROR_VERSION}/

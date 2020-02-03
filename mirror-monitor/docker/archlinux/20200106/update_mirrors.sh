#!/bin/bash

pacman -Syu --noconfirm
gcloud auth activate-service-account --key-file=/secrets/creds.json
gsutil cp -r /etc/pacman.d/mirrorlist* gs://${MIRROR_BUCKET}/mirrors/files/${MIRROR_OS}/${MIRROR_VERSION}/



#!/bin/bash

set -x
gcloud auth activate-service-account --key-file=/secrets/creds.json
gcloud container clusters get-credentials ${CLUSTER_ID} --region ${REGION}
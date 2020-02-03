#!/bin/bash

export ARCH_MIRROR_PAGE="https://www.archlinux.org/mirrorlist/?country=all&protocol=https&ip_version=4"
export CENTOS_MIRROR_PAGE="https://centos.org/download/full-mirrorlist.csv"
export DEBIAN_MIRROR_PAGE="https://www.debian.org/mirror/list"
export FEDORA_MIRROR_PAGE="https://admin.fedoraproject.org/mirrormanager/"
export UBUNTU_MIRROR_PAGE="https://launchpad.net/ubuntu/+archivemirrors"

gcloud auth activate-service-account --key-file=/secrets/creds.json

curl -o arch_mirrors.txt ${ARCH_MIRROR_PAGE}
gsutil cp arch_mirrors.txt gs://${MIRROR_BUCKET}/mirrors/files/archlinux/site/

curl -o centos_full-mirrorlist.csv ${CENTOS_MIRROR_PAGE}
gsutil cp centos_full-mirrorlist.csv gs://${MIRROR_BUCKET}/mirrors/files/centos/site/

curl -o debian_mirrors.html ${DEBIAN_MIRROR_PAGE}
gsutil cp debian_mirrors.html gs://${MIRROR_BUCKET}/mirrors/files/debian/site/

curl -o fedora_mirrors.html ${FEDORA_MIRROR_PAGE}
gsutil cp fedora_mirrors.html gs://${MIRROR_BUCKET}/mirrors/files/fedora/site/

curl -o ubuntu_mirrors.html ${UBUNTU_MIRROR_PAGE}
gsutil cp ubuntu_mirrors.html gs://${MIRROR_BUCKET}/mirrors/files/ubuntu/site/

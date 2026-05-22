#!/bin/bash

set -euo pipefail

SERVER_NAME="ephemeral-runner-1779433558"

IMAGE="ubuntu-24.04"
TYPE="cx22"
LOCATION="fsn1"

curl -L https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar xz

sudo mv hcloud /usr/local/bin/

CLOUD_INIT=$(mktemp)

sed   -e "s/GITHUB_OWNER/${GITHUB_REPOSITORY_OWNER}/g"   -e "s/GITHUB_REPO/${GITHUB_REPOSITORY##*/}/g"   -e "s/RUNNER_TOKEN/${RUNNER_TOKEN}/g"   -e "s/TAILSCALE_AUTH_KEY/${TAILSCALE_AUTH_KEY}/g"   cloud-init/runner-cloud-init.yml.tpl > $CLOUD_INIT

OUTPUT=$(hcloud server create   --name $SERVER_NAME   --image $IMAGE   --type $TYPE   --location $LOCATION   --user-data-from-file $CLOUD_INIT)

SERVER_ID=$(echo "$OUTPUT" | grep 'Server:' | awk '{print $2}')

echo "SERVER_ID=$SERVER_ID" >> $GITHUB_ENV

echo "Created VPS $SERVER_ID"

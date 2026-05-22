#!/bin/bash

set -euo pipefail

curl -L https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar xz

sudo mv hcloud /usr/local/bin/

hcloud server delete $SERVER_ID

echo "Destroyed VPS $SERVER_ID"

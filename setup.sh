#!/bin/bash

set -e
cd $(dirname $0)

source config.sh

bash scripts/install-packages.sh

bash scripts/submodule.sh init

cp -rf $AM_SUBMODULE /etc/openvpn/keys

python3 generators/server.py

bash scripts/sysctl.sh
python3 scripts/iptables.py

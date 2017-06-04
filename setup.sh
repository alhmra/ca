#!/bin/bash

set -e
cd $(dirname $0)

source config.sh

# Currently available version is 2.3, but we need 2.4, so add it from OpenVPN apt repo
source /etc/lsb-release # Need for $DISTRIB_CODENAME
wget -O - https://swupdate.openvpn.net/repos/repo-public.gpg|apt-key add -
echo "deb http://build.openvpn.net/debian/openvpn/release/2.4 $DISTRIB_CODENAME main" > /etc/apt/sources.list.d/openvpn-aptrepo.list

apt-get update
apt-get install openvpn easy-rsa whois python3

git submodule init
git submodule update

cp -rf $AM_SUBMODULE /etc/openvpn/keys

python3 generators/server.py

sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE

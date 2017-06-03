#!/bin/bash

# Currently available version is 2.3, but we need 2.4, so add it from OpenVPN apt repo
source /etc/lsb-release # Need for $DISTRIB_CODENAME
wget -O - https://swupdate.openvpn.net/repos/repo-public.gpg|apt-key add -
echo "deb http://build.openvpn.net/debian/openvpn/release/2.4 $DISTRIB_CODENAME main" > /etc/apt/sources.list.d/openvpn-aptrepo.list

apt-get update
apt-get install openvpn easy-rsa whois

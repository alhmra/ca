#!/bin/bash

# Show the absolute path of the top-level directory
export AM_ROOT=$(git rev-parse --show-toplevel)

export AM_DOMAIN="alohomora.xyz"
export AM_VPN="public-vpn.$AM_DOMAIN"
export AM_SUBMODULE="keys"

# Some of Easy-rsa vars
export KEY_SIZE=1024
# Absolute path to submodule that stores keys, should be `sourced` with an argument `server` or `client`
export KEY_DIR="$AM_ROOT/$AM_SUBMODULE/$1"
export KEY_OU=$AM_DOMAIN
export KEY_CN="Alohomora"
export KEY_ALTNAMES="something"

#!/bin/bash

# Show the absolute path of the top-level directory
ROOT=$(git rev-parse --show-toplevel)

export AM_DOMAIN="alohomora.xyz"
export AM_VPN="public-vpn.$DOMAIN"
export AM_SUBMODULE="keys"

export KEY_SIZE=1024
# Absolute path to submodule that stores keys, should be `sourced` with an argument `server` or `client`
export KEY_DIR="$ROOT/$AM_SUBMODULE/$1"
export KEY_OU=$DOMAIN
export KEY_CN="Alohomora"

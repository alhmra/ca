#!/bin/bash

set -e
cd $(dirname $0)

SUBMODULE_DIR="server"

KEYS_IN="ca"
KEYS_OUT="$SUBMODULE_DIR/keys"

if [ ! -d "$KEYS_OUT" ]; then
	mkdir "$KEYS_OUT"
fi

yes | cp -rfT "$KEYS_IN/client/keys" "$KEYS_OUT/client"
yes | cp -rfT "$KEYS_IN/server/keys" "$KEYS_OUT/server"

SRV_IN="ovpn"
SRV_OUT=$SUBMODULE_DIR

if [ ! -d "$SRV_OUT/ccd" ]; then
	mkdir "$SRV_OUT/ccd"
fi

yes | cp -rf "$SRV_IN/server.conf" $SRV_OUT
yes | cp -rf "$SRV_IN/ccd/DEFAULT" "$SRV_OUT/ccd/DEFAULT"

git submodule init
git submodule update

cd $SUBMODULE_DIR

git add --all .
git commit -m "Update $(date)"
git push

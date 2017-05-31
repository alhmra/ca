#!/bin/bash

set -e
cd $(dirname $0)

if [ -n "$1" ]; then
	SRV_CONF="server.conf"
	SRV_ADDR="public-vpn.alohomora.xyz"

	KEY_DIR="../ca/keys"

	OUT_DIR="ccd/generated"
	OUT_FILE="$OUT_DIR/$1.ovpn"

	if [ ! -d "$OUT_DIR" ]; then
		mkdir "$OUT_DIR"
	fi

	printf "\
client
nobind
resolv-retry infinite
setenv opt block-outside-dns
remote-cert-tls server
" > $OUT_FILE

	while read key value; do
		if [ "$key" = "port" ]; then
			if [ "$value" != "1194" ]; then
				echo "remote $SRV_ADDR $value" >> $OUT_FILE
			else
				echo "remote $SRV_ADDR" >> $OUT_FILE
			fi
		
		elif [ "$key" = "proto" ]; then
			echo "proto $value" >> $OUT_FILE

		elif [ "$key" = "dev" ]; then
			echo "dev $value" >> $OUT_FILE

		elif [ "$key" = "persist-key" ]; then
			echo "persist-key" >> $OUT_FILE

		elif [ "$key" = "persist-tun" ]; then
			echo "persist-tun" >> $OUT_FILE

		elif [ "$key" = "comp-lzo" ]; then
			echo "comp-lzo" >> $OUT_FILE

		elif [ "$key" = "cipher" ]; then
			echo "cipher $value" >> $OUT_FILE

		elif [ "$key" = "ca" ]; then
			printf "\
<ca>
$(<$KEY_DIR/server/ca.crt)
</ca>
" >> $OUT_FILE

		elif [ "$key" = "cert" ]; then
			printf "\
<cert>
$(grep -Pzo '(?s)-{5}BEGIN (CERTIFICATE)-{5}.*?-{5}END \1-{5}' $KEY_DIR/client/$1.crt)
</cert>
" >> $OUT_FILE

		elif [ "$key" = "key" ]; then
			printf "\
<key>
$(<$KEY_DIR/client/$1.key)
</key>
" >> $OUT_FILE

		elif [ "$key" = "tls-auth" ]; then
			printf "\
key-direction 1
<tls-auth>
$(grep -o '^[^#]*' $KEY_DIR/server/ta.key)
</tls-auth>
" >> $OUT_FILE
		fi

	done <<< $(grep -o '^[^#]*' $SRV_CONF)
else
	echo "No argument (client) specified."
fi

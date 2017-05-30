#!/bin/bash

# Easy-rsa docs
# https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html

set -e

mc() {
	make-cadir $1
	echo "New CA dir '$1' successfully created."
	cd $1
}

issue_ca() {
	printf "\n\n$1\n\n"

	source vars
	bash clean-all
	KEY_SIZE=1024

	if [ "$1" == "server" ]; then
		printf ".\n.\n.\n.\n.\nAlohomora Server\n.\n.\n" | bash build-ca
		bash build-key-server server
		bash build-dh
		openvpn --genkey --secret keys/ta.key
	fi
	
	if [ "$1" == "client" ]; then
		printf ".\n.\n.\n.\n.\nAlohomora Client\n.\n.\n" | bash build-ca
		bash build-key public
	fi

	cd ..
}

main() {
	if [ -d "$1" ]; then
		read -p "The '$1' dir already exists. Do you wish to remove it and create a *new* CA dir? [y/n]: " RESP
		if [[ $RESP =~ ^(y|Y|yes|Yes|n|N|no|No)$ ]]; then
			if [[ $RESP =~ ^(y|Y|yes|Yes)$ ]]; then
				rm -rf $1
				mc $1
			else
				echo "Exit"
				exit 1
			fi
		else
			echo "Incorrent response."
			exit 1
		fi
	else
		mc $1
	fi

	issue_ca $1
}

cd $(dirname $0)

main server
main client

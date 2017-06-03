#!/bin/bash

set -e
cd $(dirname $0)

issue_ca() {
	printf "\n$1\n\n"

	source vars
	source ../../config.sh $1

	bash clean-all
	
	printf ".\n.\n.\n.\n\n$KEY_CN $1 CA\n.\n.\n" | bash build-ca

	if [ "$1" == "server" ]; then
		bash build-key-server server
		bash build-dh
		openvpn --genkey --secret $KEY_DIR/ta.key
	elif [ "$1" == "client" ]; then
		bash build-key public
	fi
}

main() {
	if [ -d "$1" ]; then
		read -p "The '$1' dir already exists. Do you wish to remove it and create a *new* CA dir? [y/n]: " RESP
		if [[ $RESP =~ ^(y|Y|yes|Yes|n|N|no|No)$ ]]; then
			if [[ $RESP =~ ^(y|Y|yes|Yes)$ ]]; then
				rm -rf $1
			else
				echo "Exit"
				exit 1
			fi
		else
			echo "Incorrent response."
			exit 1
		fi
	fi

	make-cadir $1
	echo "New CA dir '$1' successfully created."
	cd $1

	issue_ca $1

	cd ..
}

bash ../scripts/init-submodule.sh

main server
main client

cd "$AM_ROOT/$AM_SUBMODULE"
git add --all .
git commit -m "New (ca/cert/key)s $(date)"
git push

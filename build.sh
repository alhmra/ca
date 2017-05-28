#!/bin/bash

# Easy-rsa docs
# https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html

# $1 - ca dir

main() {
	echo "Creating a new directory and prepares it to be used as a (CA) key management directory"
	make-cadir $1
	cd $1

	echo "Applying variables"
	cp ../vars.const vars
	source vars > /dev/null
	
	echo "Cleaning 'keys' dir"
	./clean-all
	
	# Build root certificate authority (CA) certificate/key
	./build-ca
	
	./build-key-server $KEY_ORG
	
	# Build Diffie-Hellman parameters (necessary for the server end of a SSL/TLS connection)
	./build-dh
	
	# create an "HMAC firewall" to help block DoS attacks and UDP port flooding.
	openvpn --genkey --secret keys/ta.key
}

if [ -d "$1" ]
then
	read -p "The '$1' dir already exists. Do you wish to remove it and continue? [yes/no]: " RESP

	if [[ ! $RESP =~ ^(y|Y|yes|Yes|n|N|no|No)$ ]]
	then
		echo "Incorrent response, exit"
	else
		if [[ $RESP =~ ^(y|Y|yes|Yes)$ ]]
		then
			rm -rf $1
			main
		else
			echo "Exit"
			exit 1
		fi
	fi
else
	main
fi

#!/bin/bash

# Easy-rsa docs
# https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html

set -e

check_dir() {
	if [ -d "$1" ]; then
		read -p "The '$1' dir already exists. Do you wish to remove it and continue? [yes/no]: " RESP
		if [[ $RESP =~ ^(y|Y|yes|Yes|n|N|no|No)$ ]]; then
			if [[ $RESP =~ ^(y|Y|yes|Yes)$ ]]; then
				rm -rf $1
			else
				echo "Exit"
				exit 1
			fi
		else
			echo "Incorrent response, exit"
			exit 1
		fi
	fi
}

server_ck() {
	if [ -d "keys" ]; then
		echo
		echo "Server key"
		echo
		./build-key-server server

		# Diffie-Hellman parameters, necessary for the server end of a SSL/TLS connection
		./build-dh

		# help block DoS attacks and UDP port flooding.
		echo "Generating an 'HMAC firewall'"
		openvpn --genkey --secret keys/ta.key
	else
		echo "'server_ck': whoops, wrong dir, exit"
		exit 1
	fi
}

client_ck() {
	if [ -d "keys" ]; then
		echo
		echo "Client public key"
		echo
		./build-key public
	else
		echo "'server_ck': whoops, wrong dir, exit"
		exit 1
	fi
}

build_ca() {
	if [ $1 ]; then
		CA_DIR=$1

		check_dir $CA_DIR

		echo "Creating a new directory and prepares it to be used as a (CA) key management directory"
		make-cadir $CA_DIR
		cd $CA_DIR
	
		echo "Applying variables"
		cp ../vars vars
		source vars > /dev/null

		echo "Cleaning 'keys' dir"
		./clean-all

		echo
		echo "Building root certificate authority (CA) certificate/key for '$1'"
		echo
		./build-ca
		
		if [ "$1" = "server" ]; then
			server_ck
		elif [ "$1" = "client" ]; then
			client_ck
		fi

		cd ..
	else
		echo "'build_ca' should have argument, exit"
		exit 1
	fi
}

build_ca server
build_ca client

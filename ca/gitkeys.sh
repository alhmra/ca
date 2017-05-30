#!/bin/bash

set -e
cd $(dirname $0)

SUBMODULE_DIR="keys"

cpk() {
	DIR="$SUBMODULE_DIR/$1"

	if [ -d "$DIR" ]; then
		read -p "The '$DIR' dir already exists. Do you wish to remove? [y/n]: " RESP
		if [[ $RESP =~ ^(y|Y|yes|Yes|n|N|no|No)$ ]]; then
			if [[ $RESP =~ ^(y|Y|yes|Yes)$ ]]; then
				rm -rf $DIR
			else
				echo "Exit"
				exit 1
			fi
		else
			echo "Incorrent response."
			exit 1
		fi
	fi

	cp -r $1/keys $DIR
	echo "'$DIR' copied"
}

git submodule init
git submodule update

cpk server
cpk client

cd keys

git add --all .
git commit -m "Update keys $(date)"
git push origin master

#!/bin/bash

set -e
cd $(dirname $0)

source ../config.sh

if [ $1 ]; then
	if [ $1 == "init" ]; then
		echo "Initializing submodule.."

		git submodule init
		git submodule update
	elif [ $1 == "update" ]; then
		echo "Committing and pushing new (ca/cert/key)s"

		cd "$AM_ROOT/$AM_SUBMODULE"
		
		git add --all .
		git commit -m "New (ca/cert/key)s $(date)"
		git push
	fi
else
	echo 'No argument'
	exit 1
fi

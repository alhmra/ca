#!/bin/bash
set -e

command_exists() {
	command -v "$@" > /dev/null 2>&1
}

to_lowercase() {
	echo $1 | tr '[:upper:]' '[:lower:]'
}

is_installed() {
	dpkg-query --show --showformat='${db:Status-Status}' $1 > /dev/null 2>&1
}

do_install() {
	if command_exists lsb_release; then
		dist=$(lsb_release -si)
		dist=$(to_lowercase $dist)

		if [ $dist != "ubuntu" ]; then
			echo "Whoops! Seems like it's not Ubuntu."
			exit 1
		fi

			user=$(id -un 2>/dev/null || true)

			if [ $user != "root" ]; then
				echo "This installer needs the ability to run commands as root."
				exit 1
			fi

			packages=("openvpn" "easy-rsa" "whois" "python3")
			did_apt_get_update=

			for pkg in "${packages[@]}"; do
				if ! is_installed $pkg; then
					if [ $pkg == "openvpn" ]; then
						codename=$(lsb_release -sc)
						codename=$(to_lowercase $codename)

						wget -O - https://swupdate.openvpn.net/repos/repo-public.gpg|apt-key add -
						echo "deb https://build.openvpn.net/debian/openvpn/release/2.4 $codename main" > /etc/apt/sources.list.d/openvpn-aptrepo.list

						apt-get update

						did_apt_get_update=1
					fi

					if [ -z $did_apt_get_update ]; then
						apt-get update
						did_apt_get_update=1
					fi

					apt-get install $pkg
				fi
			done
	fi
}

do_setup() {
	git submodule init
	git submodule update

	source config.sh

	cp -rf $AM_SUBMODULE/. /etc/openvpn/keys/

	servers=("ukraine" "russia")
	for srv in "${servers[@]}"; do
		export AM_SERVER=$srv

		python3 generators/server.py
		python3 generators/client.py
		python3 scripts/iptables.py
	done

	bash scripts/sysctl.sh
}

main() {
	do_install
	do_setup
}

main

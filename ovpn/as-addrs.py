import os, ipaddress

ASN_LIST_FILE = "asn-list.txt"

def build_list_from_file(file):
	list = []

	for line in open(file, "r"):
		if not line.startswith(("#", "\n")):
			list.append(line.rstrip())
	
	return list

def get_nets(asn_list):
	as_nets = []

	for asn in asn_list:
		whois = os.popen("whois -h whois.radb.net -- '-i origin AS" + asn + "' | grep -Eo '([0-9.]+){4}/[0-9]+' | head").read()

		as_nets.extend(whois.split())

	return as_nets

def collapse_nets(nets):
	list = [ipaddress.IPv4Network(addr) for addr in nets]
	collapsed = ipaddress.collapse_addresses(list)

	count = 0
	for addr in collapsed:
		# Nets
		# print(addr)

		# Ranges
		# print(addr.with_netmask.replace('/', ' '))
		count += 1

	print("Networks before collapsing:", len(list))
	print("Networks after collapsing:", count)

def main():
	list = build_list_from_file(ASN_LIST_FILE)
	nets = get_nets(list)
	collapse_nets(nets)

main()

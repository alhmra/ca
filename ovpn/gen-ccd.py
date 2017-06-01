import os, ipaddress

ASN_LIST_FILE = "asn-list.txt"
DNS_LIST_FILE = "dns-list.txt"
CCD_FILE = "ccd/DEFAULT"

def build_list_from_file(file):
	list = []

	for line in open(file, 'r'):
		if not line.startswith(('#', '\n', '\r\n')):
			asn = line.rstrip()
			list.append(asn)
	
	return list

def get_nets(asn_list):
	as_nets = []

	for asn in asn_list:
		whois = os.popen('whois -h whois.radb.net -- "-i origin AS' + asn + '" | grep -Eo "([0-9.]+){4}/[0-9]+" | head').read()

		as_nets.extend(whois.split())

	return as_nets

def collapse_nets(nets):
	list = [ipaddress.IPv4Network(addr) for addr in nets]
	collapsed = ipaddress.collapse_addresses(list)

	count = 0
	ranges = []
	for addr in collapsed:
		# Nets
		# print(addr)

		# Ranges
		ranges.append(addr.with_netmask.replace('/', ' '))
		count += 1

	print('Networks before collapsing:', len(list))
	print('Networks after collapsing:', count)

	return ranges

def ccd(file, list, nets):
	rewrite = open(file, 'w')
	append = open(file, 'a')
	
	for line in open(list, 'r'):
		if not line.startswith(('#', '\n', '\r\n')):
			ip = line.rstrip()
			print('push "dhcp-option DNS ' + ip + '"\npush "route ' + ip + '"', file=rewrite)
	
	for net in nets:
		print('push "route ' + net + '"', file=append)

def main():
	list = build_list_from_file(ASN_LIST_FILE)
	nets = get_nets(list)
	collapsed = collapse_nets(nets)
	ccd(CCD_FILE, DNS_LIST_FILE, collapsed)

main()

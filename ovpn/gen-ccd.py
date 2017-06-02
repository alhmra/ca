import os, ipaddress

ASN_LIST_FILE = "asn-list.txt"
DNS_LIST_FILE = "dns-list.txt"
CCD_DIR = "ccd"

def build_list_from_file(file):
	print('Building list from', file)

	list = []

	for line in open(file, 'r'):
		if not line.startswith(('#', '\n', '\r\n')):
			list.append(line.rstrip())
	
	return list

def get_nets(asn_list):
	print('Getting AS\'s nets..')

	as_nets = []

	for asn in asn_list:
		whois = os.popen('whois -h whois.radb.net -- "-i origin AS' + asn + '" | grep -Eo "([0-9.]+){4}/[0-9]+" | head').read()

		as_nets.extend(whois.split())

		print('ASN:', asn)

	return as_nets

def collapse_nets(nets):
	print('Collapsing nets..')

	list = [ipaddress.IPv4Network(addr) for addr in nets]
	collapsed = ipaddress.collapse_addresses(list)
	
	ranges = []

	for addr in collapsed:
		# Nets
		# print(addr)

		# Ranges
		ranges.append(addr.with_netmask.replace('/', ' '))

	print('Networks before collapsing: %d, after collapsing: %d' % (
		len(list),
		len(ranges)
	))

	return ranges

def gen_ccd(directory, dns_list, net_list):
	print('Generating `ccd`')

	if not os.path.exists(directory):
		print('Directory `%s` does not exists, creating new one..' % directory)

		os.makedirs(directory)

	target = open(directory + "/DEFAULT", 'w')

	for dns in dns_list:
		print(
			'push "dhcp-option DNS %s"' % dns,
			'push "route %s"' % dns,
			sep="\n",
			file=target
		)

	for net in net_list:
		print(
			'push "route %s"' % net,
			file=target
		)

def main():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	
	asn_list = build_list_from_file(ASN_LIST_FILE)
	dns_list = build_list_from_file(DNS_LIST_FILE)

	nets = get_nets(asn_list)
	collapsed = collapse_nets(nets)

	gen_ccd(CCD_DIR, dns_list, collapsed)

	print('Success!')

main()

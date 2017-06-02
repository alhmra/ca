import os, sys, ipaddress

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

sys.path.append('../utility')
from util import list_from_json

CCD_DATA = "ccd.json"
CCD_OUT_DIR = "ccd"

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
	print('Generating `ccd` configuration')

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
	asn_list = list_from_json(CCD_DATA, 'asn')
	nets = get_nets(asn_list)
	collapsed = collapse_nets(nets)

	dns_list = list_from_json(CCD_DATA, 'dns')

	gen_ccd(CCD_OUT_DIR, dns_list, collapsed)

	print('Success!')


main()

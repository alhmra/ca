import os, sys, json, ipaddress
from distutils.dir_util import copy_tree

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def gen_conf():
	print('- Generating server conf..')

	sc = open('../json/server.json', 'r')
	sc = json.loads(sc.read())

	ki = open('../json/keys.json', 'r')
	ki = json.loads(ki.read())
	
	target_f = '/etc/openvpn/server.conf'
	target = open(target_f, 'w')
	
	for key in sc:
		val = sc[key]

		if key in ['ca', 'cert', 'key', 'tls-auth', 'dh']:
			print('{} keys/{}/{}.{}'.format(
				key,
				val,
				ki[key]['server'].format(os.environ["KEY_SIZE"]),
				ki[key]['ext']
			), file=target)
		elif val:
			print(key, val, file=target)
		else:
			print(key, file=target)
	
	print('\tSaved in', target_f, '\n')

def gen_ccd():
	print('- Generating ccd routes..')

	ccd_dir = '/etc/openvpn/ccd'
	target_f = ccd_dir + '/DEFAULT'
	target = open(target_f, 'w')

	if not os.path.exists(ccd_dir):
		print('-- Directory `{}` does not exists, creating new one..'.format(ccd_dir))

		os.makedirs(ccd_dir)

	def keyd_to_list(f):
		smth = open('../json/' + f + '.json', 'r')
		smth = json.loads(smth.read())
		smth_list = []

		for arr in smth:
			smth_list.extend(smth[arr])
		
		return smth_list

	dns_list = keyd_to_list('dns')

	for addr in dns_list:
		print(
			'push "dhcp-option DNS %s"' % addr,
			'push "route %s"' % addr,
			sep="\n",
			file=target
		)
	
	print('-- Getting AS\'s nets..')

	asn_list = keyd_to_list('asn')
	as_nets = []

	for asn in asn_list:
		whois = os.popen('whois -h whois.radb.net -- "-i origin AS' + asn + '" | grep -Eo "([0-9.]+){4}/[0-9]+"').read()

		as_nets.extend(whois.split())

	print('-- Collapsing nets..')

	ip4 = [ipaddress.IPv4Network(addr) for addr in as_nets]
	ip4_collapsed = ipaddress.collapse_addresses(ip4)
	
	count = 0
	for addr in ip4_collapsed:
		ip4_range = addr.with_netmask.replace('/', ' ')

		print('push "route {}"'.format(ip4_range), file=target)

		count += 1

	print('-- Networks before collapsing: {}, after collapsing: {}'.format(len(as_nets), count))

	print('\tSaved in', target_f)

def main():
	if not os.environ["KEY_SIZE"]:
		quit()

	gen_conf()
	gen_ccd()

main()

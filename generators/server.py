import os, sys, json, ipaddress

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

			if key == 'tls-auth':
				print('key-direction 0', file=target)
		elif val:
			print(key, val, file=target)
		else:
			print(key, file=target)
	
	print('\tSaved in', target_f)

def gen_routes():
	print('- Generating ccd routes..')

	ccd_dir = '/etc/openvpn/ccd'
	
	if not os.path.exists(ccd_dir):
		print('-- Directory `{}` does not exists, creating new one..'.format(ccd_dir))

		os.makedirs(ccd_dir)
	
	target_f = ccd_dir + '/DEFAULT'
	target = open(target_f, 'w')

	def keyd_to_list(f):
		content = json.loads(open('../json/' + f + '.json', 'r').read())
		list = []

		for arr in content:
			list.extend(content[arr])
		
		return list

	for addr in keyd_to_list('dns'):
		print(
			'push "dhcp-option DNS %s"' % addr,
			'push "route %s"' % addr,
			sep="\n",
			file=target
		)
	
	print('-- Getting AS\'s nets..')

	as_nets = []

	for asn in keyd_to_list('asn'):
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
	if not os.environ['AM_ROOT']:
		quit()

	gen_conf()
	gen_routes()

main()

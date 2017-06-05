import os, json, re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def gen_conf():
	print('- Generating client conf..')

	cc = open('../json/client.json', 'r')
	cc = json.loads(cc.read())

	sc = open('../json/server.json', 'r')
	sc = json.loads(sc.read())

	ki = open('../json/keys.json', 'r')
	ki = json.loads(ki.read())

	key_dir = os.environ['KEY_DIR']

	target_f = '../alohomora.ovpn'
	target = open(target_f, 'w')

	for key in cc:
		val = cc[key]

		if sc.get(key):
			if key in ['ca', 'cert', 'key', 'tls-auth']:
				source = '{}{}/{}.{}'.format(key_dir, val, ki[key]['client'], ki[key]['ext'])
				content = open(source, 'r').read()

				insert = re.search(r'(?s)-{5}BEGIN.*-{5}.*?-{5}END.*-{5}', content)
				insert = insert.group(0)

				print('<{}>\n{}\n</{}>'.format(key, insert, key), file=target)

				if key == 'tls-auth':
					print('key-direction 1', file=target)
			else:
				print(key, sc[key], file=target)
		else:
			if key == 'remote':
				addr = os.environ['AM_VPN']
				port = sc['port']

				if port == 1194:
					print(key, addr, file=target)
				else:
					print(key, addr, port, file=target)
			else:
				print(key, file=target)
	
	print('\tSaved in', target_f)

def main():
	if not os.environ['AM_ROOT']:
		quit()
	
	gen_conf()

main()

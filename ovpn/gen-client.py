import os, sys, re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

sys.path.append('../utility')
from util import cdir, parse_conf, list_from_json

DATA = 'data.json'

SRV_CONF = 'server.conf'
SRV_ADDR = 'public-vpn.alohomora.xyz'

KEY_DIR = '../server'

OUT_DIR = 'ccd'

def gen_client(conf, params, client):
	if client:
		cdir(OUT_DIR)

		target = OUT_DIR + '/' + client + '.ovpn'
		target = open(target, 'w')

		for item in params:
			if item in conf:
				val = conf[item]

				if val:
					if item == 'port':
						if val != '1194':
							print('remote', SRV_ADDR, val, file=target)
						else:
							print('remote', SRV_ADDR, file=target)
					elif item in ['ca', 'cert', 'key', 'tls-auth']:
						path = ''
						
						if item == 'ca':
							path = 'keys/server/ca.crt'
						elif item == 'cert':
							path = 'keys/client/' + client + '.crt'
						elif item == 'key':
							path = 'keys/client/' + client + '.key'
						else:
							path = 'keys/server/ta.key'

						if item == 'tls-auth':
							print('key-direction 1', file=target)

						with open(KEY_DIR + '/' + path, 'r') as content:
							content = content.read()
							
							result = re.search(r'(?s)-{5}BEGIN.*-{5}.*?-{5}END.*-{5}', content)
							result = result.group(0)

							print('<%s>\n%s\n</%s>' % (item, result, item), file=target)
					else:
						print(item, val, file=target)
				else:
					print(item, file=target)
			else:
				print(item, file=target)

def main():
	server_conf = parse_conf(SRV_CONF)
	client = sys.argv[1]
	params = list_from_json(DATA, 'client_config_params')

	gen_client(server_conf, params, client)

	print('Success!')

main()

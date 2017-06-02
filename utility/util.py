import json, os

def cdir(directory):
	if not os.path.exists(directory):
		print('Directory `%s` does not exists, creating new one..' % directory)

		os.makedirs(directory)

def list_from_json(file, of):
	print('Building list of %s from %s' % (of.upper(), file))
	data = json.loads(open(file, 'r').read())
	data = data[of.lower()]
	
	if isinstance(data, list):
		return data
	else:
		res = []
		for thing in data:
			res.extend(data[thing])

		return res

def list_from_txt(file):
	print('Building list from file:', file)

	list = []

	for line in open(file, 'r'):
		if not line.startswith(('#', '\n', '\r\n')):
			list.append(line.rstrip())
	
	return list

def parse_conf(conf):
	conf = os.popen('grep -o "^[^#]*" ' + conf).read()
	conf = conf.split('\n')
	pairs = {}

	for line in conf:
		if line:
			key, val = line.rstrip().partition(' ')[::2]

			pairs[key] = val

	return pairs

import json

def list_from_json(file, of):
	print('Building list of %s from %s' % (of.upper(), file))
	data = json.loads(open(file, 'r').read())
	data = data[of.lower()]
	list = []

	for thing in data:
		list.extend(data[thing])

	return list

def list_from_txt(file):
	print('Building list from file:', file)

	list = []

	for line in open(file, 'r'):
		if not line.startswith(('#', '\n', '\r\n')):
			list.append(line.rstrip())
	
	return list

import os, json, ipaddress

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

sc = open('../json/server.json', 'r')
sc = json.loads(sc.read())

# https://docs.python.org/3/library/ipaddress.html#network-objects
addr_netmask = sc['server'].replace(' ', '/')
network = ipaddress.IPv4Network(addr_netmask)

os.popen('iptables -t nat -A POSTROUTING -s {} -o eth0 -j MASQUERADE'.format(network))

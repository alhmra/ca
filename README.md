# Alohomora Core

```bash
git clone
cd alohomora
sudo bash install.sh
```

## Scripts and files

###### generators/server.py
Generates server configuration and routes for DNS's in `json/dns.json` and AS's, that has been blocked by ISPs in Ukraine - `json/asn.json` according to [decree](http://www.president.gov.ua/documents/1332017-21850) of the Ukrainian president.
ASNs collected manualy at [bgp.he.net](http://bgp.he.net/).

###### generators/client.py
Generates client configuration.

### Keys submodule

> Sign server certificates with one CA and client certificates with a different CA. The client config "ca" directive should reference the server-signing CA while the server config "ca" directive should reference the client-signing CA.

```bash
.
├── client
│   └── keys
│       ├── ca.crt
│       ├── public.crt
│       └── public.key
└── server
    └── keys
        ├── ca.crt
        ├── dh{}.pem
        ├── server.crt
        ├── server.key
        └── ta.key
```

### So far, everything is so.

---

- [OpenVPN apt repos](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos)
- [Easy-rsa docs](https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html)

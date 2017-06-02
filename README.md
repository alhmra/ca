# Alohomora Core

## Scripts and files

##### `ca/issue.sh`
Builds own ca for server and client, for each it's own, builds Diffie-Hellman parameters and issues a server key, and public client key since `duplicate-cn` is enabled in `ovpn/server.conf`.

> Sign server certificates with one CA and client certificates with a different CA. The client config "ca" directive should reference the server-signing CA while the server config "ca" directive should reference the client-signing CA.

Below, here is what we get

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
        ├── dh1024.pem
        ├── server.crt
        ├── server.key
        └── ta.key
```

##### `ovpn/gen-ccd.py`
Generates `ovpn/ccd/DEFAULT` out of data in `ovpn/ccd.json`.

##### `ovpn/data.json`
Contains DNS servers, and ASNs that was blocked by ISPs in Ukraine according to [decree](http://www.president.gov.ua/documents/1332017-21850) of the Ukrainian president.
ASNs collected manualy at [bgp.he.net](http://bgp.he.net/).

##### `ovpn/gen-client.py`
Generates client config, `.ovpn` file, considering server config (`server.conf`), required params are in `ovpn/data.json`.

##### `pack-server.sh`
This thing takes configuration, keys, other stuff, and pushes it to `server` submodule that is a private repo.

### So far, everything is so.

---

Some things has leaked from [this article](https://habrahabr.ru/post/329248/).

---

- [OpenVPN apt repos](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos)
- [Easy-rsa docs](https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html)

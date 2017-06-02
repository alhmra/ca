# Alohomora Core

##### `ca/issue.sh`
Builds own ca for server and client, for each it's own, builds Diffie-Hellman parameters and issues a server key, and public client key since `duplicate-cn` is enabled in `ovpn/server.conf`.
> Sign server certificates with one CA and client certificates with a different CA. The client config "ca" directive should reference the server-signing CA while the server config "ca" directive should reference the client-signing CA.

```bash
# Thats what we get by running `./ca/issue.sh`
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
Generates `ovpn/ccd/DEFAULT` out of data in `ovpn/ccd.json` that contains DNS servers and ASNs that was blocked by ISPs in Ukraine according to [decree](http://www.president.gov.ua/documents/1332017-21850) of the Ukrainian president.

##### `ovpn/gen-client.sh`
Generates client config (`.ovpn` file) considering server config (`server.conf`).

##### `pack-server.sh`
This thing takes configuration, keys, other stuff, and pushes it to `server` submodule that is a private repo.

### So far, everything is so.

---

- [OpenVPN apt repos](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos)
- [Easy-rsa docs](https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html)

# ca
Alohomora Core

---

**`build-ca.sh`** implements the following:
> Sign server certificates with one CA and client certificates with a different CA.

The client config "ca" directive should reference the server-signing CA while the server config "ca" directive should reference the client-signing CA.

```bash
.
├── client
│   └── keys           <────┐
│       ├── ca.crt      ><┐ │
│       ├── public.crt    │ │
│       └── public.key    │ │
└── server                │ │
    └── keys              │ │
        ├── ca.crt      ><┘ │
        ├── dh1024.pem      │
        ├── server.crt      │
        ├── server.key      │
        └── ta.key       >──┘
```

---

- [OpenVPN apt repos](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos)
- [Easy-rsa docs](https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html)

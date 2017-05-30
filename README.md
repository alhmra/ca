# Alohomora Core

Before using `ca/build-ca.sh`, make sure that `openvpn` and `easy-rsa` are installed

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

> Sign server certificates with one CA and client certificates with a different CA.
The client config "ca" directive should reference the server-signing CA while the server config "ca" directive should reference the client-signing CA.

---

- [OpenVPN apt repos](https://community.openvpn.net/openvpn/wiki/OpenvpnSoftwareRepos)
- [Easy-rsa docs](https://openvpn.net/index.php/open-source/documentation/miscellaneous/77-rsa-key-management.html)

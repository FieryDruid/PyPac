# PyPac
This is a instrument for configuration PAC-script domains from browser.

The main script was taken from the shadowsocks repository: https://github.com/shadowsocks/shadowsocks-windows

PyPac is a service for configuration USERRULES section of this script file. And setup windows configuration for it.

**Proxy settings is will be automatically reset after all rule changes, just wait some time or restart your applications**

## Settings
Change settings in `settings.env` file.

* `PROXY_DOMAIN` - domain for your proxy/vpn/etc. server. Default - local machine
* `PROXY_PORT` - domain for your proxy/vpn/etc. server.
* `LOG_LEVEL` - logging level
* `PORT` - port for `PyPac` server.'

## Domains configuration
In version `0.0.1` you can configure domains list in browser. Just open `http://localhost:{PORT}/docs` (with defaults: http://localhost:8080/docs).

### Add new rule:
1. Open `Set rule` (`POST`)
2. Click on `Try it out` button 
3. Write your rule into input field
4. Click on `Execute`
5. If you see integer rule identifier in response - it works!

### Remove rule:
1. Open `Remove rule` (`DELETE`)
2. Click on `Try it out` button 
3. Write your rule into input field
4. Click on `Execute`

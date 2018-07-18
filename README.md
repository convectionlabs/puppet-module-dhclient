# puppet-module-dhclient

Manages the DHCP Client for AWS instances (Route53 DNS)

## Requirements
---

- Puppet version 3 or greater with Hiera support
- Puppet Modules:

| OS Family      | Module |
| :------------- |:-------------: |
| ALL            | [clabs/core](https://bitbucket.org/convectionlabs/puppet-module-core)|

## Usage
---

Loading the dhclient class:

```puppet
include dhclient
```

## Configuration
---

All configuration settings should be defined using Hiera.

### Example

```yaml
dhclient::interface:    'eth0'
dhclient::searchpath:
    - "%{::domain}"
    - "sub1.%{::domain}"
    - "sub2.%{::domain}"
```

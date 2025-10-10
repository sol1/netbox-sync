# Netbox Configuration

Controls the connection parameters to your netBox instance
    

## `api_token`
**Type:** `str`  
**Required:** `true`  
**Example:** `XYZ`

Requires an NetBox API token with full permissions on all objects except 'auth', 'secrets'
and 'users'

## `host_fqdn`
**Type:** `str`  
**Required:** `true`  
**Example:** `netbox.example.com`

Requires a hostname or IP which points to your NetBox instance

## `port`
**Type:** `int`  
**Default:** `443`

Define the port your NetBox instance is listening on. If 'disable_tls' is set to "true"
this option might be set to 80

## `disable_tls`
**Type:** `bool`  
**Default:** `False`

Whether TLS encryption is enabled or disabled

## `validate_tls_certs`
**Type:** `bool`  
**Default:** `True`

Enforces TLS certificate validation. If this system doesn't trust the NetBox web server
certificate then this option needs to be changed

## `proxy`
**Type:** `str`  
**Default:** `None`  
**Example:** `http://example.com:3128`

Defines a proxy which will be used to connect to NetBox. Proxy setting needs to include
the schema. Proxy basic auth example: http://user:pass@10.10.1.10:312

## `client_cert`
**Type:** `str`  
**Default:** `None`  
**Example:** `client.pem`

Specify a client certificate which can be used to authenticate to NetBox

## `client_cert_key`
**Type:** `str`  
**Default:** `None`  
**Example:** `client.key`

Specify the client certificate private key belonging to the client cert

## `prune_enabled`
**Type:** `bool`  
**Default:** `False`

Whether items which were created by this program but can't be found in any source anymore
will be deleted or not

## `prune_delay_in_days`
**Type:** `int`  
**Default:** `30`

Orphaned objects will first be tagged before they get deleted. Once the amount of days
passed the object will actually be deleted

## `ignore_unknown_source_object_pruning`
**Type:** `bool`  
**Default:** `False`

This will tell netbox-sync to ignore objects in NetBox with tag 'NetBox-synced' from
pruning if the source is not defined in this config file (https://github.com/bb-
Ricardo/netbox-sync/issues/176)

## `default_netbox_result_limit`
**Type:** `int`  
**Default:** `200`

The maximum number of objects returned in a single request. If a NetBox instance is very
quick responding the value should be raised

## `timeout`
**Type:** `int`  
**Default:** `30`

The maximum time a query is allowed to execute before being killed and considered failed

## `max_retry_attempts`
**Type:** `int`  
**Default:** `4`

The amount of times a failed request will be reissued. Once the maximum is reached the
syncing process will be stopped completely.

## `use_caching`
**Type:** `bool`  
**Default:** `True`

Defines if caching of NetBox objects is used or not. If problems with unresolved
dependencies occur, switching off caching might help.

## `cache_directory_location`
**Type:** `str`  
**Default:** `cache`

The location of the directory where the cache files should be stored

## Example (YAML)

```

netbox:
  # api_token: "XYZ"  # required
  # host_fqdn: "netbox.example.com"  # required
  port: 443
  disable_tls: false
  validate_tls_certs: true
  # proxy: "http://example.com:3128"  # optional
  # client_cert: "client.pem"  # optional
  # client_cert_key: "client.key"  # optional
  prune_enabled: false
  prune_delay_in_days: 30
  ignore_unknown_source_object_pruning: false
  default_netbox_result_limit: 200
  timeout: 30
  max_retry_attempts: 4
  use_caching: true
  cache_directory_location: "cache"
```

## Example (INI)

```

[netbox]
# api_token = XYZ  ; required
# host_fqdn = netbox.example.com  ; required
port = 443
disable_tls = false
validate_tls_certs = true
# proxy = http://example.com:3128  ; optional
# client_cert = client.pem  ; optional
# client_cert_key = client.key  ; optional
prune_enabled = false
prune_delay_in_days = 30
ignore_unknown_source_object_pruning = false
default_netbox_result_limit = 200
timeout = 30
max_retry_attempts = 4
use_caching = true
cache_directory_location = cache
```

---

# Source Redfish Configuration

Base class to parse config data

## `enabled`
**Type:** `bool`  
**Default:** `True`

Defines if this source is enabled or not

## `type`
**Type:** `str`  
**Required:** `true`  
**Example:** `check_redfish`

type of source. This defines which source handler to use

## `inventory_file_path`
**Type:** `str`  
**Required:** `true`  
**Example:** `/full/path/to/inventory/files`

define the full path where the check_redfish inventory json files are located

## `permitted_subnets`
**Type:** `str`  
**Default:** `None`  
**Example:** `172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24`

IP networks eligible to be synced to NetBox. If an IP address is not part of this networks
then it WON'T be synced to NetBox. To excluded small blocks from bigger IP blocks a
leading '!' has to be added

## `overwrite_host_name`
**Type:** `bool`  
**Default:** `False`

define if the host name discovered via check_redfish overwrites the device host name in
NetBox

## `overwrite_power_supply_name`
**Type:** `bool`  
**Default:** `False`

define if the name of the power supply discovered via check_redfish overwrites the power
supply name in NetBox

## `overwrite_power_supply_attributes`
**Type:** `bool`  
**Default:** `True`

define if existing power supply attributes are overwritten with data discovered via
check_redfish if False only data which is not preset in NetBox will be added

## `overwrite_interface_name`
**Type:** `bool`  
**Default:** `False`

define if the name of the interface discovered via check_redfish overwrites the interface
name in NetBox

## `overwrite_interface_attributes`
**Type:** `bool`  
**Default:** `False`

define if existing interface attributes are overwritten with data discovered via
check_redfish if False only data which is not preset in NetBox will be added

## `ip_tenant_inheritance_order`
**Type:** `str`  
**Default:** `device, prefix`

define in which order the IP address tenant will be assigned if tenant is undefined.
possible values:
  * device : host or VM tenant will be assigned to the IP address
  * prefix : if the IP address belongs to an existing prefix and this prefix has a tenant assigned, then this one is used
  * disabled : no tenant assignment to the IP address will be performed
the order of the definition is important, the default is "device, prefix" which means:
If the device has a tenant then this one will be used. If not, the prefix tenant will be used if defined

## Example (YAML)

```

source:
  enabled: true
  # type: "check_redfish"  # required
  # inventory_file_path: "/full/path/to/inventory/files"  # required
  # permitted_subnets: "172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24"  # optional
  overwrite_host_name: false
  overwrite_power_supply_name: false
  overwrite_power_supply_attributes: true
  overwrite_interface_name: false
  overwrite_interface_attributes: false
  ip_tenant_inheritance_order: "device, prefix"
```

## Example (INI)

```

[source]
enabled = true
# type = check_redfish  ; required
# inventory_file_path = /full/path/to/inventory/files  ; required
# permitted_subnets = 172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24  ; optional
overwrite_host_name = false
overwrite_power_supply_name = false
overwrite_power_supply_attributes = true
overwrite_interface_name = false
overwrite_interface_attributes = false
ip_tenant_inheritance_order = device, prefix
```

---

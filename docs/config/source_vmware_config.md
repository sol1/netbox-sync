# Source VMWare Configuration

Base class to parse config data

## TOC

[Option: enabled](#enabled)
[Option: type](#type)
[Option: host_fqdn](#host_fqdn)
[Option: port](#port)
[Option: username](#username)
[Option: password](#password)
[Option: validate_tls_certs](#validate_tls_certs)
[Option: proxy_host](#proxy_host)
[Option: proxy_port](#proxy_port)
[Option: permitted_subnets](#permitted_subnets)
[Option: cluster_exclude_filter](#cluster_exclude_filter)
[Option: cluster_include_filter](#cluster_include_filter)
[Option: host_exclude_filter](#host_exclude_filter)
[Option: host_include_filter](#host_include_filter)
[Option: vm_exclude_filter](#vm_exclude_filter)
[Option: vm_include_filter](#vm_include_filter)
[Option: vm_exclude_by_tag_filter](#vm_exclude_by_tag_filter)
[Option: cluster_site_relation](#cluster_site_relation)
[Option: host_site_relation](#host_site_relation)
[Option: cluster_scope_type_relation](#cluster_scope_type_relation)
[Option: cluster_scope_id_relation](#cluster_scope_id_relation)
[Option: cluster_tenant_relation](#cluster_tenant_relation)
[Option: host_tenant_relation](#host_tenant_relation)
[Option: vm_tenant_relation](#vm_tenant_relation)
[Option: host_platform_relation](#host_platform_relation)
[Option: vm_platform_relation](#vm_platform_relation)
[Option: host_role_relation](#host_role_relation)
[Option: vm_role_relation](#vm_role_relation)
[Option: cluster_tag_relation](#cluster_tag_relation)
[Option: host_tag_relation](#host_tag_relation)
[Option: vm_tag_relation](#vm_tag_relation)
[Option: match_host_by_serial](#match_host_by_serial)
[Option: match_on_mac_address](#match_on_mac_address)
[Option: match_on_ip_address](#match_on_ip_address)
[Option: collect_hardware_asset_tag](#collect_hardware_asset_tag)
[Option: collect_hardware_serial](#collect_hardware_serial)
[Option: dns_name_lookup](#dns_name_lookup)
[Option: custom_dns_servers](#custom_dns_servers)
[Option: set_primary_ip](#set_primary_ip)
[Option: skip_vm_comments](#skip_vm_comments)
[Option: skip_vm_templates](#skip_vm_templates)
[Option: skip_offline_vms](#skip_offline_vms)
[Option: skip_srm_placeholder_vms](#skip_srm_placeholder_vms)
[Option: strip_host_domain_name](#strip_host_domain_name)
[Option: strip_vm_domain_name](#strip_vm_domain_name)
[Option: cluster_tag_source](#cluster_tag_source)
[Option: host_tag_source](#host_tag_source)
[Option: vm_tag_source](#vm_tag_source)
[Option: sync_custom_attributes](#sync_custom_attributes)
[Option: host_custom_object_attributes](#host_custom_object_attributes)
[Option: vm_custom_object_attributes](#vm_custom_object_attributes)
[Option: set_source_name_as_cluster_group](#set_source_name_as_cluster_group)
[Option: sync_vm_dummy_interfaces](#sync_vm_dummy_interfaces)
[Option: disable_vlan_sync](#disable_vlan_sync)
[Option: vlan_sync_exclude_by_name](#vlan_sync_exclude_by_name)
[Option: vlan_sync_exclude_by_id](#vlan_sync_exclude_by_id)
[Option: vlan_group_relation_by_name](#vlan_group_relation_by_name)
[Option: vlan_group_relation_by_id](#vlan_group_relation_by_id)
[Option: track_vm_host](#track_vm_host)
[Option: overwrite_device_interface_name](#overwrite_device_interface_name)
[Option: overwrite_vm_interface_name](#overwrite_vm_interface_name)
[Option: overwrite_device_platform](#overwrite_device_platform)
[Option: overwrite_vm_platform](#overwrite_vm_platform)
[Option: host_management_interface_match](#host_management_interface_match)
[Option: ip_tenant_inheritance_order](#ip_tenant_inheritance_order)
[Option: sync_vm_interface_mtu](#sync_vm_interface_mtu)
[Option: host_nic_exclude_by_mac_list](#host_nic_exclude_by_mac_list)
[Option: custom_attribute_exclude](#custom_attribute_exclude)
[Option: vm_disk_and_ram_in_decimal](#vm_disk_and_ram_in_decimal)
[Option: netbox_host_device_role](#netbox_host_device_role)
[Option: netbox_vm_device_role](#netbox_vm_device_role)
[Option: sync_tags](#sync_tags)
[Option: sync_parent_tags](#sync_parent_tags)
[Example (YAML)](#example-yaml)
[Example (INI)](#example-ini)

## Configuration Options
### `enabled`
**Type:** `bool`  
**Default:** `True`

Defines if this source is enabled or not

### `type`
**Type:** `str`  
**Required:** `true`  
**Example:** `vmware`

type of source. This defines which source handler to use

### `host_fqdn`
**Type:** `str`  
**Required:** `true`  
**Example:** `vcenter.example.com`

host name / IP address of the vCenter

### `port`
**Type:** `int`  
**Default:** `443`

TCP port to connect to

### `username`
**Type:** `str`  
**Required:** `true`  
**Example:** `vcenter-readonly`

username to use to log into vCenter

### `password`
**Type:** `str`  
**Required:** `true`  
**Example:** `super-secret`

password to use to log into vCenter

### `validate_tls_certs`
**Type:** `bool`  
**Default:** `False`

Enforces TLS certificate validation. If vCenter uses a valid TLS certificate then this
option should be set to 'true' to ensure a secure connection.

### `proxy_host`
**Type:** `str`  
**Default:** `None`  
**Example:** `10.10.1.10`

EXPERIMENTAL: Connect to a vCenter using a proxy server (socks proxies are not supported).
define a host name or an IP address

### `proxy_port`
**Type:** `int`  
**Default:** `None`  
**Example:** `3128`

EXPERIMENTAL: Connect to a vCenter using a proxy server (socks proxies are not supported).
define proxy server port number

### `permitted_subnets`
**Type:** `str`  
**Default:** `None`  
**Example:** `172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24`

IP networks eligible to be synced to NetBox. If an IP address is not part of this networks
then it WON'T be synced to NetBox. To excluded small blocks from bigger IP blocks a
leading '!' has to be added

### `cluster_exclude_filter`
**Type:** `str`  
**Default:** `None`

If a cluster is excluded from sync then ALL VMs and HOSTS inside the cluster will be
ignored! a cluster can be specified as "Cluster-name" or "Datacenter-name/Cluster-name" if
multiple clusters have the same name

### `cluster_include_filter`
**Type:** `str`  
**Default:** `None`

### `host_exclude_filter`
**Type:** `str`  
**Default:** `None`

This will only include/exclude the host, not the VM if Host is part of a multi host
cluster

### `host_include_filter`
**Type:** `str`  
**Default:** `None`

### `vm_exclude_filter`
**Type:** `str`  
**Default:** `None`

simply include/exclude VMs

### `vm_include_filter`
**Type:** `str`  
**Default:** `None`

### `vm_exclude_by_tag_filter`
**Type:** `str`  
**Default:** `None`  
**Example:** `tag-a, tag-b`

defines a comma separated list of vCenter tags which (if assigned to a VM) will exclude
this VM from being synced to NetBox. The config option 'vm_tag_source' determines which
tags are collected for VMs.

### `cluster_site_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `Cluster_NYC = New York, Cluster_FFM.* = Frankfurt, Datacenter_TOKIO/.* = Tokio, Cluster_MultiSite = <NONE>`

This option defines which vCenter cluster is part of a NetBox site.
This is done with a comma separated key = value list.
  key: defines the cluster name as regex
  value: defines the NetBox site name (use quotes if name contains commas)
This is a quite important config setting as IP addresses, prefixes, VLANs
and VRFs are site dependent. In order to assign the correct prefix to an IP
address it is important to pick the correct site.
A VM always depends on the cluster site relation
a cluster can be specified as "Cluster-name" or
"Datacenter-name/Cluster-name" if multiple clusters have the same name.
When a vCenter cluster consists of hosts from multiple NetBox sites,
it is possible to leave the site for a NetBox cluster empty. All VMs from
this cluster will then also have no site reference.
The keyword "<NONE>" can be used as a value for this.

### `host_site_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `nyc02.* = New York, ffm01.* = Frankfurt`

Same as cluster site but on host level. If unset it will fall back to
cluster_site_relation

### `cluster_scope_type_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `Cluster_NYC = dcim.site, Cluster_FFM = dcim.sitegroup, Cluster_BER = dcim.location`

This option defines the scope type for a cluster. The scope type can be 'dcim.site',
'dcim.sitegroup', 'dcim.location' or 'dcim.region'. This is done with a comma separated
key = value list. Can be set to "<NONE>" to not assign a scope type. Note: this does not
remove scope types from existing clusters in NetBox. key: defines a cluster name as regex
value: defines the NetBox scope type name (use quotes if name contains commas)

### `cluster_scope_id_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `Cluster_NYC = 1, Cluster_FFM.* = 2, Cluster_BER = 7`

This option defines the scope id for a cluster. The scope id is the NetBox ID of the scope
type. This is done with a comma separated key = value list. To be used in combination with
the 'cluster_scope_type_relation'. key: defines a cluster name as regex value: defines the
NetBox scope id (use quotes if name contains commas)

### `cluster_tenant_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `Cluster_NYC.* = Customer A`

This option defines which cluster/host/VM belongs to which tenant.
This is done with a comma separated key = value list.
  key: defines a hosts/VM name as regex
  value: defines the NetBox tenant name (use quotes if name contains commas)
a cluster can be specified as "Cluster-name" or
"Datacenter-name/Cluster-name" if multiple clusters have the same name

### `host_tenant_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `esxi300.* = Infrastructure`

### `vm_tenant_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `grafana.* = Infrastructure`

### `host_platform_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `VMware ESXi 7.0.3 = VMware ESXi 7.0 Update 3o`

This option defines custom platforms if the VMWare created platforms are not suitable.
Pretty much a mapping of VMWare platform name to your own platform name.
This is done with a comma separated key = value list.
  key: defines a VMWare returned platform name as regex
  value: defines the desired NetBox platform name

### `vm_platform_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `centos-7.* = centos7, microsoft-windows-server-2016.* = Windows2016`

### `host_role_relation`
**Type:** `str`  
**Default:** `.* = Server`

Define the NetBox device role used for hosts. The default is
set to "Server". This is done with a comma separated key = value list.
  key: defines host(s) name as regex
  value: defines the NetBox role name (use quotes if name contains commas)

### `vm_role_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `.* = Server`

Define the NetBox device role used for VMs. This is done with a
comma separated key = value list, same as 'host_role_relation'.
  key: defines VM(s) name as regex
  value: defines the NetBox role name (use quotes if name contains commas)

### `cluster_tag_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `Cluster_NYC.* = Infrastructure`

Define NetBox tags which are assigned to a cluster, host or VM. This is
done with a comma separated key = value list.
  key: defines a hosts/VM name as regex
  value: defines the NetBox tag (use quotes if name contains commas)
a cluster can be specified as "Cluster-name" or
"Datacenter-name/Cluster-name" if multiple clusters have the same name

### `host_tag_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `esxi300.* = Infrastructure`

### `vm_tag_relation`
**Type:** `str`  
**Default:** `None`  
**Example:** `grafana.* = Infrastructure`

### `match_host_by_serial`
**Type:** `bool`  
**Default:** `True`

Try to find existing host based on serial number. This can cause issues with blade centers
if VMWare does not report the blades serial number properly.

### `match_on_mac_address`
**Type:** `bool`  
**Default:** `True`

Try to find existing VM based on the mac address. This can cause issues if VMs have been
renamed and replaced with new VM's of the same name with a new MAC while the old VM still
exists.

### `match_on_ip_address`
**Type:** `bool`  
**Default:** `True`

Try to find existing VM based on the IP address. This can cause issues if VMs have been
renamed and replaced with new VM's of the same name with a new IP while the old VM still
exists.

### `collect_hardware_asset_tag`
**Type:** `bool`  
**Default:** `True`

Attempt to collect asset tags from vCenter hosts

### `collect_hardware_serial`
**Type:** `bool`  
**Default:** `True`

Attempt to collect serials from vCenter hosts

### `dns_name_lookup`
**Type:** `bool`  
**Default:** `True`

Perform a reverse lookup for all collected IP addresses. If a dns name was found it will
be added to the IP address object in NetBox

### `custom_dns_servers`
**Type:** `str`  
**Default:** `None`  
**Example:** `192.168.1.11, 192.168.1.12`

use custom DNS server to do the reverse lookups

### `set_primary_ip`
**Type:** `str`  
**Default:** `when-undefined`

define how the primary IPs should be set
possible values:

  always:     will remove primary IP from the object where this address is
              currently set as primary and moves it to new object

  when-undefined:
              only sets primary IP if undefined, will cause ERRORs if same IP is
              assigned more then once to different hosts and IP is set as the
              objects primary IP

  never:      don't set any primary IPs, will cause the same ERRORs
              as "when-undefined"

### `skip_vm_comments`
**Type:** `bool`  
**Default:** `False`

Do not sync notes from a VM in vCenter to the comments field on a VM in netbox

### `skip_vm_templates`
**Type:** `bool`  
**Default:** `True`

Do not sync template VMs

### `skip_offline_vms`
**Type:** `bool`  
**Default:** `False`

Skip virtual machines which are reported as offline.
ATTENTION: this option will keep purging stopped VMs if activated!

### `skip_srm_placeholder_vms`
**Type:** `bool`  
**Default:** `False`

If the VMware Site Recovery Manager is used to can skip syncing placeholder/replicated VMs
from fail-over site to NetBox.

### `strip_host_domain_name`
**Type:** `bool`  
**Default:** `False`

strip domain part from host name before syncing device to NetBox

### `strip_vm_domain_name`
**Type:** `bool`  
**Default:** `False`

strip domain part from VM name before syncing VM to NetBox

### `cluster_tag_source`
**Type:** `str`  
**Default:** `None`

### `host_tag_source`
**Type:** `str`  
**Default:** `None`

### `vm_tag_source`
**Type:** `str`  
**Default:** `None`

### `sync_custom_attributes`
**Type:** `bool`  
**Default:** `False`

sync custom attributes defined for hosts and VMs in vCenter to NetBox as custom fields

### `host_custom_object_attributes`
**Type:** `str`  
**Default:** `None`  
**Example:** `summary.runtime.bootTime`

### `vm_custom_object_attributes`
**Type:** `str`  
**Default:** `None`  
**Example:** `config.uuid`

### `set_source_name_as_cluster_group`
**Type:** `bool`  
**Default:** `False`

this will set the sources name as cluster group name instead of the datacenter. This works
if the vCenter has ONLY ONE datacenter configured. Otherwise it will rename all
datacenters to the source name!

### `sync_vm_dummy_interfaces`
**Type:** `bool`  
**Default:** `False`

activating this option will also include "dummy/virtual" interfaces which are only visible
inside the VM and are exposed through VM guest tools. Dummy interfaces without an IP
address will be skipped.

### `disable_vlan_sync`
**Type:** `bool`  
**Default:** `False`

disables syncing of any VLANs visible in vCenter to NetBox

### `vlan_sync_exclude_by_name`
**Type:** `str`  
**Default:** `None`  
**Example:** `New York/Storage, Backup, Tokio/DMZ, Madrid/.*`

### `vlan_sync_exclude_by_id`
**Type:** `str`  
**Default:** `None`  
**Example:** `Frankfurt/25, 1023-1042`

### `vlan_group_relation_by_name`
**Type:** `str`  
**Default:** `None`  
**Example:** `London/Vlan_.* = VLAN Group 1, Tokio/Vlan_.* = VLAN Group 2`

adds a relation to assign VLAN groups to matching VLANs by name. Same matching rules as
the exclude_by_name option uses are applied. If name and id relations are defined, the
name relation takes precedence. Fist match wins. Only newly discovered VLANs which are not
present in NetBox will be assigned a VLAN group. Supported scopes for a VLAN group are
"site", "site-group", "cluster" and "cluster-group". Scopes are buggy in NetBox
https://github.com/netbox-community/netbox/issues/18706

### `vlan_group_relation_by_id`
**Type:** `str`  
**Default:** `None`  
**Example:** `1023-1042 = VLAN Group 1, Tokio/2342 = VLAN Group 2`

adds a relation to assign VLAN groups to matching VLANs by ID. Same matching rules as the
exclude_by_id option uses are applied. Fist match wins. Only newly discovered VLANs which
are not present in NetBox will be assigned a VLAN group.

### `track_vm_host`
**Type:** `bool`  
**Default:** `False`

enabling this option will add the ESXi host this VM is running on to the VM details

### `overwrite_device_interface_name`
**Type:** `bool`  
**Default:** `True`

define if the name of the device interface discovered overwrites the interface name in
NetBox. The interface will only be matched by identical MAC address

### `overwrite_vm_interface_name`
**Type:** `bool`  
**Default:** `True`

define if the name of the VM interface discovered overwrites the interface name in NetBox.
The interface will only be matched by identical MAC address

### `overwrite_device_platform`
**Type:** `bool`  
**Default:** `True`

define if the platform of the device discovered overwrites the device platform in NetBox.

### `overwrite_vm_platform`
**Type:** `bool`  
**Default:** `True`

define if the platform of the VM discovered overwrites the VM platform in NetBox.

### `host_management_interface_match`
**Type:** `str`  
**Default:** `management, mgmt`

set a matching value for ESXi host management interface description (case insensitive,
comma separated). Used to figure out the ESXi primary IP address

### `ip_tenant_inheritance_order`
**Type:** `str`  
**Default:** `device, prefix`

define in which order the IP address tenant will be assigned if tenant is undefined.
possible values:
  * device : host or VM tenant will be assigned to the IP address
  * prefix : if the IP address belongs to an existing prefix and this prefix has a tenant assigned, then this one is used
  * disabled : no tenant assignment to the IP address will be performed
the order of the definition is important, the default is "device, prefix" which means:
If the device has a tenant then this one will be used. If not, the prefix tenant will be used if defined

### `sync_vm_interface_mtu`
**Type:** `bool`  
**Default:** `True`

Usually netbox-sync grabs the MTU size for the VM interface from the ESXi hosts vSwitch.
If this is not fitting or incorrect it is possible to disable the synchronisation by
setting this option to 'False'

### `host_nic_exclude_by_mac_list`
**Type:** `str`  
**Default:** `None`  
**Example:** `AA:BB:CC:11:22:33, 66:77:88:AA:BB:CC`

defines a comma separated list of MAC addresses which should be excluded from sync. Any
host NIC with a matching MAC address will be excluded from sync.

### `custom_attribute_exclude`
**Type:** `str`  
**Default:** `None`  
**Example:** `VB_LAST_BACKUP, VB_LAST_BACKUP2`

defines a comma separated list of custom attribute which should be excluded from sync. Any
custom attribute with a matching attribute key will be excluded from sync.

### `vm_disk_and_ram_in_decimal`
**Type:** `bool`  
**Default:** `True`

In NetBox version 4.1.0 and newer the VM disk and RAM values are displayed in power of 10
instead of power of 2. If this values is set to true 4GB of RAM will be set to a value of
4000 megabyte. If set to false 4GB of RAM will be reported as 4096MB. The same behavior
also applies for VM disk sizes.

### `netbox_host_device_role`
**Type:** `str`  
**Default:** `None`

### `netbox_vm_device_role`
**Type:** `str`  
**Default:** `None`

### `sync_tags`
**Type:** `bool`  
**Default:** `None`

### `sync_parent_tags`
**Type:** `bool`  
**Default:** `None`

## Example (YAML)

```
source:
  enabled: true
  # type: "vmware"  # required
  # host_fqdn: "vcenter.example.com"  # required
  port: 443
  # username: "vcenter-readonly"  # required
  # password: "super-secret"  # required
  validate_tls_certs: false
  # proxy_host: "10.10.1.10"  # optional
  # proxy_port: 3128  # optional
  # permitted_subnets: "172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24"  # optional
  # cluster_exclude_filter: null  # optional
  # cluster_include_filter: null  # optional
  # host_exclude_filter: null  # optional
  # host_include_filter: null  # optional
  # vm_exclude_filter: null  # optional
  # vm_include_filter: null  # optional
  # vm_exclude_by_tag_filter: "tag-a, tag-b"  # optional
  # cluster_site_relation: "Cluster_NYC = New York, Cluster_FFM.* = Frankfurt, Datacenter_TOKIO/.* = Tokio, Cluster_MultiSite = <NONE>"  # optional
  # host_site_relation: "nyc02.* = New York, ffm01.* = Frankfurt"  # optional
  # cluster_scope_type_relation: "Cluster_NYC = dcim.site, Cluster_FFM = dcim.sitegroup, Cluster_BER = dcim.location"  # optional
  # cluster_scope_id_relation: "Cluster_NYC = 1, Cluster_FFM.* = 2, Cluster_BER = 7"  # optional
  # cluster_tenant_relation: "Cluster_NYC.* = Customer A"  # optional
  # host_tenant_relation: "esxi300.* = Infrastructure"  # optional
  # vm_tenant_relation: "grafana.* = Infrastructure"  # optional
  # host_platform_relation: "VMware ESXi 7.0.3 = VMware ESXi 7.0 Update 3o"  # optional
  # vm_platform_relation: "centos-7.* = centos7, microsoft-windows-server-2016.* = Windows2016"  # optional
  host_role_relation: ".* = Server"
  # vm_role_relation: ".* = Server"  # optional
  # cluster_tag_relation: "Cluster_NYC.* = Infrastructure"  # optional
  # host_tag_relation: "esxi300.* = Infrastructure"  # optional
  # vm_tag_relation: "grafana.* = Infrastructure"  # optional
  match_host_by_serial: true
  match_on_mac_address: true
  match_on_ip_address: true
  collect_hardware_asset_tag: true
  collect_hardware_serial: true
  dns_name_lookup: true
  # custom_dns_servers: "192.168.1.11, 192.168.1.12"  # optional
  set_primary_ip: "when-undefined"
  skip_vm_comments: false
  skip_vm_templates: true
  skip_offline_vms: false
  skip_srm_placeholder_vms: false
  strip_host_domain_name: false
  strip_vm_domain_name: false
  # cluster_tag_source: null  # optional
  # host_tag_source: null  # optional
  # vm_tag_source: null  # optional
  sync_custom_attributes: false
  # host_custom_object_attributes: "summary.runtime.bootTime"  # optional
  # vm_custom_object_attributes: "config.uuid"  # optional
  set_source_name_as_cluster_group: false
  sync_vm_dummy_interfaces: false
  disable_vlan_sync: false
  # vlan_sync_exclude_by_name: "New York/Storage, Backup, Tokio/DMZ, Madrid/.*"  # optional
  # vlan_sync_exclude_by_id: "Frankfurt/25, 1023-1042"  # optional
  # vlan_group_relation_by_name: "London/Vlan_.* = VLAN Group 1, Tokio/Vlan_.* = VLAN Group 2"  # optional
  # vlan_group_relation_by_id: "1023-1042 = VLAN Group 1, Tokio/2342 = VLAN Group 2"  # optional
  track_vm_host: false
  overwrite_device_interface_name: true
  overwrite_vm_interface_name: true
  overwrite_device_platform: true
  overwrite_vm_platform: true
  host_management_interface_match: "management, mgmt"
  ip_tenant_inheritance_order: "device, prefix"
  sync_vm_interface_mtu: true
  # host_nic_exclude_by_mac_list: "AA:BB:CC:11:22:33, 66:77:88:AA:BB:CC"  # optional
  # custom_attribute_exclude: "VB_LAST_BACKUP, VB_LAST_BACKUP2"  # optional
  vm_disk_and_ram_in_decimal: true
  # netbox_host_device_role: null  # optional
  # netbox_vm_device_role: null  # optional
  # sync_tags: null  # optional
  # sync_parent_tags: null  # optional
```

## Example (INI)

```
[source]
enabled = true
# type = vmware  ; required
# host_fqdn = vcenter.example.com  ; required
port = 443
# username = vcenter-readonly  ; required
# password = super-secret  ; required
validate_tls_certs = false
# proxy_host = 10.10.1.10  ; optional
# proxy_port = 3128  ; optional
# permitted_subnets = 172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, fd00::/8, !10.23.42.0/24  ; optional
# cluster_exclude_filter =  ; optional
# cluster_include_filter =  ; optional
# host_exclude_filter =  ; optional
# host_include_filter =  ; optional
# vm_exclude_filter =  ; optional
# vm_include_filter =  ; optional
# vm_exclude_by_tag_filter = tag-a, tag-b  ; optional
# cluster_site_relation = Cluster_NYC = New York, Cluster_FFM.* = Frankfurt, Datacenter_TOKIO/.* = Tokio, Cluster_MultiSite = <NONE>  ; optional
# host_site_relation = nyc02.* = New York, ffm01.* = Frankfurt  ; optional
# cluster_scope_type_relation = Cluster_NYC = dcim.site, Cluster_FFM = dcim.sitegroup, Cluster_BER = dcim.location  ; optional
# cluster_scope_id_relation = Cluster_NYC = 1, Cluster_FFM.* = 2, Cluster_BER = 7  ; optional
# cluster_tenant_relation = Cluster_NYC.* = Customer A  ; optional
# host_tenant_relation = esxi300.* = Infrastructure  ; optional
# vm_tenant_relation = grafana.* = Infrastructure  ; optional
# host_platform_relation = VMware ESXi 7.0.3 = VMware ESXi 7.0 Update 3o  ; optional
# vm_platform_relation = centos-7.* = centos7, microsoft-windows-server-2016.* = Windows2016  ; optional
host_role_relation = .* = Server
# vm_role_relation = .* = Server  ; optional
# cluster_tag_relation = Cluster_NYC.* = Infrastructure  ; optional
# host_tag_relation = esxi300.* = Infrastructure  ; optional
# vm_tag_relation = grafana.* = Infrastructure  ; optional
match_host_by_serial = true
match_on_mac_address = true
match_on_ip_address = true
collect_hardware_asset_tag = true
collect_hardware_serial = true
dns_name_lookup = true
# custom_dns_servers = 192.168.1.11, 192.168.1.12  ; optional
set_primary_ip = when-undefined
skip_vm_comments = false
skip_vm_templates = true
skip_offline_vms = false
skip_srm_placeholder_vms = false
strip_host_domain_name = false
strip_vm_domain_name = false
# cluster_tag_source =  ; optional
# host_tag_source =  ; optional
# vm_tag_source =  ; optional
sync_custom_attributes = false
# host_custom_object_attributes = summary.runtime.bootTime  ; optional
# vm_custom_object_attributes = config.uuid  ; optional
set_source_name_as_cluster_group = false
sync_vm_dummy_interfaces = false
disable_vlan_sync = false
# vlan_sync_exclude_by_name = New York/Storage, Backup, Tokio/DMZ, Madrid/.*  ; optional
# vlan_sync_exclude_by_id = Frankfurt/25, 1023-1042  ; optional
# vlan_group_relation_by_name = London/Vlan_.* = VLAN Group 1, Tokio/Vlan_.* = VLAN Group 2  ; optional
# vlan_group_relation_by_id = 1023-1042 = VLAN Group 1, Tokio/2342 = VLAN Group 2  ; optional
track_vm_host = false
overwrite_device_interface_name = true
overwrite_vm_interface_name = true
overwrite_device_platform = true
overwrite_vm_platform = true
host_management_interface_match = management, mgmt
ip_tenant_inheritance_order = device, prefix
sync_vm_interface_mtu = true
# host_nic_exclude_by_mac_list = AA:BB:CC:11:22:33, 66:77:88:AA:BB:CC  ; optional
# custom_attribute_exclude = VB_LAST_BACKUP, VB_LAST_BACKUP2  ; optional
vm_disk_and_ram_in_decimal = true
# netbox_host_device_role =  ; optional
# netbox_vm_device_role =  ; optional
# sync_tags =  ; optional
# sync_parent_tags =  ; optional
```

---

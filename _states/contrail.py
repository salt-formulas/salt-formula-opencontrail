#!/usr/bin/python
# Copyright 2017 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Management of Contrail resources
================================

:depends:   - vnc_api Python module


Enforce the virtual router existence
------------------------------------

.. code-block:: yaml

    virtual_router:
      contrail.virtual_router_present:
        name: tor01
        ip_address: 10.0.0.23
        dpdk_enabled: False
        router_type: tor-agent


Enforce the virtual router absence
----------------------------------

.. code-block:: yaml

    virtual_router_tor01:
      contrail.virtual_router_absent:
        name: tor01


Enforce the physical router existence
------------------------------------

.. code-block:: yaml

    physical_router_phr01:
      contrail.physical_router_present:
      name: phr01
        parent_type: global-system-config
        management_ip: 10.167.4.206
        dataplane_ip: 172.17.56.9
        vendor_name: MyVendor
        product_name: MyProduct
        agents:
          - tor01
          - tns01


Enforce the physical router absence
----------------------------------

.. code-block:: yaml

    physical_router_delete_phr01:
      contrail.physical_router_absent:
        name: phr01


Enforce the physical interface present
----------------------------------

.. code-block:: yaml

    create physical interface ge-0/1/10 for phr01:
      contrail.physical_interface_present:
        - name: ge-0/1/10
        - physical_router: prh01


Enforce the physical interface absence
----------------------------------

.. code-block:: yaml

    physical_interface_delete ge-0/1/10:
      contrail.physical_interface_absent:
        name: ge-0/1/10
        physical_router: phr01

Enforce the logical interface present
----------------------------------

.. code-block:: yaml

    create logical interface 11/15:
      contrail.logical_interface_present:
        - name: ge-0/1/11.15
        - parent_names:
          - ge-0/1/11
          - phr01
        - parent_type: physical-interface
        - vlan_tag: 15
        - interface_type: L3


Enforce the logical interface absence
----------------------------------

.. code-block:: yaml

    logical interface delete ge-0/1/10.0 phr02:
      contrail.logical_interface_absent:
        - name: ge-0/1/10.0
        - parent_names:
          - ge-0/1/10
          - phr02
        - parent_type: physical-interface


Enforce the global vrouter config existence
-------------------------------------------

.. code-block:: yaml

    #Example
    opencontrail_client_virtual_router_global_conf_create:
      contrail.global_vrouter_config_present:
      - name: "global-vrouter-config"
      - parent_type: "global-system-config"
      - encap_priority : "MPLSoUDP,MPLSoGRE"
      - vxlan_vn_id_mode : "automatic"
      - flow_export_rate: 100
      - fq_names:
        - default-global-system-config
        - default-global-vrouter-config


Enforce the global vrouter config absence
-----------------------------------------

.. code-block:: yaml

    #Example
    opencontrail_client_virtual_router_global_conf_delete:
      contrail.global_vrouter_config_absent:
      - name: "global-vrouter-config"


Enforce the link local service entry existence
----------------------------------------------

.. code-block:: yaml

    # Example with dns name, only one is permited
    lls_meta1:
      contrail.linklocal_service_present:
        - name: meta1
        - lls_ip: 10.0.0.23
        - lls_port: 80
        - ipf_addresses: "meta.example.com"
        - ipf_port: 80

    # Example with multiple ip addresses
    lls_meta2:
      contrail.linklocal_service_present:
        - name: meta2
        - lls_ip: 10.0.0.23
        - lls_port: 80
        - ipf_addresses:
          - 10.10.10.10
          - 10.20.20.20
          - 10.30.30.30
        - ipf_port: 80

    # Example with one ip addresses
    lls_meta3:
      contrail.linklocal_service_present:
        - name: meta3
        - lls_ip: 10.0.0.23
        - lls_port: 80
        - ipf_addresses:
          - 10.10.10.10
        - ipf_port: 80


Enforce the link local service entry absence
--------------------------------------------

.. code-block:: yaml

    lls_meta1_delete:
      contrail.linklocal_service_absent:
        - name: cmp01


Enforce the analytics node existence
------------------------------------

.. code-block:: yaml

    analytics_node01:
      contrail.analytics_node_present:
        - name: nal01
        - ip_address: 10.0.0.13


Enforce the analytics node absence
------------------------------------

.. code-block:: yaml

    analytics_node01_delete:
      contrail.analytics_node_absent:
        - name: nal01



Enforce the config node existence
---------------------------------

.. code-block:: yaml

    config_node01:
      contrail.config_node_present:
        - name: ntw01
        - ip_address: 10.0.0.23


Enforce the config node absence
-------------------------------

.. code-block:: yaml

    config_node01_delete:
      contrail.config_node_absent:
        - name: ntw01


Enforce the BGP router existence
--------------------------------

.. code-block:: yaml

    BGP router mx01:
      contrail.bgp_router_present:
        - name: mx01
        - ip_address: 10.0.0.133
        - type: mx
        - asn: 64512
        - key_type: md5
        - key: password


Enforce the BGP router absence
------------------------------

.. code-block:: yaml

    BGP router mx01:
      contrail.bgp_router_absence:
        - name: mx01


Enforce the service appliance set existence
-------------------------------------------

.. code-block:: yaml

   create service appliance:
     contrail.service_appliance_set_present:
       - name: testappliance
       - driver: 'neutron_lbaas.drivers.avi.avi_ocdriver.OpencontrailAviLoadbalancerDriver'
       - ha_mode: active-backup
       - properties:
           address: 10.1.11.3
           user: admin
           password: avi123
           cloud: Default-Cloud


Enforce the service appliance set entry absence
-----------------------------------------------

 .. code-block:: yaml

    delete service appliance:
     contrail.service_appliance_set_absent:
       - name: testappliance


Enforce the database node existence
-----------------------------------

.. code-block:: yaml

    database_node01:
      contrail.database_node_present:
        - name: dbs01
        - ip_address: 10.0.0.33


Enforce the database node absence
-----------------------------------

.. code-block:: yaml

    database_node01:
      contrail.database_node_absent:
        - name: dbs01


Enforce the global system config existence
------------------------------------------

.. code-block:: yaml
    global_system_config_update:
      contrail.global_system_config_present:
        - name: default-global-system_config
        - ans: 64512
        - grp:
            enable: true
            restart_time: 400
            bgp_helper_enable: true
            xmpp_helper_enable: true
            long_lived_restart_time: 400
            end_of_rib_timeout: 40


Enforce the global system config absence
----------------------------------------

.. code-block:: yaml

    global_system_config_delete:
      contrail.global_system_config_absent:
        - name: global-system_config


Enforce the virtual network existence
----------------------------------------

.. code-block: yaml

    virtual_network_create:
      contrail.virtual_network_present:
        - name: virtual_network_name
        - conf:
            domain: domain name
            project: domain project
            ipam_domain: ipam domain name
            ipam_project: ipam project name
            ipam_name: ipam name
            ip_prefix: xxx.xxx.xxx.xxx
            ip_prefix_len: 24
            asn: 64512
            target: 10000
            external: False
            allow_transit: False
            forwading_mode: 'l2_l3'
            rpf: 'disabled'
            mirror_destination: False



Enforce Floating Ip Pool configuration
----------------------------------------

.. code-block: yaml

    floating_ip_pool_present
       - vn_name: virtual_network_name
       - vn_project:
       - vn_domain
       - owner_access: owner_access_permission
       - global_access: global_access_permission
       - projects: list of project-permission pairs
'''


def __virtual__():
    '''
    Load Contrail module
    '''
    return 'contrail'


def virtual_router_present(name, ip_address, router_type=None, dpdk_enabled=False, **kwargs):
    '''
    Ensures that the Contrail virtual router exists.

    :param name:        Virtual router name
    :param ip_address:  Virtual router IP address
    :param router_type: Any of ['tor-agent', 'tor-service-node', 'embedded']
    '''
    ret = __salt__['contrail.virtual_router_create'](name, ip_address, router_type, dpdk_enabled, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def virtual_router_absent(name, **kwargs):
    '''
    Ensure that the Contrail virtual router doesn't exist

    :param name: The name of the virtual router that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Virtual router "{0}" is already absent'.format(name)}
    virtual_router = __salt__['contrail.virtual_router_get'](name, **kwargs)
    if 'Error' not in virtual_router:
        ret = __salt__['contrail.virtual_router_delete'](name, **kwargs)
    return ret


def physical_router_present(name, parent_type=None,
                            management_ip=None,
                            dataplane_ip=None,  # VTEP address in web GUI
                            vendor_name=None,
                            product_name=None,
                            vnc_managed=None,
                            junos_service_ports=None,
                            agents=None, **kwargs):
    '''
    Ensures that the Contrail virtual router exists.

    :param name:        	Physical router name
    :param parent_type:		Parent resource type: Any of ['global-system-config']
    :param management_ip:	Management ip for this physical router. It is used by the device manager to perform netconf and by SNMP collector if enabled.
    :param dataplane_ip: 	VTEP address in web GUI. This is ip address in the ip-fabric(underlay) network that can be used in data plane by physical router. Usually it is the VTEP address in VxLAN for the TOR switch.
    :param vendor_name:		Vendor name of the physical router (e.g juniper). Used by the device manager to select driver.
    :param product_name:	Model name of the physical router (e.g juniper). Used by the device manager to select driver.
    :param vnc_managed:		This physical router is enabled to be configured by device manager.
    :param user_credentials:	Username and password for netconf to the physical router by device manager.
    :param junos_service_ports:	Juniper JUNOS specific service interfaces name to perform services like NAT.
    :param agents: 		List of virtual-router references
    '''

    ret = __salt__['contrail.physical_router_create'](name, parent_type, management_ip, dataplane_ip, vendor_name,
                                                      product_name, vnc_managed, junos_service_ports, agents,
                                                      **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def physical_router_absent(name, **kwargs):
    '''
    Ensure that the Contrail physical router doesn't exist

    :param name: The name of the physical router that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Physical router "{0}" is already absent'.format(name)}
    physical_router = __salt__['contrail.physical_router_get'](name, **kwargs)
    if 'Error' not in physical_router:
        ret = __salt__['contrail.physical_router_delete'](name, **kwargs)
    return ret


def physical_interface_present(name, physical_router, **kwargs):
    '''
    Ensures that the Contrail physical interface exists.

    :param name:                Physical interface name
    :param physical_router:     Name of existing physical router
    '''
    ret = __salt__['contrail.physical_interface_create'](name, physical_router, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def physical_interface_absent(name, physical_router, **kwargs):
    '''
    Ensure that the Contrail physical interface doesn't exist

    :param name: 		The name of the physical interface that should not exist
    :param physical_router:     Physical router name
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Physical interface "{0}" is already absent'.format(name)}
    physical_interface = __salt__['contrail.physical_interface_get'](name, physical_router, **kwargs)
    if 'Error' not in physical_interface:
        ret = __salt__['contrail.physical_interface_delete'](name, physical_router, **kwargs)
    return ret


def logical_interface_present(name, parent_names, parent_type, vlan_tag=None, interface_type="L2",
                              vmis=None, **kwargs):
    '''
    Ensures that the Contrail logical interface exists.

    :param name:                Logical interface name
    :param parent_names:  	List of parents
    :param parent_type		Parent resource type. Any of ['physical-router', 'physical-interface']
    :param vlan_tag:		VLAN tag (.1Q) classifier for this logical interface.
    :param interface_type:	Logical interface type can be L2 or L3.
    :param vmis:                Virtual machine interface name associate with
    '''
    ret = __salt__['contrail.logical_interface_create'](name, parent_names, parent_type, vlan_tag,
                                                        interface_type, vmis=vmis, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def logical_interface_absent(name, parent_names, parent_type=None, **kwargs):
    '''
    Ensure that the Contrail logical interface doesn't exist

    :param name: 		The name of the logical interface that should not exist
    :param parent_names: 	List of parent names. Example ['phr01','ge-0/1/0']
    :param parent_type: 	Parent resource type. Any of ['physical-router', 'physical-interface']
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'logical interface "{0}" is already absent'.format(name)}
    logical_interface = __salt__['contrail.logical_interface_get'](name, parent_names, parent_type, **kwargs)
    if 'Error' not in logical_interface:
        ret = __salt__['contrail.logical_interface_delete'](name, parent_names, parent_type, **kwargs)
    return ret


def global_vrouter_config_present(name, parent_type, encap_priority="MPLSoUDP,MPLSoGRE", vxlan_vn_id_mode="automatic",
                                  flow_export_rate=None, *fq_names, **kwargs):
    '''
    Ensures that the Contrail global vrouter config exists.

    :param name:         	Global vrouter config name
    :param parent_type:  	Parent resource type
    :param encap_priority: 	Ordered list of encapsulations that vrouter will use in priority order
    :param vxlan_vn_id_mode:	Method of allocation of VxLAN VNI(s).
    :param fq_names:		Fully Qualified Name of resource devided <string>array
    :param flow_export_rate:	Flow export rate is global config, rate at which each vrouter will sample and export flow records to analytics
    '''
    ret = __salt__['contrail.global_vrouter_config_create'](name, parent_type, encap_priority, vxlan_vn_id_mode,
                                                            flow_export_rate, *fq_names, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def global_vrouter_config_absent(name, **kwargs):
    '''
    Ensure that the Contrail global vrouter config doesn't exist

    :param name: The name of the global vrouter config that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Global vrouter config "{0}" is already absent'.format(name)}
    vrouter_conf = __salt__['contrail.global_vrouter_config_get'](name, **kwargs)
    if 'Error' not in vrouter_conf:
        ret = __salt__['contrail.global_vrouter_config_delete'](name, **kwargs)
    return ret


def linklocal_service_present(name, lls_ip, lls_port, ipf_addresses, ipf_port, **kwargs):
    '''
    Ensures that the Contrail link local service entry exists.

    :param name:           Link local service name
    :param lls_ip:         Link local ip address
    :param lls_port:       Link local service port
    :param ipf_addresses:  IP fabric dns name or list of IP fabric ip addresses
    :param ipf_port:       IP fabric port
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Link local service "{0}" already exists'.format(name)}

    ret = __salt__['contrail.linklocal_service_create'](name, lls_ip, lls_port, ipf_addresses, ipf_port, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def linklocal_service_absent(name, **kwargs):
    '''
    Ensure that the Contrail link local service entry doesn't exist

    :param name: The name of the link local service entry
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Linklocal service "{0}" is already absent'.format(name)}
    lls = __salt__['contrail.linklocal_service_get'](name, **kwargs)
    if 'Error' not in lls:
        ret = __salt__['contrail.linklocal_service_delete'](name, **kwargs)
    return ret


def analytics_node_present(name, ip_address, **kwargs):
    '''
    Ensures that the Contrail analytics node exists.

    :param name:        Analytics node name
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Analytics node {0} already exists'.format(name)}

    ret = __salt__['contrail.analytics_node_create'](name, ip_address, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def analytics_node_absent(name, **kwargs):
    '''
    Ensure that the Contrail analytics node doesn't exist

    :param name: The name of the analytics node that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Analytics node "{0}" is already absent'.format(name)}
    node = __salt__['contrail.analytics_node_get'](name, **kwargs)
    if 'Error' not in node:
        ret = __salt__['contrail.analytics_node_delete'](name, **kwargs)
    return ret


def config_node_present(name, ip_address, **kwargs):
    '''
    Ensures that the Contrail config node exists.

    :param name:        Config node name
    '''
    ret = __salt__['contrail.config_node_create'](name, ip_address, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def config_node_absent(name, **kwargs):
    '''
    Ensure that the Contrail config node doesn't exist

    :param name: The name of the config node that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Config node "{0}" is already absent'.format(name)}
    node = __salt__['contrail.config_node_get'](name, **kwargs)
    if 'Error' not in node:
        ret = __salt__['contrail.config_node_delete'](name, **kwargs)
    return ret


def bgp_router_present(name, type, ip_address, asn=64512, key_type=None, key=None, **kwargs):
    '''
    Ensures that the Contrail BGP router exists.

    :param name:        BGP router name
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'BGP router {0} already exists'.format(name)}

    ret = __salt__['contrail.bgp_router_create'](name, type, ip_address, asn, key_type, key, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def bgp_router_absent(name, **kwargs):
    '''
    Ensure that the Contrail BGP router doesn't exist

    :param name: The name of the BGP router that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'BGP router "{0}" is already absent'.format(name)}
    node = __salt__['contrail.bgp_router_get'](name, **kwargs)
    if 'Error' not in node:
        ret = __salt__['contrail.bgp_router_delete'](name, **kwargs)
    return ret


def database_node_present(name, ip_address, **kwargs):
    '''
    Ensures that the Contrail database node exists.

    :param name:        Database node name
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Database node {0} already exists'.format(name)}
    ret = __salt__['contrail.database_node_create'](name, ip_address, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def database_node_absent(name, **kwargs):
    '''
    Ensure that the Contrail database node doesn't exist

    :param name: The name of the database node that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Database node "{0}" is already absent'.format(name)}
    node = __salt__['contrail.database_node_get'](name, **kwargs)
    if 'Error' not in node:
        ret = __salt__['contrail.database_node_delete'](name, **kwargs)
    return ret


def virtual_machine_interface_present(name,
                                      virtual_network,
                                      mac_address=None,
                                      ip_address=None,
                                      security_group=None,
                                      **kwargs):
    '''
    Ensures that the Contrail virtual machine interface exists.

    :param name:             Virtual machine interface name
    :param virtual_network:  Network name
    :param mac_address:      Mac address of vmi interface
    :param ip_address:       Virtual machine interface ip address
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Virtual machine interface "{0}" already exists'.format(name)}

    vmis = __salt__['contrail.virtual_machine_interface_list'](**kwargs)

    for vmi in vmis:
      if vmi['name'] == name:
        return ret

    vmi = __salt__['contrail.virtual_machine_interface_create'](name, virtual_network,
                                                                mac_address=mac_address,
                                                                ip_address=ip_address,
                                                                security_group=security_group,
                                                                **kwargs)
    if vmi['name'] == name:
        ret['comment'] = 'Virtual machine interface {0} has been created'.format(name)
        ret['result'] = True
    else:
        ret['comment'] = 'Virtual machine interface {0} creation failed'.format(name)
        ret['result'] = False
    return ret


def service_appliance_set_present(name,
                                  properties=None,
                                  driver=None,
                                  ha_mode=None,
                                  **kwargs):
    '''
    Ensures that the Contrail service appliance set exists.

    :param name:             Service appliance set name
    :param properties:       Key:Value pairs that are used by the provider driver and opaque to sytem.
    :param driver:           Name of the provider driver for this service appliance set.
    :param ha_mode:          High availability mode for the service appliance set, active-active or active-backup.
    '''
    ret = __salt__['contrail.service_appliance_set_create'](name, properties, driver, ha_mode, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def service_appliance_set_absent(name, **kwargs):
    '''
    Ensure that the Contrail service appliance set doesn't exist

    :param name: The name of the service appliance set that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service appliance set "{0}" is already absent'.format(name)}
    physical_router = __salt__['contrail.service_appliance_set_get'](name, **kwargs)
    if 'Error' not in physical_router:
        ret = __salt__['contrail.service_appliance_set_delete'](name, **kwargs)
    return ret


def global_system_config_present(name, ans=64512, grp=None, **kwargs):
    '''
    Ensures that the Contrail global system config exists or is updated

    :param name:        Virtual router name
    :param ans:         Autonomous system number
    :param grp:         Graceful-Restart-Parameters - dict of parameters
    '''
    ret = __salt__['contrail.global_system_config_create'](name=name, ans=ans, grp=grp, **kwargs)
    if len(ret['changes']) == 0:
        pass
    return ret


def global_system_config_absent(name, **kwargs):
    '''
    Ensure that the Contrail global system config doesn't exist

    :param name: The name of the global system config that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Global system config "{0}" is already absent'.format(name)}
    gsc = __salt__['contrail.global_system_config_get'](name, **kwargs)
    if 'Error' not in gsc:
        ret = __salt__['contrail.global_system_config_delete'](name, **kwargs)
    return ret


def virtual_network_present(name, conf=None, **kwargs):
    '''
    Ensure that the virtual network exists.

    :param name: Name of the virtual network
    :param conf: Key:Value pairs used for network creation
    '''

    ret = __salt__['contrail.virtual_network_create'](name, conf, **kwargs)
    return ret

def floating_ip_pool_present(vn_name,
                             vn_project,
                             vn_domain=None,
                             owner_access=None,
                             global_access=None,
                             projects=None,
                             **kwargs):
    '''
    Ensure that floating ip pool existst
    Virtual network with flag external need to be created before this
    function is called

    :param vn_name: Name of the virtual network with external flag,
                    tell us which floating ip pool we want to manage
    :param vn_project: Name of the project in which floating pool exists
    :param vn_domain: Name of the domain in which floating pool exists
    :param owner_access: permissions rights for owner of the pool
    :param global_access: permissions rights for other users than owner
    :param projects: list of pairs (project, permission for given project)
    '''

    ret = __salt__['contrail.update_floating_ip_pool'](vn_name,
                                                       vn_project,
                                                       vn_domain,
                                                       owner_access,
                                                       global_access,
                                                       projects,
                                                       **kwargs)
    return ret

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

from netaddr import IPNetwork
from vnc_api.vnc_api import PhysicalRouter, PhysicalInterface, LogicalInterface
from vnc_api.vnc_api import EncapsulationPrioritiesType
from vnc_api.vnc_api import VirtualMachineInterface, MacAddressesType

try:
    from vnc_api import vnc_api
    from vnc_api.vnc_api import LinklocalServiceEntryType, \
        LinklocalServicesTypes, GlobalVrouterConfig
    from vnc_api.gen.resource_client import VirtualRouter, AnalyticsNode, \
        ConfigNode, DatabaseNode, BgpRouter
    from vnc_api.gen.resource_xsd import AddressFamilies, BgpSessionAttributes, \
        BgpSession, BgpPeeringAttributes, BgpRouterParams

    HAS_CONTRAIL = True
except ImportError:
    HAS_CONTRAIL = False

__opts__ = {}


def __virtual__():
    '''
    Only load this module if vnc_api library is installed.
    '''
    if HAS_CONTRAIL:
        return 'contrail'

    return False


def _auth(**kwargs):
    '''
    Set up Contrail API credentials.
    '''
    user = kwargs.get('user')
    password = kwargs.get('password')
    tenant_name = kwargs.get('project')
    api_host = kwargs.get('api_server_ip')
    api_port = kwargs.get('api_server_port')
    api_base_url = kwargs.get('api_base_url')
    use_ssl = False
    auth_host = kwargs.get('auth_host_ip')
    vnc_lib = vnc_api.VncApi(user, password, tenant_name,
                             api_host, api_port, api_base_url, wait_for_connect=True,
                             api_server_use_ssl=use_ssl, auth_host=auth_host)

    return vnc_lib


def _get_config(vnc_client, global_system_config='default-global-system-config'):
    try:
        gsc_obj = vnc_client.global_system_config_read(id=global_system_config)
    except vnc_api.NoIdError:
        gsc_obj = vnc_client.global_system_config_read(fq_name_str=global_system_config)
    except:
        gsc_obj = None

    return gsc_obj


def _get_rt_inst_obj(vnc_client):
    # TODO pick fqname hardcode from common
    rt_inst_obj = vnc_client.routing_instance_read(
        fq_name=['default-domain', 'default-project',
                 'ip-fabric', '__default__'])

    return rt_inst_obj

def _get_fq_name(vnc_client, resource_name, project_name, domain='default-domain'):
    res = [domain]
    if project_name:
        res.append(project_name)
    if resource_name:
        res.append(resource_name)
    return res

def _get_project_obj(vnc_client, name, domain='default-domain'):
    return vnc_client.project_read(fq_name=[domain, name])


def _get_ip(ip_w_pfx):
    return str(IPNetwork(ip_w_pfx).ip)


def virtual_router_list(**kwargs):
    '''
    Return a list of all Contrail virtual routers

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_router_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    vrouter_objs = vnc_client._objects_list('virtual-router', detail=True)
    for vrouter_obj in vrouter_objs:
        ret[vrouter_obj.name] = {
            'ip_address': vrouter_obj.virtual_router_ip_address,
            'dpdk_enabled': vrouter_obj.virtual_router_dpdk_enabled,
            'uuid': vrouter_obj.uuid

        }
    return ret


def virtual_router_get(name, **kwargs):
    '''
    Return a specific Contrail virtual router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_router_get cmp01
    '''
    ret = {}
    vrouter_objs = virtual_router_list(**kwargs)
    if name in vrouter_objs:
        ret[name] = vrouter_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving virtual router.'}
    return ret


def virtual_router_create(name, ip_address, router_type=None, dpdk_enabled=False, **kwargs):
    '''
    Create specific Contrail virtual router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_router_create cmp02 10.10.10.102
        router_types:
        - tor-agent
        - tor-service-node
        - embedded
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    vrouter_objs = virtual_router_list(**kwargs)
    router_types = ['tor-agent', 'tor-service-node', 'embedded']
    if router_type not in router_types:
        router_type = None
    if name in vrouter_objs:
        vrouter = virtual_router_get(name)
        vrouter_obj = vnc_client._object_read('virtual-router', id=vrouter[name]['uuid'])
        changed = False
        if vrouter_obj.get_virtual_router_ip_address() != ip_address:
            ret['ip_address'] = {'from': vrouter_obj.get_virtual_router_ip_address(), "to": ip_address}
            vrouter_obj.set_virtual_router_ip_address(ip_address)
            changed = True
        if vrouter_obj.get_virtual_router_type() != router_type:
            ret['router_type'] = {"from": vrouter_obj.get_virtual_router_type(), "to": router_type}
            vrouter_obj.set_virtual_router_type(router_type)
            changed = True
        if vrouter_obj.get_virtual_router_dpdk_enabled() != dpdk_enabled:
            ret['dpdk_enabled'] = {"from": vrouter_obj.get_virtual_router_dpdk_enabled(), "to": dpdk_enabled}
            vrouter_obj.set_virtual_router_dpdk_enabled(dpdk_enabled)
            changed = True
        if changed:
            if __opts__['test']:
                return "Virtual router " + name + " will be updated"
            vnc_client.virtual_router_update(vrouter_obj)
            return ret
        return {'OK': 'Virtual router %s already exists and is updated' % name}
    else:
        vrouter_obj = VirtualRouter(
            name, gsc_obj,
            virtual_router_ip_address=ip_address,
            virtual_router_type=router_type)
        vrouter_obj.set_virtual_router_dpdk_enabled(dpdk_enabled)
        if __opts__['test']:
            return "Virtual router " + name + " will be created"
        vnc_client.virtual_router_create(vrouter_obj)
    ret = virtual_router_list(**kwargs)
    return "Create"


def virtual_router_delete(name, **kwargs):
    '''
    Delete specific Contrail virtual router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_router_delete cmp01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    vrouter_obj = VirtualRouter(name, gsc_obj)
    if __opts__['test']:
        return "Virtual router " + name + " will be deleted"
    vnc_client.virtual_router_delete(
        fq_name=vrouter_obj.get_fq_name())
    return "Deleted"


def physical_router_list(**kwargs):
    '''
    Return a list of all Contrail physical routers

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_router_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    prouter_objs = vnc_client._objects_list('physical-router', detail=True)
    for prouter_obj in prouter_objs:
        ret[prouter_obj.name] = {
            'uuid': prouter_obj._uuid,
            'management_ip': prouter_obj._physical_router_management_ip,
            'product_name': prouter_obj._physical_router_product_name,
        }

    return ret


def physical_router_get(name, **kwargs):
    '''
    Return a specific Contrail physical router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_router_get router_name
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    prouter_objs = vnc_client._objects_list('physical-router', detail=True)
    for prouter_obj in prouter_objs:
        if name == prouter_obj.name:
            ret[name] = prouter_obj.__dict__
    if len(ret) == 0:
        return {'Error': 'Error in retrieving physical router.'}
    return ret


def physical_router_create(name, parent_type=None,
                           management_ip=None,
                           dataplane_ip=None,  # VTEP address in web GUI
                           vendor_name=None,
                           product_name=None,
                           vnc_managed=None,
                           junos_service_ports=None,
                           agents=None, **kwargs):
    '''
    Create specific Contrail physical router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_router_create OVSDB_router management_ip=10.167.4.202 dataplane_ip=172.16.20.15 vendor_name=MyVendor product_name=MyProduct agents="['tor01','tns01']"
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    prouter_objs = physical_router_list(**kwargs)
    if name in prouter_objs:
        prouter = physical_router_get(name)
        prouter_obj = vnc_client._object_read('physical-router', id=prouter[name]['_uuid'])
        if prouter_obj.physical_router_management_ip != management_ip:
            ret['management_ip'] = {'from': prouter_obj.physical_router_management_ip, "to": management_ip}
            prouter_obj.set_physical_router_management_ip(management_ip)
        if prouter_obj.physical_router_dataplane_ip != dataplane_ip:
            ret['dataplane_ip'] = {'from': prouter_obj.physical_router_dataplane_ip, "to": dataplane_ip}
            prouter_obj.set_physical_router_dataplane_ip(dataplane_ip)
        if prouter_obj.get_physical_router_vendor_name() != vendor_name:
            ret['vendor_name'] = {'from': prouter_obj.get_physical_router_vendor_name(), "to": vendor_name}
            prouter_obj.set_physical_router_vendor_name(vendor_name)
        if prouter_obj.get_physical_router_product_name() != product_name:
            ret['product_name'] = {'from': prouter_obj.get_physical_router_product_name(), "to": product_name}
            prouter_obj.set_physical_router_product_name(product_name)
        if prouter_obj.get_physical_router_vnc_managed() != vnc_managed:
            ret['vnc_managed'] = {'from': prouter_obj.get_physical_router_vnc_managed(), "to": vnc_managed}
            prouter_obj.set_physical_router_vnc_managed(vnc_managed)
        if prouter_obj.get_physical_router_junos_service_ports() != junos_service_ports:
            ret['junos_service_ports'] = {'from': prouter_obj.get_physical_router_junos_service_ports(),
                                          "to": junos_service_ports}
            prouter_obj.set_physical_router_junos_service_ports(junos_service_ports)

        if __opts__['test']:
            if len(ret) != 0:
                return "Physical router " + name + " will be updated"
            return {"OK": "Physical router exists and is updated"}

        vrouter_objs = vnc_client._objects_list('virtual-router', detail=True)  # all vrouter objects
        c_agents = []  # referenced vrouters
        for c_agent in prouter_obj.get_virtual_router_refs():
            c_agents.append(c_agent['uuid'])
        agent_objs = []  # required state of references
        for vrouter_obj in vrouter_objs:
            if vrouter_obj._display_name in agents and vrouter_obj._uuid not in c_agents:
                prouter_obj.add_virtual_router(vrouter_obj)
                ret['vrouter ' + vrouter_obj._display_name] = "Reference added"
            if vrouter_obj._display_name not in agents and vrouter_obj._uuid in c_agents:
                prouter_obj.del_virtual_router(vrouter_obj)
                ret['vrouter ' + vrouter_obj._display_name] = "Reference removed"
        vnc_client.physical_router_update(prouter_obj)

        if len(ret) == 0:
            return {"OK": "Physical router exists and is updated"}
        return ret
    else:
        if __opts__['test']:
            return "Physical router " + name + " will be created"
        prouter_obj = PhysicalRouter(
            name=name,
            parent_obj=None,
            physical_router_management_ip=management_ip,
            physical_router_dataplane_ip=dataplane_ip,
            physical_router_vendor_name=vendor_name,
            physical_router_product_name=product_name,
            physical_router_vnc_managed=vnc_managed,
            physical_router_junos_service_ports=junos_service_ports,
        )
        for agent in agents:
            vrouter = virtual_router_get(agent)
            vrouter_obj = vnc_client._object_read('virtual-router', id=vrouter[agent]['uuid'])
            prouter_obj.add_virtual_router(vrouter_obj)
        vnc_client.physical_router_create(prouter_obj)
    return "Created"


def physical_router_delete(name, **kwargs):
    '''
    Delete specific Contrail physical router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_router_delete router_name
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    prouter_obj = PhysicalRouter(name, gsc_obj)
    if __opts__['test']:
        return "Physical router " + name + " will be deleted"
    vnc_client.physical_router_delete(
        fq_name=prouter_obj.get_fq_name())
    return "Deleted"


def physical_interface_list(**kwargs):
    '''
    Return a list of all Contrail physical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_interface_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    pinterface_objs = vnc_client._objects_list('physical-interface', detail=True)
    for pinterface_obj in pinterface_objs:
        ret[pinterface_obj.name] = {
            'uuid': pinterface_obj._uuid,
            'fq_name': pinterface_obj.fq_name,
            'parent_type': pinterface_obj.parent_type,
        }

    return ret


def physical_interface_get(name, physical_router, **kwargs):
    '''
    Return a specific Contrail physical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_interface_get interface_name physical_router_name
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    pinterf_objs = vnc_client._objects_list('physical-interface', detail=True)
    for pinterf_obj in pinterf_objs:
        if name == pinterf_obj.name and physical_router in pinterf_obj.fq_name:
            ret[name] = pinterf_obj.__dict__
    if len(ret) == 0:
        return {'Error': 'Error in retrieving physical interface.'}
    return ret


def physical_interface_create(name, physical_router, **kwargs):
    '''
    Create specific Contrail physical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.physical_interface_create ge-0/0/10 physical_router_name
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    pinterf_obj = physical_interface_get(name, physical_router, **kwargs)
    if 'Error' not in pinterf_obj:
        return {'OK': 'Physical interface ' + name + ' on ' + physical_router + ' already exists'}
    else:
        if __opts__['test']:
            return "Physical interface " + name + " will be created"
        prouter = physical_router_get(physical_router)
        prouter_obj = vnc_client._object_read('physical-router', id=prouter[physical_router]['_uuid'])
        pinterf_obj = PhysicalInterface(name, prouter_obj)
        vnc_client.physical_interface_create(pinterf_obj)
    return "Created"


def physical_interface_delete(name, physical_router, **kwargs):
    '''
    Delete specific Contrail physical interface

    CLI Example:
    .. code-block:: bash

        salt '*' contrail.physical_interface_delete ge-0/0/0 phr01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    piface = physical_interface_get(name, physical_router)
    if __opts__['test']:
        return "Physical interface " + name + " will be deleted"
    vnc_client.physical_interface_delete(id=piface[name]['_uuid'])
    return "Deleted"


def logical_interface_list(**kwargs):
    '''
    Return a list of all Contrail logical interfaces

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.logical_interface_list
    '''
    ret = []
    vnc_client = _auth(**kwargs)
    liface_objs = vnc_client._objects_list('logical-interface', detail=True)
    for liface_obj in liface_objs:
        ret.append({
            'name': liface_obj.name,
            'uuid': liface_obj._uuid,
            'fq_name': liface_obj.fq_name,
            'parent_type': liface_obj.parent_type,
        })
    return ret


def logical_interface_get(name, parent_names, parent_type=None, **kwargs):
    '''
    Return a specific Contrail logical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.logical_interface_get ge-0/0/0.10 ['phr01']
        or
        salt '*' contrail.logical_interface_get ge-0/0/0.10 ['ge-0/0/0','phr01']
        or
        salt '*' contrail.logical_interface_get ge-0/0/0.10 ['phr01'] parent_type=physcal-interface
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    liface_objs = vnc_client._objects_list('logical-interface', detail=True)
    count = 0
    for liface_obj in liface_objs:
        if name == liface_obj.name and set(parent_names).issubset(liface_obj.fq_name):
            if parent_type and parent_type == liface_obj.parent_type:
                count += 1
                ret[liface_obj.name] = liface_obj.__dict__
            if not parent_type:
                count += 1
                ret[liface_obj.name] = liface_obj.__dict__
    if len(ret) == 0:
        return {'Error': 'Error in retrieving logical interface.'}
    if count > 1:
        return {
            'Error': 'Error Was found more then one logical interface. Please put more parent_name or put parent_type to chose one of them.'}
    return ret


def logical_interface_create(name, parent_names, parent_type='physical-interface', vlan_tag=None, interface_type="l2",
                             vmis=None, **kwargs):
    '''
    Create specific Contrail logical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.logical_interface_create ge-0/0/10.11 parent_names="['ge-0/0/0','phr1']" parent_type=physical-interface vlan_tag=1025 interface_type=L2
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)

    liface_obj = logical_interface_get(name, parent_names, parent_type, **kwargs)
    if 'Error' not in liface_obj:
        return {'OK': 'Logical interface ' + name + ' already exists'}
    else:
        if __opts__['test']:
            return "Logical interface " + name + " will be created"
        parent_obj = None
        for router in parent_names:
            parent_router = physical_router_get(router)
            if 'Error' not in parent_router:
                parent_obj = vnc_client._object_read('physical-router', id=parent_router[router]['_uuid'])
                break
        if not parent_obj:
            return {'Error': 'Physical router have to be defined'}
        if parent_type == 'physical-interface':
            for interface in parent_names:
                parent_interface = physical_interface_get(interface, parent_obj.name)
                if 'Error' not in parent_interface:
                    parent_obj = vnc_client._object_read('physical-interface', id=parent_interface[interface]['_uuid'])
                    break
        if interface_type.lower() == "l3":
            return {'Error': "Virtual Network have to be defined for L3 interface type"}

        liface_obj = LogicalInterface(name, parent_obj, vlan_tag, interface_type.lower())

        for vmi_name, vmi in vmis.iteritems():
            vmi = vnc_client.virtual_machine_interface_read(
                fq_name=_get_fq_name(vnc_client, resource_name=vmi_name,
                                     project_name=kwargs.get('tenant', 'admin')))
            liface_obj.add_virtual_machine_interface(vmi)
        vnc_client.logical_interface_create(liface_obj)

    return "Created"


def logical_interface_delete(name, parent_names, parent_type=None, **kwargs):
    '''
    Delete specific Contrail logical interface

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.logical_interface_delete ge-0/0/0.12 ['ge-0/0/0','phr01']
        or
        salt '*' contrail.logical_interface_delete ge-0/0/0.12 ['phr01'] parent_type=physical-router

    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    liface = logical_interface_get(name, parent_names, parent_type)
    if 'Error' not in liface:
        if __opts__['test']:
            return "Logical interface " + name + " will be deleted"
        vnc_client.logical_interface_delete(id=liface[name]['_uuid'])
        return "Deleted"
    else:
        return liface


def global_vrouter_config_list(**kwargs):
    '''
    Return a list of all Contrail global vrouter configs

    CLI Example:

    .. code-block:: bash"

        salt '*' global_vrouter_config_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    vrouter_conf_objs = vnc_client._objects_list('global-vrouter-config', detail=True)
    for vrouter_conf_obj in vrouter_conf_objs:
        ret[vrouter_conf_obj._display_name] = vrouter_conf_obj.__dict__
    return ret


def global_vrouter_config_get(name, **kwargs):
    '''
    Return a specific Contrail global vrouter config

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.global_vrouter_get global-vrouter-config
    '''
    ret = {}
    vrouter_conf_objs = global_vrouter_config_list(**kwargs)
    if name in vrouter_conf_objs:
        ret[name] = vrouter_conf_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving  global vrouter config.'}
    return ret


def global_vrouter_config_create(name, parent_type, encap_priority, vxlan_vn_id_mode, *fq_names, **kwargs):
    '''
    Create specific Contrail global vrouter config

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.global_vrouter_config_create name=global-vrouter-config parent_type=global-system-config encap_priority="MPLSoUDP,MPLSoGRE" vxlan_vn_id_mode="automatic" fq_names="['default-global-system-config', 'default-global-vrouter-config']"
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    vrouter_conf_objs = global_vrouter_config_list(**kwargs)
    if name in vrouter_conf_objs:
        return {'OK': 'Global vrouter config %s already exists' % name}
    else:
        vrouter_conf_obj = GlobalVrouterConfig(
            name=name,
            parent_obj=None,
            encapsulation_priorities=EncapsulationPrioritiesType(encapsulation=encap_priority.split(",")),
            fq_name=fq_names,
            vxlan_network_identifier_mode=vxlan_vn_id_mode,
            parent_type=parent_type,
        )
        if __opts__['test']:
            return "Global vRouter config " + name + " will be created"
        vnc_client.global_vrouter_config_create(vrouter_conf_obj)
    return "Created"


def global_vrouter_config_delete(name, **kwargs):
    '''
    Delete specific Contrail global vrouter config

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.global_vrouter_config_delete global-vrouter-config
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    vrouter_conf_obj = GlobalVrouterConfig(name, gsc_obj)
    if __opts__['test']:
        return "Global vRouter config " + name + " will be deleted"
    vnc_client.global_vrouter_config_delete(
        fq_name=vrouter_conf_obj.get_fq_name())
    return "Deleted"


def analytics_node_list(**kwargs):
    '''
    Return a list of all Contrail analytics nodes

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.analytics_node_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    node_objs = vnc_client._objects_list('analytics-node', detail=True)
    for node_obj in node_objs:
        ret[node_obj.name] = node_obj.__dict__
    return ret


def analytics_node_get(name, **kwargs):
    '''
    Return a specific Contrail analytics node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.analytics_node_get nal01
    '''
    ret = {}
    vrouter_objs = analytics_node_list(**kwargs)
    if name in vrouter_objs:
        ret[name] = vrouter_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving analytics node.'}
    return ret


def analytics_node_create(name, ip_address, **kwargs):
    '''
    Create specific Contrail analytics node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.analytics_node_create ntw03 10.10.10.103
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    analytics_node_objs = analytics_node_list(**kwargs)
    if name in analytics_node_objs:
        return {'OK': 'Analytics node %s already exists' % name}
    else:
        analytics_node_obj = AnalyticsNode(
            name, gsc_obj,
            analytics_node_ip_address=ip_address)
        if __opts__['test']:
            return "AnalyticsNode " + name + " will be created"
        vnc_client.analytics_node_create(analytics_node_obj)
    return "Created"


def analytics_node_delete(name, **kwargs):
    '''
    Delete specific Contrail analytics node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.analytics_node_delete cmp01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    analytics_node_obj = AnalyticsNode(name, gsc_obj)
    if __opts__['test']:
        return "AnalyticsNode " + name + " will be deleted"
    vnc_client.analytics_node_delete(
        fq_name=analytics_node_obj.get_fq_name())
    return "Deleted"


def config_node_list(**kwargs):
    '''
    Return a list of all Contrail config nodes

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.config_node_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    node_objs = vnc_client._objects_list('config-node', detail=True)
    for node_obj in node_objs:
        ret[node_obj.name] = node_obj.__dict__
    return ret


def config_node_get(name, **kwargs):
    '''
    Return a specific Contrail config node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.config_node_get nal01
    '''
    ret = {}
    vrouter_objs = config_node_list(**kwargs)
    if name in vrouter_objs:
        ret[name] = vrouter_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving config node.'}
    return ret


def config_node_create(name, ip_address, **kwargs):
    '''
    Create specific Contrail config node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.config_node_create ntw03 10.10.10.103
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    config_node_objs = config_node_list(**kwargs)
    if name in config_node_objs:
        return {'OK': 'Config node %s already exists' % name}
    else:
        config_node_obj = ConfigNode(
            name, gsc_obj,
            config_node_ip_address=ip_address)
        if __opts__['test']:
            return "ConfigNode " + name + " will be created"
        vnc_client.config_node_create(config_node_obj)
    return "Created"


def config_node_delete(name, **kwargs):
    '''
    Delete specific Contrail config node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.config_node_delete cmp01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    config_node_obj = ConfigNode(name, gsc_obj)
    if __opts__['test']:
        return "ConfigNode " + name + " will be deleted"
    vnc_client.config_node_delete(
        fq_name=config_node_obj.get_fq_name())
    return "Deleted"


def bgp_router_list(**kwargs):
    '''
    Return a list of all Contrail BGP routers

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.bgp_router_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    bgp_router_objs = vnc_client._objects_list('bgp-router', detail=True)
    for bgp_router_obj in bgp_router_objs:
        ret[bgp_router_obj.name] = bgp_router_obj.__dict__
    return ret


def bgp_router_get(name, **kwargs):
    '''
    Return a specific Contrail BGP router

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.bgp_router_get nal01
    '''
    ret = {}
    bgp_router_objs = bgp_router_list(**kwargs)
    if name in bgp_router_objs:
        ret[name] = bgp_router_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving BGP router.'}
    return ret


def bgp_router_create(name, type, ip_address, asn=64512, **kwargs):
    '''
    Create specific Contrail control node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.bgp_router_create ntw03 control-node 10.10.10.103
        salt '*' contrail.bgp_router_create mx01 router 10.10.10.105
    '''
    ret = {}
    vnc_client = _auth(**kwargs)

    address_families = ['route-target', 'inet-vpn', 'e-vpn', 'erm-vpn',
                        'inet6-vpn']
    if type != 'control-node':
        address_families.remove('erm-vpn')

    bgp_addr_fams = AddressFamilies(address_families)
    bgp_sess_attrs = [
        BgpSessionAttributes(address_families=bgp_addr_fams)]
    bgp_sessions = [BgpSession(attributes=bgp_sess_attrs)]
    bgp_peering_attrs = BgpPeeringAttributes(session=bgp_sessions)
    rt_inst_obj = _get_rt_inst_obj(vnc_client)

    if type == 'control-node':
        vendor = 'contrail'
    elif type == 'router':
        vendor = 'mx'
    else:
        vendor = 'unknown'

    router_params = BgpRouterParams(router_type=type,
                                    vendor=vendor, autonomous_system=int(asn),
                                    identifier=_get_ip(ip_address),
                                    address=_get_ip(ip_address),
                                    port=179, address_families=bgp_addr_fams)

    bgp_router_objs = bgp_router_list(**kwargs)
    if name in bgp_router_objs:
        bgp_router_obj = vnc_client._object_read('bgp-router', id=bgp_router_objs[name]['_uuid'])
        bgp_router_obj.set_bgp_router_parameters(router_params)
        if __opts__['test']:
            return "BGP router " + name + " will be updated"
        vnc_client.bgp_router_update(bgp_router_obj)
    else:
        bgp_router_obj = BgpRouter(name, rt_inst_obj, bgp_router_parameters=router_params)
        if __opts__['test']:
            return "BGP router " + name + " will be created"
        vnc_client.bgp_router_create(bgp_router_obj)
        return "Created"
    return {'OK': 'Config node %s already exists' % name}


def bgp_router_delete(name, **kwargs):
    '''
    Delete specific Contrail control node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.bgp_router_delete mx01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    bgp_router_obj = BgpRouter(name, gsc_obj)

    if __opts__['test']:
        return "BGP router " + name + " will be deleted"
    vnc_client.bgp_router_delete(
        fq_name=bgp_router_obj.get_fq_name())

    return "Deleted"


def database_node_list(**kwargs):
    '''
    Return a list of all Contrail database nodes

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.database_node_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    node_objs = vnc_client._objects_list('database-node', detail=True)
    for node_obj in node_objs:
        ret[node_obj.name] = node_obj.__dict__
    return ret


def database_node_get(name, **kwargs):
    '''
    Return a specific Contrail database node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.database_node_get nal01
    '''
    ret = {}
    vrouter_objs = database_node_list(**kwargs)
    if name in vrouter_objs:
        ret[name] = vrouter_objs.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving database node.'}
    return ret


def database_node_create(name, ip_address, **kwargs):
    '''
    Create specific Contrail database node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.database_node_create ntw03 10.10.10.103
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    database_node_objs = database_node_list(**kwargs)
    if name in database_node_objs:
        return {'OK': 'Database node %s already exists' % name}
    else:
        database_node_obj = DatabaseNode(
            name, gsc_obj,
            database_node_ip_address=ip_address)
        if __opts__['test']:
            return "DatabaseNode " + name + " will be created"
        vnc_client.database_node_create(database_node_obj)
    return "Created"


def database_node_delete(name, **kwargs):
    '''
    Delete specific Contrail database node

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.database_node_delete cmp01
    '''
    vnc_client = _auth(**kwargs)
    gsc_obj = _get_config(vnc_client)
    database_node_obj = DatabaseNode(name, gsc_obj)
    if __opts__['test']:
        return "DatabaseNode " + name + " will be deleted"
    vnc_client.database_node_delete(
        fq_name=database_node_obj.get_fq_name())


def _get_vrouter_config(vnc_client):
    try:
        config = vnc_client.global_vrouter_config_read(
            fq_name=['default-global-system-config', 'default-global-vrouter-config'])
    except Exception:
        config = None

    return config


def linklocal_service_list(**kwargs):
    '''
    Return a list of all Contrail link local services

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.linklocal_service_list
    '''
    ret = {}
    vnc_client = _auth(**kwargs)

    current_config = _get_vrouter_config(vnc_client)
    if current_config is None:
        return ret

    service_list_res = current_config.get_linklocal_services()
    if service_list_res is None:
        service_list_obj = {'linklocal_service_entry': []}
    else:
        service_list_obj = service_list_res.__dict__
    for _, value in service_list_obj.iteritems():
        for entry in value:
            service = entry.__dict__
            if 'linklocal_service_name' in service:
                ret[service['linklocal_service_name']] = service
    return ret


def linklocal_service_get(name, **kwargs):
    '''
    Return a specific Contrail link local service

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.linklocal_service_get llservice
    '''
    ret = {}
    services = linklocal_service_list(**kwargs)
    if name in services:
        ret[name] = services.get(name)
    if len(ret) == 0:
        return {'Error': 'Error in retrieving link local service "{0}"'.format(name)}
    return ret


def linklocal_service_create(name, lls_ip, lls_port, ipf_dns_or_ip, ipf_port, **kwargs):
    '''
    Create specific Contrail link local service

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.linklocal_service_create \
            llservice 10.10.10.103 22 '["20.20.20.20", "30.30.30.30"]' 22
        salt '*' contrail.linklocal_service_create \
            llservice 10.10.10.103 22 link-local.service.dns-name 22
    '''
    ret = {}
    vnc_client = _auth(**kwargs)

    current_config = _get_vrouter_config(vnc_client)

    service_entry = LinklocalServiceEntryType(
        linklocal_service_name=name,
        linklocal_service_ip=lls_ip,
        linklocal_service_port=lls_port,
        ip_fabric_service_port=ipf_port)
    if isinstance(ipf_dns_or_ip, basestring):
        service_entry.ip_fabric_DNS_service_name = ipf_dns_or_ip
    elif isinstance(ipf_dns_or_ip, list):
        service_entry.ip_fabric_service_ip = ipf_dns_or_ip
        service_entry.ip_fabric_DNS_service_name = ''

    if current_config is None:
        new_services = LinklocalServicesTypes([service_entry])
        new_config = GlobalVrouterConfig(linklocal_services=new_services)
        if __opts__['test']:
            ret['GlobalVrouterConfig'] = "Global vRouter Config will be created"
        else:
            ret = "Created"
            vnc_client.global_vrouter_config_create(new_config)
    else:
        _current_service_list = current_config.get_linklocal_services()
        if _current_service_list is None:
            service_list = {'linklocal_service_entry': []}
        else:
            service_list = _current_service_list.__dict__
        new_services = [service_entry]
        for key, value in service_list.iteritems():
            if key != 'linklocal_service_entry':
                continue
            for _entry in value:
                entry = _entry.__dict__
                if 'linklocal_service_name' in entry:
                    if entry['linklocal_service_name'] == name:
                        return {'OK': 'Link local service "{0}" already exists'.format(name)}
                    new_services.append(_entry)
            if __opts__['test']:
                ret['Test'] = "LinkLocalSevices will be created"
            service_list[key] = new_services
        new_config = GlobalVrouterConfig(linklocal_services=service_list)
        if __opts__['test']:
            ret['GlobalVrouterConfig'] = "Global vRouter Config will be updated"
        else:
            vnc_client.global_vrouter_config_update(new_config)
            ret = "Created"
    return ret


def linklocal_service_delete(name, **kwargs):
    '''
    Delete specific link local service entry

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.linklocal_service_delete llservice
    '''
    vnc_client = _auth(**kwargs)

    current_config = _get_vrouter_config(vnc_client)

    found = False
    if current_config is not None:
        _current_service_list = current_config.get_linklocal_services()
        if _current_service_list is None:
            service_list = {'linklocal_service_entry': []}
        else:
            service_list = _current_service_list.__dict__
        new_services = []
        for key, value in service_list.iteritems():
            if key != 'linklocal_service_entry':
                continue
            for _entry in value:
                entry = _entry.__dict__
                if 'linklocal_service_name' in entry:
                    if entry['linklocal_service_name'] == name:
                        found = True
                    else:
                        new_services.append(_entry)
            service_list[key] = new_services
        new_config = GlobalVrouterConfig(linklocal_services=service_list)
        if __opts__['test']:
            return "Link local service " + name + " will be deleted"
        vnc_client.global_vrouter_config_update(new_config)
        return "Deleted"
    if not found:
        return {'Error': 'Link local service "{0}" not found'.format(name)}


def virtual_machine_interface_list(**kwargs):
    '''
    Return a list of all Contrail virtual machine interfaces

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_machine_interfaces
    '''
    ret = []
    vnc_client = _auth(**kwargs)
    project = _get_project_obj(vnc_client, name=kwargs.get('tenant', 'admin'))
    project_uuid = project.get_uuid()

    vm_ifaces = vnc_client.virtual_machine_interfaces_list(
        detail=True, parent_id=project_uuid)

    for vm_iface in vm_ifaces:
        ret.append(vm_iface.__dict__)

    return ret


def virtual_machine_interface_create(name,
                                     virtual_network,
                                     mac_address=None,
                                     ip_address=None,
                                     security_group=None,
                                     **kwargs):
    '''
    Create specific Contrail  virtual machine interface (Port)

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_machine_interface_create port01 net01 mac_address='01:02:03:04:05:06'
        router_types:
        - tor-agent
        - tor-service-node
        - embedded
    '''
    ret = {}
    vnc_client = _auth(**kwargs)
    project = _get_project_obj(vnc_client, name=kwargs.get('tenant', 'admin'))

    vm_int = VirtualMachineInterface(name, parent_obj=project)

    if mac_address:
      mac_address_obj = MacAddressesType([mac_address])
      vm_int.set_virtual_machine_interface_mac_addresses(mac_address_obj)

    if security_group:
      sgo = vnc_client.security_group_read(fq_name=_get_fq_name(
          vnc_client, security_group, kwargs.get('tenant', 'admin')))
      vm_int.set_security_group(sgo)

    vnet_uuid = virtual_network_get(virtual_network, **kwargs)[virtual_network]['_uuid']
    vnet_obj = vnc_client.virtual_network_read(id=vnet_uuid)
    vm_int.set_virtual_network(vnet_obj)

    vmi_uuid = vnc_client.virtual_machine_interface_create(vm_int)
    vmi = vnc_client.virtual_machine_interface_read(id=vmi_uuid)

    vm_int.set_port_security_enabled(False)
    vnc_client.virtual_machine_interface_update(vm_int)

    #Allocate IP to VMI
    ip = vnc_api.InstanceIp(name + '.ip')
    ip.set_virtual_machine_interface(vmi)
    ip.set_virtual_network(vnet_obj)

    ip_uuid = vnc_client.instance_ip_create(ip)

    if ip_address:
        ip.set_instance_ip_address(ip_address)
        vnc_client.instance_ip_update(ip)

    return vmi.__dict__


def virtual_network_list(**kwargs):
    '''
    Return a list of all Contrail virtual network

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_network
    '''

    ret = {}
    vnc_client = _auth(**kwargs)
    virtual_networks = vnc_client._objects_list('virtual-network', detail=True)
    for virtual_network in virtual_networks:
        ret[virtual_network.name] = virtual_network.__dict__
    return ret


def virtual_network_get(name, **kwargs):
    '''
    Return a specific Contrail virtual network

    CLI Example:

    .. code-block:: bash

        salt '*' contrail.virtual_network_get net01
    '''
    ret = {}
    vnet_objs = virtual_network_list(**kwargs)
    if name in vnet_objs:
        ret[name] = vnet_objs.get(name)
    if len(ret) != 1 :
        return {'result': False,
                'Error': 'Error in retrieving virtual networks.'}
    return ret

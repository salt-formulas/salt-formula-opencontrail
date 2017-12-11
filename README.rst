====================
OpenContrail Formula
====================

Contrail Controller is an open, standards-based software solution that
delivers network virtualization and service automation for federated cloud
networks. It provides self-service provisioning, improves network
troubleshooting and diagnostics, and enables service chaining for dynamic
application environments across enterprise virtual private cloud (VPC),
managed Infrastructure as a Service (IaaS), and Networks Functions
Virtualization (NFV) use cases.


Package source
==============

Formula support OpenContrail as well as Juniper Contrail package repository in the backend.

Differences withing the configuration and state run are controlled by
``opencontrail.common.vendor: [opencontrail|juniper]`` pillar attribute.

Default value is set to ``opencontrail``.

Juniper releases tested with this formula:
 - 3.0.2.x

To use Juniper Contrail repository as a source of packages override pillar as in this example:

.. code-block:: yaml

    opencontrail:
      common:
        vendor: juniper


Sample Pillars
==============

Controller nodes
----------------

There are several scenarios for OpenContrail control plane.

All-in-one single
~~~~~~~~~~~~~~~~~

Config, control, analytics, database, web -- altogether on one node.

.. code-block:: yaml

    opencontrail:
      common:
        version: 2.2
        source:
          engine: pkg
          address: http://mirror.robotice.cz/contrail-havana/
        identity:
          engine: keystone
          host: 127.0.0.1
          port: 35357
          token: token
          password: password
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
      config:
        version: 2.2
        enabled: true
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
        discovery:
          host: 127.0.0.1
        analytics:
          host: 127.0.0.1
        bind:
          address: 127.0.0.1
        message_queue:
          engine: rabbitmq
          host: 127.0.0.1
          port: 5672
        database:
          members:
          - host: 127.0.0.1
            port: 9160
        cache:
          members:
          - host: 127.0.0.1
            port: 11211
        identity:
          engine: keystone
          version: '2.0'
          region: RegionOne
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin
        members:
        - host: 127.0.0.1
          id: 1
        rootlogger: "INFO, CONSOLE"
      control:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        discovery:
          host: 127.0.0.1
        master:
          host: 127.0.0.1
        members:
        - host: 127.0.0.1
          id: 1
      collector:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        master:
          host: 127.0.0.1
        discovery:
          host: 127.0.0.1
        data_ttl: 2
        database:
          members:
          - host: 127.0.0.1
            port: 9160
      database:
        version: 2.2
        cassandra:
          version: 2
        enabled: true
        minimum_disk: 10
        name: 'Contrail'
        original_token: 0
        compaction_throughput_mb_per_sec: 16
        concurrent_compactors: 1
        data_dirs:
        - /var/lib/cassandra
        id: 1
        discovery:
          host: 127.0.0.1
        bind:
          host: 127.0.0.1
          port: 9042
          rpc_port: 9160
        members:
        - host: 127.0.0.1
          id: 1
      web:
        version: 2.2
        enabled: True
        bind:
          address: 127.0.0.1
        analytics:
          host: 127.0.0.1
        master:
          host: 127.0.0.1
        cache:
          engine: redis
          host: 127.0.0.1
          port: 6379
        members:
        - host: 127.0.0.1
          id: 1
        identity:
          engine: keystone
          version: '2.0'
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin


All-in-one cluster
~~~~~~~~~~~~~~~~~~

Config, control, analytics, database, web -- altogether, clustered on multiple
nodes.

.. code-block:: yaml

    opencontrail:
      common:
        version: 2.2
        source:
          engine: pkg
          address: http://mirror.robotice.cz/contrail-havana/
        identity:
          engine: keystone
          host: 127.0.0.1
          port: 35357
          token: token
          password: password
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
      config:
        version: 2.2
        enabled: true
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
        discovery:
          host: 127.0.0.1
        analytics:
          host: 127.0.0.1
        bind:
          address: 127.0.0.1
        message_queue:
          engine: rabbitmq
          host: 127.0.0.1
          port: 5672
        database:
          members:
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
        cache:
          members:
          - host: 127.0.0.1
            port: 11211
          - host: 127.0.0.1
            port: 11211
          - host: 127.0.0.1
            port: 11211
        identity:
          engine: keystone
          version: '2.0'
          region: RegionOne
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      control:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        discovery:
          host: 127.0.0.1
        master:
          host: 127.0.0.1
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      collector:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        master:
          host: 127.0.0.1
        discovery:
          host: 127.0.0.1
        data_ttl: 1
        database:
          members:
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
      database:
        version: 2.2
        cassandra:
          version: 2
        enabled: true
        name: 'Contrail'
        minimum_disk: 10
        original_token: 0
        data_dirs:
        - /var/lib/cassandra
        id: 1
        discovery:
          host: 127.0.0.1
        bind:
          host: 127.0.0.1
          port: 9042
          rpc_port: 9160
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      web:
        version: 2.2
        enabled: True
        bind:
          address: 127.0.0.1
        master:
          host: 127.0.0.1
        analytics:
          host: 127.0.0.1
        cache:
          engine: redis
          host: 127.0.0.1
          port: 6379
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
        identity:
          engine: keystone
          version: '2.0'
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin


Separated analytics from control and config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Config, control, database, web.

.. code-block:: yaml

    opencontrail:
      common:
        version: 2.2
        identity:
          engine: keystone
          host: 127.0.0.1
          port: 35357
          token: token
          password: password
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
      config:
        version: 2.2
        enabled: true
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
        discovery:
          host: 127.0.0.1
        analytics:
          host: 127.0.0.1
        bind:
          address: 127.0.0.1
        message_queue:
          engine: rabbitmq
          host: 127.0.0.1
          port: 5672
        database:
          members:
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
        cache:
          members:
          - host: 127.0.0.1
            port: 11211
          - host: 127.0.0.1
            port: 11211
          - host: 127.0.0.1
            port: 11211
        identity:
          engine: keystone
          version: '2.0'
          region: RegionOne
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      control:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        discovery:
          host: 127.0.0.1
        master:
          host: 127.0.0.1
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      database:
        version: 127.0.0.1
        cassandra:
          version: 2
        enabled: true
        name: 'Contrail'
        minimum_disk: 10
        original_token: 0
        data_dirs:
        - /var/lib/cassandra
        id: 1
        discovery:
          host: 127.0.0.1
        bind:
          host: 127.0.0.1
          port: 9042
          rpc_port: 9160
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
      web:
        version: 2.2
        enabled: True
        bind:
          address: 127.0.0.1
        analytics:
          host: 127.0.0.1
        master:
          host: 127.0.0.1
        cache:
          engine: redis
          host: 127.0.0.1
          port: 6379
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3
        identity:
          engine: keystone
          version: '2.0'
          host: 127.0.0.1
          port: 35357
          user: admin
          password: password
          token: token
          tenant: admin

Analytic nodes

Analytics and database on an analytic node(s)

.. code-block:: yaml

    opencontrail:
      common:
        version: 2.2
        identity:
          engine: keystone
          host: 127.0.0.1
          port: 35357
          token: token
          password: password
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
      collector:
        version: 2.2
        enabled: true
        bind:
          address: 127.0.0.1
        master:
          host: 127.0.0.1
        discovery:
          host: 127.0.0.1
        data_ttl: 1
        database:
          members:
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
          - host: 127.0.0.1
            port: 9160
      database:
        version: 2.2
        cassandra:
          version: 2
        enabled: true
        name: 'Contrail'
        minimum_disk: 10
        original_token: 0
        data_dirs:
        - /var/lib/cassandra
        id: 1
        discovery:
          host: 127.0.0.1
        bind:
          host: 127.0.0.1
          port: 9042
          rpc_port: 9160
        members:
        - host: 127.0.0.1
          id: 1
        - host: 127.0.0.1
          id: 2
        - host: 127.0.0.1
          id: 3


Compute nodes
-------------

Vrouter configuration on a compute node(s)

.. code-block:: yaml

    opencontrail:
      common:
        version: 2.2
        identity:
          engine: keystone
          host: 127.0.0.1
          port: 35357
          token: token
          password: password
        network:
          engine: neutron
          host: 127.0.0.1
          port: 9696
      compute:
        version: 2.2
        enabled: True
        hostname: node-12.domain.tld
        discovery:
          host: 127.0.0.1
        interface:
          address: 127.0.0.1
          dev: eth0
          gateway: 127.0.0.1
          mask: /24
          dns: 127.0.0.1
          mtu: 9000


Compute nodes with gateway_mode
-------------------------------

Gateway mode: can be server/ vcpe (default is none)

.. code-block:: yaml

    opencontrail:
      compute:
        gateway_mode: server

TSN nodes
---------

Configure TSN nodes

.. code-block:: yaml

  opencontrail:
    compute:
      enabled: true
      tor:
        enabled: true
        bind:
          port: 8086
        agent:
          tor01:
            id: 0
            port: 6632
            host: 127.0.0.1
            address: 127.0.0.1


Set up metadata secret for the Vrouter
--------------------------------------

In order to get cloud-init within the instance to properly fetch
instance metadata, metadata_proxy_secret in the Vrouter agent config
should match the value in nova.conf. The administrator should define
it in the pillar:

.. code-block:: yaml

    opencontrail:
      compute:
        metadata:
          secret: opencontrail

Add auth info for Barbican on compute nodes
-------------------------------------------

.. code-block:: yaml

    opencontrail:
      compute:
        lbaas:
          enabled: true
          secret_manager:
            engine: barbican
            identity:
              user: admin
              password: "supersecretpassword123"
              tenant: admin


Keystone v3
-----------

To enable support for keystone v3 in opencontrail, there must be defined
version for config and web role.

.. code-block:: yaml

    opencontrail:
      config:
        version: 2.2
        enabled: true
        ...
        identity:
          engine: keystone
          version: '3'
        ...

    opencontrail:
      web:
        version: 2.2
        enabled: true
        ...
        identity:
          engine: keystone
          version: '3'
        ...

Without Keystone
----------------

.. code-block:: yaml

    opencontrail:
      ...
      common:
        ...
        identity:
          engine: none
          token: none
          password: none
        ...
      config:
        ...
        identity:
          engine: none
          password: none
          token: none
        ...
      web:
        ...
        identity:
          engine: none
          password: none
          token: none
        ...

Kubernetes support
------------------

Kubernetes vrouter nodes

Vrouter configuration on a kubernetes node(s)

.. code-block:: yaml

    opencontrail:
      ...
      compute:
        engine: kubernetes
      ...

vRouter with separated control plane

Separate XMPP traffic from dataplane interface.

.. code-block:: yaml

    opencontrail:
      compute:
        bind:
          address: 172.16.0.50
      ...

Override RPF default in Contrail API
------------------------------------

From MCP1.1 with OpenContrail >= 3.1.1 you can override RPF default for newly
created virtual networks. This can be useful for usecases like running
Calico and K8S in overlay. The `override_rpf_default_by` has valid values
`disable`, `enable`. If not defined, the configuration fallbacks to Contrail
default - currently `enable`.

.. code-block:: yaml

    opencontrail:
      ...
      config:
        override_rpf_default_by: 'disable'
      ...

Cassandra GC logging
--------------------

From Contrail version 3 you can set a way you want to handle Cassandra GC logs.
The behavior is controlled by `cassandra_gc_logging`. Valid values are
'rotation' (default), 'legacy' and false.

- 'rotation' is supported by JDK 6u34 7u2 or later and handles rotation of log
files automatically.
- 'legacy' is a way to support older JDKs and you will need to handle logs by
other means. This can be handled for example by using
`- service.opencontrail.database.cassandra_log_cleanup` in your reclass model.
- false will disable the cassandra gc logging

.. code-block:: yaml

    opencontrail:
      ...
      database:
        cassandra_gc_logging: false
      ...


Disable Contrail API authentication
-----------------------------------

Contrail version must >= 3.0. It is useful especially for Keystone v3.

.. code-block:: yaml

    opencontrail:
      ...
      config:
        multi_tenancy: false
      ...

Switch from on demand to periodic keystone sync
-----------------------------------------------

This can be useful when you want to sync projects from OpenStack to Contrail
automatically. The period of sync is 60s.

.. code-block:: yaml

    opencontrail:
      ...
      config:
        identity:
          sync_on_demand: false
      ...

Cassandra listen interface
--------------------------

.. code-block:: yaml

    database:
      ....
      bind:
        interface: eth0
        port: 9042
        rpc_port: 9160
      ....

OpenContrail WebUI version >= 3.1.1
-----------------------------------
For OpenContrail version >= 3.1.1 and Cassandra >= 2.1 we should override WebUI's cassandra port from 9160 to 9042.

For appropriate node at class level:

.. code-block:: yaml

    opencontrail:
      ....
      web:
        database:
          port: 9042
      ....


RabbitMQ HA hosts
------------------

.. code-block:: yaml

    opencontrail:
      config:
        message_queue:
          engine: rabbitmq
          members:
            - host: 10.0.16.1
            - host: 10.0.16.2
            - host: 10.0.16.3
          port: 5672

.. code-block:: yaml

    database:
      ....
      bind:
        interface: eth0
        port: 9042
        rpc_port: 9160
      ....

DPDK vRouter
-------------

.. code-block:: yaml

    opencontrail:
      compute:
        dpdk:
          enabled: true
          taskset: "0x0000003C00003C"
          socket_mem: "1024,1024"
        interface:
          mac_address: 90:e2:ba:7c:22:e1
          pci: 0000:81:00.1
      ...

Increase number of alarm-gen workers
------------------------------------

Port prefix will increment used ports by workers starting with 5901.

.. code-block:: yaml

    collector:
      alarm_gen:
        workers: 1
        port_prefix: 59

Contrail client
---------------

Basic parameters with identity and host configs

.. code-block:: yaml

  opencontrail:
    client:
      identity:
        user: admin
        project: admin
        password: adminpass
        host: keystone_host
      config:
        host: contrail_api_host
        port: contrail_api_ort

Enforcing virtual routers

.. code-block:: yaml

  opencontrail:
    client:
      ...
      virtual_router:
        cmp01:
          ip_address: 172.16.0.11
          dpdk_enabled: True
        cmp02:
          ip_address: 172.16.0.12
          dpdk_enabled: True

Enforcing global vrouter config

.. code-block:: yaml

  opencontrail:
    client:
      ...
      global_vrouter_config:
        name: global-vrouter-config
        parent_type: global-system-config
        encap_priority: "MPLSoUDP,MPLSoGRE"
        vxlan_vn_id_mode: automatic
        fq_names:
          - 'default-global-system-config'
          - 'default-global-vrouter-config'

Enforcing control nodes

.. code-block:: yaml

  opencontrail:
    client:
      ...
      bgp_router:
        ntw01:
          type: control-node
          ip_address: 172.16.0.11
        nwt02:
          type: control-node
          ip_address: 172.16.0.12
        nwt03:
          type: control-node
          ip_address: 172.16.0.13


Enforcing edge BGP routers

.. code-block:: yaml

  opencontrail:
    client:
      ...
      bgp_router:
        mx01:
          type: router
          ip_address: 172.16.0.21
          asn: 64512
        mx02:
          type: router
          ip_address: 172.16.0.22
          asn: 64512

Enforcing config nodes

.. code-block:: yaml

  opencontrail:
    client:
      ...
      config_node:
        ctl01:
          ip_address: 172.16.0.21
        ctl02:
          ip_address: 172.16.0.22

Enforcing database nodes

.. code-block:: yaml

  opencontrail:
    client:
      ...
      database_node:
        ntw01:
          ip_address: 172.16.0.21
        ntw02:
          ip_address: 172.16.0.22

Enforcing analytics nodes

.. code-block:: yaml

  opencontrail:
    client:
      ...
      analytics_node:
        nal01:
          ip_address: 172.16.0.31
        nal02:
          ip_address: 172.16.0.32

Enforcing Link Local Services

.. code-block:: yaml

  opencontrail:
    client:
      ...
      linklocal_service:
         # example with dns name address (only one permited)
         meta1:
           lls_ip: 10.0.0.23
           lls_port: 80
           ipf_addresses: "meta.example.com"
           ipf_port: 80
         # example with multiple ip addresses
         meta2:
           lls_ip: 10.0.0.23
           lls_port: 80
           ipf_addresses:
           - 10.10.10.10
           - 10.20.20.20
           - 10.30.30.30
           ipf_port: 80
         # example with one ip address
         meta3:
           lls_ip: 10.0.0.23
           lls_port: 80
           ipf_addresses:
           - 10.10.10.10
           ipf_port: 80
         # example with name override
         lls_meta4:
           name: meta4
           lls_ip: 10.0.0.23
           lls_port: 80
           ipf_addresses:
           - 10.10.10.10
           ipf_port: 80


Configuring OpenStack default quotasx

.. code-block:: yaml
    config:
      quota:
        network: 5
        subnet: 10
        router: 10
        floating_ip: 100
        secgroup: 1000
        secgroup_rule: 1000
        port: 1000
        pool: -1
        member: -1
        health_monitor: -1
        vip: -1

Enforcing physical routers
h
.. code-block:: yaml

  opencontrail:
    client:
      ...
      physical_router:
        router1:
          name: router1
          dataplane_ip: 1.2.3.4
          management_ip: 1.2.3.4
          vendor_name: ovs
          product_name: ovs
          agents:
           - tsn0-0
           - tsn0

Enforcing physical/logical interfaces for routers


.. code-block:: yaml

  opencontrail
    client:
    ...
    physical_router:
      router1:
        ...
        interface:
          port1:
            name: port1
            logical_interface:
              port1_l:
                name: 'port1.0'
                vlan_tag: 0
                interface_type: L2
                virtual_machine_interface:
                  port1_port:
                    name: port1_port
                    ip_address: 192.168.90.107
                    mac_address: '2e:92:a8:af:c2:21'
                    security_group: 'default'
                    virtual_network: 'virtual-network'


Contrail DNS custom forwarders
------------------------------

By default Contrail uses the /etc/resolv.conf file to determine the upstream DNS servers.
This can have some side-affects, like resolving internal DNS entries on you public instances.

In order to overrule this default set, you can configure nameservers using pillar data.
The formula is then responsible for configuring and generating a alternate resolv.conf file.

Note: this has been patched recently in the Contrail distribution of Mirantis:
https://github.com/Mirantis/contrail-controller/commit/ed9a25ccbcfebd7d079a93aecc5a1a7bf1265ea4
https://github.com/Mirantis/contrail-controller/commit/94c844cf2e9bcfcd48587aec03d10b869e737ade


To change forwarders for the default-dns option (which is handled by compute nodes):

.. code-block:: yaml

    compute:
      ....
      dns:
        forwarders:
        - 8.8.8.8
        - 8.8.4.4
      ....

To change forwarders for vDNS zones (handled by control nodes):

.. code-block:: yaml

    control:
      ....
      dns:
        forwarders:
        - 8.8.8.8
        - 8.8.4.4
      ....


Usage
=====

Basic installation
------------------

Add control BGP

.. code-block:: bash

    python /etc/contrail/provision_control.py --api_server_ip 192.168.1.11 --api_server_port 8082 --host_name network1.contrail.domain.com --host_ip 192.168.1.11 --router_asn 64512

Install compute node

.. code-block:: bash

    yum install contrail-vrouter contrail-openstack-vrouter

    salt-call state.sls nova,opencontrail

Add virtual router

.. code-block:: bash

    python /etc/contrail/provision_vrouter.py --host_name hostnode1.intra.domain.com --host_ip 10.0.100.101 --api_server_ip 10.0.100.30 --oper add --admin_user admin --admin_password cloudlab --admin_tenant_name admin

    /etc/sysconfig/network-scripts/ifcfg-bond0 -- comment GATEWAY,NETMASK,IPADDR

    reboot

Debugging
---------

Display vhost XMPP connection status

You should see the correct controller_ip and state should be established.

    http://<compute-node>:8085/Snh_AgentXmppConnectionStatusReq?

Display vrouter interface status

When vrf_name = ---ERROR--- then something goes wrong

    http://<compute-node>:8085/Snh_ItfReq?name=

Display IF MAP table

Look for neighbours, if VM has 2, it's ok

	http://<control-node>:8083/Snh_IFMapTableShowReq?table_name=

Trace XMPP requests

	http://<compute-node>:8085/Snh_SandeshTraceRequest?x=XmppMessageTrace


Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use Github issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-opencontrail/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

    https://github.com/salt-formulas/salt-formula-opencontrail

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net

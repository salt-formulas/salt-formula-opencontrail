opencontrail:
  common:
    version: 4.0
    config_only: true
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
    version: 4.0
    config_only: true
    enabled: true
    bind:
      address: 127.0.0.1
    master:
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
    analytics:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
    message_queue:
      host: 127.0.0.1
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
    config:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
  database:
    version: 4.0
    config_only: true
    cassandra:
      version: 2
    enabled: true
    name: 'Contrail'
    minimum_disk: 10
    original_token: 0
    data_dirs:
    - /var/lib/cassandra
    id: 1
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
    analytics:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1

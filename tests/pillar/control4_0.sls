opencontrail:
  common:
    version: 4.0
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
    version: 4.0
    enabled: true
    api:
      host: 127.0.0.1
    network:
      engine: neutron
      host: 127.0.0.1
      port: 9696
    analytics:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
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
    list_optimization_enabled: true
  control:
    version: 4.0
    enabled: true
    name: ntw-01
    bind:
      address: 127.0.0.1
    analytics:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
    message_queue:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
    database:
      members:
      - host: 127.0.0.1
      - host: 127.0.0.1
      - host: 127.0.0.1
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
    version: 4.0
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
  web:
    version: 4.0
    enabled: True
    network:
      host: 127.0.0.1
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

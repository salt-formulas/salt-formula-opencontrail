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
    api:
      host: 127.0.0.1
    enabled: true
    network:
      engine: neutron
      host: 127.0.0.1
      port: 9696
    discovery:
      host: 127.0.0.1
    analytics:
      members:
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
  control:
    name: ntw-01
    version: 4.0
    enabled: true
    config_only: True
    bind:
      address: 127.0.0.1
    analytics:
      members:
      - host: 127.0.0.1
    message_queue:
      members:
      - host: 127.0.0.1
    database:
      members:
      - host: 127.0.0.1
    master:
      host: 127.0.0.1
    members:
    - host: 127.0.0.1
      id: 1
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
    enabled: true
    bind:
      address: 127.0.0.1
    master:
      host: 127.0.0.1
    data_ttl: 2
    database:
      members:
      - host: 127.0.0.1
        port: 9160
    analytics:
      members:
      - host: 127.0.0.1
    message_queue:
      host: 127.0.0.1
      members:
      - host: 127.0.0.1
    config:
      members:
      - host: 127.0.0.1
  database:
    version: 4.0
    cassandra:
      version: 2
    enabled: true
    minimum_disk: 10
    name: 'Contrail'
    original_token: 0
    data_dirs:
    - /var/lib/cassandra
    id: 1
    config_only: True
    analytics:
      members:
      - host: 127.0.0.1
    bind:
      host: 127.0.0.1
      port: 9042
      rpc_port: 9160
    members:
    - host: 127.0.0.1
      id: 1
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
    identity:
      engine: keystone
      version: '2.0'
      host: 127.0.0.1
      port: 35357
      user: admin
      password: password
      token: token
      tenant: admin

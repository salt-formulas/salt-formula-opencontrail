parameters:
  _param:
    apt_mk_version: stable
  linux:
    system:
      repo:
        mirantis_openstack:
          source: "deb http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }} mitaka main"
          architectures: amd64
          key_url: "http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }}/archive-mcpmitaka.key"
          pin:
          - pin: 'release a=mitaka'
            priority: 1100
            package: '*'
        mirantis_openstack_hotfix:
          source: "deb http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }} mitaka-hotfix main"
          architectures: amd64
          key_url: "http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }}/archive-mcpmitaka.key"
          pin:
          - pin: 'release a=mitaka-hotfix'
            priority: 1100
            package: '*'
        mirantis_openstack_security:
          source: "deb http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }} mitaka-security main"
          architectures: amd64
          key_url: "http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }}/archive-mcpmitaka.key"
          pin:
          - pin: 'release a=mitaka-security'
            priority: 1100
            package: '*'
        mirantis_openstack_updates:
          source: "deb http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }} mitaka-updates main"
          architectures: amd64
          key_url: "http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }}/archive-mcpmitaka.key"
          pin:
          - pin: 'release a=mitaka-uptades'
            priority: 1100
            package: '*'
        mirantis_openstack_holdback:
          source: "deb http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }} mitaka-holdback main"
          architectures: amd64
          key_url: "http://mirror.fuel-infra.org/mcp-repos/mitaka/{{ grains.get('oscodename') }}/archive-mcpmitaka.key"
          pin:
          - pin: 'release a=mitaka-holdback'
            priority: 1100
            package: '*'
        mk_openstack:
          source: "deb [arch=amd64] http://apt.mirantis.com/{{ grains.get('oscodename') }}/ ${_param:apt_mk_version} mitaka"
          architectures: amd64
          key_url: "http://apt.mirantis.com/public.gpg"
          pin:
          - pin: 'release a=${_param:apt_mk_version}'
            priority: 1100
            package: '*'

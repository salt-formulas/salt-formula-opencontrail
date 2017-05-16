linux:
  system:
    enabled: true
    repo:
      mcp_opencontrail_repo:
        source: "deb [arch=amd64] http://apt-mk.mirantis.com/{{ grains.get('oscodename') }}/ stable oc311 extra"
        architectures: amd64
        key_url: "http://apt-mk.mirantis.com/public.gpg"
        pin:
        - pin: 'release a=stable'
          priority: 1100
          package: '*'
      opencontrail_team:
        source: "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu {{ grains.get('oscodename') }} main"
      opencontrail_extra:
        source: "deb http://ppa.launchpad.net/mirantis-opencontrail/extra/ubuntu trusty main"
      openjdk-r_repo:
        source: "deb http://ppa.launchpad.net/openjdk-r/ppa/ubuntu {{ grains.get('oscodename') }} main"
      opencontrail_311:
        source: "deb http://ppa.launchpad.net/mirantis-opencontrail/opencontrail-3.1.1/ubuntu {{ grains.get('oscodename') }} main "

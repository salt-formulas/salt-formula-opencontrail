linux:
  system:
    enabled: true
    repo:
      mcp_opencontrail_repo:
        source: "deb [arch=amd64] http://apt.mirantis.com/{{ grains.get('oscodename') }}/ nightly oc311 extra"
        architectures: amd64
        key_url: "http://apt.mirantis.com/public.gpg"
        pin:
        - pin: 'release a=nightly'
          priority: 1100
          package: '*'
    package:
      librdkafka1:
        version: 0.9.0-0contrail0
        hold: true
      python-kafka:
        version: 1.0.1-0contrail1
        hold: true

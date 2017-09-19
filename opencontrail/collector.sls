{%- from "opencontrail/map.jinja" import collector with context %}
{%- if collector.enabled %}

include:
- opencontrail.common

opencontrail_collector_packages:
  pkg.installed:
  - names: {{ collector.pkgs }}
  - force_yes: True

/etc/contrail/contrail-analytics-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-analytics-nodemgr.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-alarm-gen.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-alarm-gen.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-snmp-collector.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-snmp-collector.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-topology.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-topology.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

{{ collector.redis_config }}:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/collector/redis.conf
  - makedirs: True
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-collector.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-collector.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-query-engine.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-query-engine.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

/etc/contrail/contrail-analytics-api.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-analytics-api.conf
  - template: jinja
  - require:
    - pkg: opencontrail_collector_packages

{%- if collector.version >= 3.0 and grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_analytics_files/contrail-analytics-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/collector/contrail-analytics-nodemgr.ini
  - makedirs: True
  - require:
    - pkg: opencontrail_collector_packages
  - require_in:
    - service: opencontrail_collector_services

/etc/contrail/supervisord_analytics.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/collector/supervisord_analytics.conf
  - require:
    - pkg: opencontrail_collector_packages
  - require_in:
    - service: opencontrail_collector_services

{%- endif %}

opencontrail_collector_services:
  service.running:
  - enable: true
  - names: {{ collector.services }}
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: /etc/contrail/contrail-analytics-api.conf
    - file: /etc/contrail/contrail-query-engine.conf
    - file: /etc/contrail/contrail-collector.conf
    - file: {{ collector.redis_config }}
    - file: /etc/contrail/contrail-topology.conf
    - file: /etc/contrail/contrail-snmp-collector.conf
    - file: /etc/contrail/contrail-analytics-nodemgr.conf
    - file: /etc/contrail/contrail-alarm-gen.conf

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_collector_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.collector
  - mode: 755

{%- endif %}

{%- endif %}

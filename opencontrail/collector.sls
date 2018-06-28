{%- from "opencontrail/map.jinja" import collector with context %}
{%- if collector.enabled %}

include:
- opencontrail.common

{%- if not collector.get('config_only', False) %}
opencontrail_collector_packages:
  pkg.installed:
  - names: {{ collector.pkgs }}
  - force_yes: True
  - require_in:
    - file: /etc/contrail/contrail-analytics-nodemgr.conf
    - file: /etc/contrail/contrail-alarm-gen.conf
    - file: /etc/contrail/contrail-snmp-collector.conf
    - file: /etc/contrail/contrail-topology.conf
    - file: {{ collector.redis_config }}
    - file: /etc/contrail/contrail-collector.conf
    - file: /etc/contrail/contrail-query-engine.conf
    - file: /etc/contrail/contrail-analytics-api.conf
    {%- if collector.version >= 3.0 and grains.get('init') != 'systemd' %}
    - file: /etc/contrail/supervisord_analytics_files/contrail-analytics-nodemgr.ini
    - file: /etc/contrail/supervisord_analytics.conf
    {%- endif %}
{%- endif %}

/etc/contrail/contrail-analytics-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-analytics-nodemgr.conf
  - template: jinja

/etc/contrail/contrail-alarm-gen.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-alarm-gen.conf
  - template: jinja

/etc/contrail/contrail-snmp-collector.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-snmp-collector.conf
  - template: jinja

/etc/contrail/contrail-topology.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-topology.conf
  - template: jinja

{{ collector.redis_config }}:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/redis.conf
  - template: jinja
  - makedirs: True

/etc/contrail/contrail-collector.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-collector.conf
  - template: jinja

/etc/contrail/contrail-query-engine.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-query-engine.conf
  - template: jinja

/etc/contrail/contrail-analytics-api.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-analytics-api.conf
  - template: jinja

{%- if collector.version >= 4.0 and collector.identity.engine == "keystone" %}
/etc/contrail/contrail-keystone-auth.conf_analytics:
  file.managed:
  - name: /etc/contrail/contrail-keystone-auth.conf
  - source: salt://opencontrail/files/{{ collector.version }}/collector/contrail-keystone-auth.conf
  - template: jinja
{%- endif %}

{%- if collector.version == 3.0 %}

/etc/contrail/supervisord_analytics_files/contrail-analytics-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/collector/contrail-analytics-nodemgr.ini
  - makedirs: True

/etc/contrail/supervisord_analytics.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/collector/supervisord_analytics.conf

/etc/contrail/supervisord_analytics_files/contrail-alarm-gen.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ collector.version }}/contrail-alarm-gen.ini
  - makedirs: True
  - template: jinja

{%- endif %}

{%- if not collector.get('config_only', False) %}

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
    {%- if collector.version == 3.0 %}
    - file: /etc/contrail/supervisord_analytics_files/contrail-analytics-nodemgr.ini
    - file: /etc/contrail/supervisord_analytics.conf
    - file: /etc/contrail/supervisord_analytics_files/contrail-alarm-gen.ini
    {%- endif %}

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_collector_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.collector
  - mode: 755

{%- endif %}

{%- else %}
{%- if collector.container_name is defined %}
{%- if grains['saltversioninfo'] < [2017, 7] %}
  {% set docker_module = 'dockerng' %}
{%- else %}
  {% set docker_module = 'docker' %}
{%- endif %}
{%- if salt['{{ docker_module }}.exists'](collector.container_name) %}
opencontrail_collector_dockerng_services:
  dockerng_service.running:
  - services: {{ collector.services }}
  - container: {{ collector.container_name }}
  - watch:
    - file: /etc/contrail/contrail-analytics-api.conf
    - file: /etc/contrail/contrail-query-engine.conf
    - file: /etc/contrail/contrail-collector.conf
    - file: {{ collector.redis_config }}
    - file: /etc/contrail/contrail-topology.conf
    - file: /etc/contrail/contrail-snmp-collector.conf
    - file: /etc/contrail/contrail-analytics-nodemgr.conf
    - file: /etc/contrail/contrail-alarm-gen.conf
{%- endif %}
{%- endif %}
{%- endif %}

{%- endif %}

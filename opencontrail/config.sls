{%- from "opencontrail/map.jinja" import common,config with context %}
{%- if config.enabled %}

include:
- opencontrail.common

opencontrail_config_packages:
  pkg.installed:
  - names: {{ config.pkgs }}
  - force_yes: True

{% if config.version == 2.2 or config.version == 3.0 %}

/etc/ifmap-server/authorization.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/authorization.properties
  - require:
    - pkg: opencontrail_config_packages

/etc/ifmap-server/publisher.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/publisher.properties
  - unless: test -e /etc/ifmap-server/deployed
  - require:
    - pkg: opencontrail_config_packages

publisher_init:
  cmd.run:
  - name: touch /etc/ifmap-server/deployed
  - unless: test -e /etc/ifmap-server/deployed
  - require:
    - pkg: opencontrail_config_packages

/etc/ifmap-server/log4j.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/log4j.properties
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

/etc/ifmap-server/basicauthusers.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/basicauthusers.properties
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

{%- if grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_config_files/contrail-discovery.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail-discovery.ini
  - makedirs: true
  - require:
    - pkg: opencontrail_config_packages

/etc/init.d/contrail-discovery:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail-discovery
  - require:
    - pkg: opencontrail_config_packages

{%- endif %}

/etc/contrail/contrail-discovery.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-discovery.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

{%- endif %}

{%- if grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_config_files/contrail-api.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail-api.ini
  - makedirs: true
  - require:
    - pkg: opencontrail_config_packages

/etc/init.d/contrail-api:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail-api
  - require:
    - pkg: opencontrail_config_packages

{%- endif %}

/etc/contrail/contrail-api.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-api.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

/etc/contrail/vnc_api_lib.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/vnc_api_lib.ini
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

/etc/contrail/contrail-device-manager.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-device-manager.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages
  - watch_in:
    - service: opencontrail_config_services

/etc/contrail/contrail-config-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-config-nodemgr.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages
  - watch_in:
    - service: opencontrail_config_services

/etc/sudoers.d/contrail_sudoers:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail_sudoers
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

{%- if config.identity.engine == "keystone" %}
/etc/contrail/contrail-keystone-auth.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-keystone-auth.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages
  - watch_in:
    - service: opencontrail_config_services
{%- endif %}

/etc/contrail/contrail-schema.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-schema.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

/etc/contrail/contrail-svc-monitor.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/contrail-svc-monitor.conf
  - template: jinja
  - require:
    - pkg: opencontrail_config_packages

{%- if config.version >= 3.0 and grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_config_files/contrail-config-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/contrail-config-nodemgr.ini
  - require:
    - pkg: opencontrail_config_packages
  - require_in:
    - service: opencontrail_config_services

{%- if not grains.get('virtual_subtype', None) == "Docker" %}
{%- if not common.vendor == "juniper" %}

/etc/contrail/supervisord_config_files/ifmap.ini:
  file.absent:
  - require:
    - pkg: opencontrail_config_packages
  - require_in:
    - service: opencontrail_config_services

{%- endif %}
{%- endif %}

/etc/contrail/supervisord_config.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ config.version }}/config/supervisord_config.conf
  - require:
    - pkg: opencontrail_config_packages
  - require_in:
    - service: opencontrail_config_services

{%- endif %}

opencontrail_config_services:
  service.running:
  - enable: true
  - names: {{ config.services }}
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    {%- if config.version <= 3.0 %}
    - file: /etc/contrail/contrail-discovery.conf
    - file: /etc/ifmap-server/basicauthusers.properties
    {%- endif %}
    - file: /etc/contrail/contrail-svc-monitor.conf
    - file: /etc/contrail/contrail-schema.conf
    - file: /etc/contrail/contrail-api.conf
    - file: /etc/contrail/vnc_api_lib.ini
    - file: /etc/sudoers.d/contrail_sudoers

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_config_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.config
  - mode: 755

{%- endif %}

{%- endif %}

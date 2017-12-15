{%- from "opencontrail/map.jinja" import control with context %}
{%- if control.enabled %}

include:
- opencontrail.common

{%- if not control.get('config_only', False) %}
opencontrail_control_packages:
  pkg.installed:
  - names: {{ control.pkgs }}
  - force_yes: True
  - require_in:
    - /etc/contrail/contrail-control-nodemgr.conf
    - /etc/contrail/contrail-control.conf
    - /etc/contrail/contrail-dns.conf
    - /etc/contrail/dns
    - /etc/contrail/dns/contrail-rndc.conf
    {%- if control.version >= 3.0 and grains.get('init') != 'systemd' %}
    - /etc/contrail/supervisord_control_files/contrail-control-nodemgr.ini
    - /etc/contrail/supervisord_control.conf
    {%- endif %}
{%- endif %}

/etc/contrail/contrail-control-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-control-nodemgr.conf
  - template: jinja

/etc/contrail/contrail-control.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-control.conf
  - template: jinja

/etc/contrail/contrail-dns.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-dns.conf
  - template: jinja

{%- if control.get('config_only', False) %}

user_contrail:
  user.present:
    - name: contrail
    - system: True
    - require_in:
      - /etc/contrail/dns

opencontrail_control_doctrail:
  file.managed:
  - name: /usr/bin/doctrail
  - template: jinja
  - source: salt://opencontrail/files/{{ control.version }}/doctrail
  - mode: 755

{% endif %}

/etc/contrail/dns:
  file.directory:
  - user: contrail
  - group: contrail

/etc/contrail/dns/contrail-rndc.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/contrail-rndc.conf
  - makedirs: True

{%- if control.version == 3.0 and control.get('dns', {}).get('forwarders', False) ) %}
contrail_control_resolv:
  file.managed:
  - name: /etc/contrail/resolv.conf
  - source: salt://opencontrail/files/{{ control.version }}/resolv.conf
  - template: jinja
  - defaults:
      dns: {{ control.get('dns', {})|yaml }}
  - require:
    - file: /etc/contrail
{%- endif %}

{%- if control.version >= 3.0 and grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_control_files/contrail-control-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/contrail-control-nodemgr.ini
  - makedirs: true

/etc/contrail/supervisord_control.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/supervisord_control.conf

{%- endif %}

{%- if not control.get('config_only', False) %}
opencontrail_control_services:
  service.running:
  - enable: true
  - names: {{ control.services }}
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: /etc/contrail/dns/contrail-rndc.conf
    - file: /etc/contrail/contrail-dns.conf
    - file: /etc/contrail/contrail-control.conf
    - file: /etc/contrail/contrail-control-nodemgr.conf
  - require:
    - /etc/contrail/supervisord_control_files/contrail-control-nodemgr.ini
    - /etc/contrail/supervisord_control.conf

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_control_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.control
  - mode: 755
{%- endif %}

{%- endif %}

{%- endif %}

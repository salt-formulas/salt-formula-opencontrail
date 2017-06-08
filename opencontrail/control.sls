{%- from "opencontrail/map.jinja" import control with context %}
{%- if control.enabled %}

include:
- opencontrail.common

opencontrail_control_packages:
  pkg.installed:
  - names: {{ control.pkgs }}
  - force_yes: True

/etc/contrail/contrail-control-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-control-nodemgr.conf
  - template: jinja
  - require:
    - pkg: opencontrail_control_packages

/etc/contrail/contrail-control.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-control.conf
  - template: jinja
  - require:
    - pkg: opencontrail_control_packages

/etc/contrail/contrail-dns.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/contrail-dns.conf
  - template: jinja
  - require:
    - pkg: opencontrail_control_packages

/etc/contrail/dns:
  file.directory:
  - user: contrail
  - group: contrail
  - require:
    - pkg: opencontrail_control_packages

/etc/contrail/dns/contrail-rndc.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/contrail-rndc.conf
  - require:
    - pkg: opencontrail_control_packages

{% if control.version == 3.0 %}

/etc/contrail/supervisord_control_files/contrail-control-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/contrail-control-nodemgr.ini
  - makedirs: true
  - require:
    - pkg: opencontrail_control_packages
  - require_in:
    - service: opencontrail_control_services

/etc/contrail/supervisord_control.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ control.version }}/control/supervisord_control.conf
  - require:
    - pkg: opencontrail_control_packages
  - require_in:
    - service: opencontrail_control_services

{% endif %}

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

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_control_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.control
  - mode: 755

{%- endif %}

{%- endif %}


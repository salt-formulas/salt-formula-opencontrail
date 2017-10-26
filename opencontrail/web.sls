{%- from "opencontrail/map.jinja" import web with context %}
{%- if web.enabled %}

{%- if not web.get('config_only', False) %}
opencontrail_web_packages:
  pkg.installed:
  - names: {{ web.pkgs }}
  - force_yes: True
  - require_in:
    - /etc/contrail/contrail-webui-userauth.js
    - /etc/contrail/config.global.js
{%- endif %}

/etc/contrail/config.global.js:
  file.managed:
  - source: salt://opencontrail/files/{{ web.version }}/config.global.js
  - template: jinja

/etc/contrail/contrail-webui-userauth.js:
  file.managed:
  - source: salt://opencontrail/files/{{ web.version }}/contrail-webui-userauth.js
  - template: jinja

{%- if not web.get('config_only', False) %}

opencontrail_web_services:
  service.running:
  - enable: true
  - names: {{ web.services }}
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: /etc/contrail/config.global.js
    - file: /etc/contrail/contrail-webui-userauth.js

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_web_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.web
  - mode: 755

{%- endif %}

{%- endif %}

{%- if web.version >= 4.0 and web.get('config_only', False) %}
/lib/systemd/system/contrail-webui-jobserver.service:
  file.managed:
  - source: salt://opencontrail/files/{{ web.version }}/contrail-webui-jobserver.service
  - template: jinja

/lib/systemd/system/contrail-webui-webserver.service:
  file.managed:
  - source: salt://opencontrail/files/{{ web.version }}/contrail-webui-webserver.service
  - template: jinja
{%- endif %}

{%- endif %}

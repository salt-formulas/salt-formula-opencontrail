{%- macro set_param(param_name, param_dict) -%}
{%- if param_dict.get(param_name, False) -%}
- {{ param_name }}: {{ param_dict[param_name] }}
{%- endif -%}
{%- endmacro -%}
{%- from "opencontrail/map.jinja" import compute with context %}
{%- from "linux/map.jinja" import network with context %}
{%- if compute.enabled %}

include:
- opencontrail.common

opencontrail_compute_packages:
  pkg.installed:
  - names: {{ compute.pkgs }}

{%- if grains.get('virtual_subtype', None) not in ['Docker', 'LXC'] %}

net.ipv4.ip_local_reserved_ports:
  sysctl.present:
    - value: 8085,9090
    - require:
      - pkg: opencontrail_compute_packages
    - require_in:
      - service: opencontrail_compute_services

{%- endif %}

{%- if compute.get('lbaas', {}).get('enabled', False) %}

{%- if compute.lbaas.get('secret_manager', {}).get('engine', 'noop') == 'barbican' %}

/etc/contrail/contrail-lbaas-auth.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-lbaas-auth.conf
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages

{%- endif %}

{%- endif %}

/etc/contrail/contrail-vrouter-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-vrouter-nodemgr.conf
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages
  - watch_in:
    - service: opencontrail_compute_services

{%- if compute.version <= 3.0 %}

/etc/contrail/vrouter_nodemgr_param:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/vrouter_nodemgr_param
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages

{%- if compute.version == 3.0 and compute.get('dns', {}).get('forwarders', False) ) %}
contrail_compute_resolv:
  file.managed:
  - name: /etc/contrail/resolv.conf
  - source: salt://opencontrail/files/{{ compute.version }}/resolv.conf
  - template: jinja
  - defaults:
      dns: {{ compute.get('dns', {})|yaml }}
  - require:
    - file: /etc/contrail
{%- endif %}

{%- endif %}

/etc/contrail/agent_param:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/agent_param
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages

/etc/contrail/contrail-vrouter-agent.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-vrouter-agent.conf
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages
  - watch_in:
    - service: opencontrail_compute_services

/usr/local/bin/findns:
  file.managed:
  - source: salt://opencontrail/files/findns
  - mode: 755

{%- if compute.version >= 3.0 %}

{%- if compute.version < 4.0 or grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_vrouter_files/contrail-vrouter-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-vrouter-nodemgr.ini
  - require:
    - pkg: opencontrail_compute_packages
  - require_in:
    - service: opencontrail_compute_services

{%- endif %}

/etc/udev/rules.d/vhost-net.rules:
  file.managed:
  - contents: 'KERNEL=="vhost-net", GROUP="kvm", MODE="0660"'
  - makedirs: True

/etc/modules:
  file.append:
  - text: "vhost-net"
  - require:
    - file: /etc/udev/rules.d/vhost-net.rules

{%- endif %}

{%- if compute.dpdk.enabled %}

opencontrail_vrouter_package:
  pkg.installed:
  - names:
    - contrail-vrouter-dpdk
    - contrail-vrouter-dpdk-init
    - contrail-vrouter-agent
  - require_in:
    - pkg: opencontrail_compute_packages

{%- if compute.version < 4.0 or grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_vrouter_files/contrail-vrouter-dpdk.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-vrouter-dpdk.ini
  - template: jinja
  - require:
    - pkg: opencontrail_compute_packages
    - pkg: opencontrail_vrouter_package
  - require_in:
    - service: opencontrail_compute_services

{%- endif %}

modules_dpdk:
  file.append:
  - name: /etc/modules
  - text: uio
  - require:
    - pkg: opencontrail_vrouter_package

/usr/lib/contrail/if-vhost0:
  file.managed:
  - contents: "# Phony script as nothing to do in DPDK vRouter case."

{%- else %}

opencontrail_vrouter_package:
  pkg.installed:
  - names:
    - contrail-vrouter-dkms
    - contrail-vrouter-agent
  - require_in:
    - pkg: opencontrail_compute_packages

/etc/modprobe.d/vrouter.conf:
  file.managed:
  - contents: "options vrouter vr_flow_entries=2097152"

{%- if network.interface.get('vhost0', {}).get('enabled', False) %}
{%- if grains.get('virtual_subtype', None) not in ['Docker', 'LXC'] %}

contrail_load_vrouter_kernel_module:
  cmd.run:
  - name: sync && echo 3 > /proc/sys/vm/drop_caches && echo 1 > /proc/sys/vm/compact_memory && modprobe vrouter
  - unless: "lsmod | grep vrouter"
  - cwd: /root
  - require:
    - pkg: opencontrail_compute_packages

{%- endif %}
{%- endif %}
{%- endif %}

{%- if compute.get('tor', {}).get('enabled', False) %}

{% for agent_name, agent in compute.tor.agent.iteritems() %}

/etc/contrail/contrail-tor-agent-{{ agent.id }}.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/contrail-tor-agent.conf
  - template: jinja
  - defaults:
      agent_name: {{ agent_name }}
  - watch_in:
    - service: opencontrail_compute_services

{%- if compute.version < 4.0 or grains.get('init') != 'systemd' %}

/etc/contrail/supervisord_vrouter_files/contrail-tor-agent-{{ agent.id }}.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ compute.version }}/tor/contrail-tor-agent.ini
  - template: jinja
  - defaults:
      agent_name: {{ agent_name }}
  - watch_in:
    - service: opencontrail_compute_services

{%- endif %}

{%- endfor %}
{%- endif %}

opencontrail_compute_services:
  service.running:
  - names: {{ compute.services }}
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}

{%- endif %}

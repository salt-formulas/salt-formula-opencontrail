{%- from "opencontrail/map.jinja" import test with context  %}
{%- if test.enabled %}

opencontrail_test_packages:
  pkg.installed:
    - names: {{ test.pkgs }}
    - force_yes: True

install_python_packages:
  pip.installed:
    - names:
      - pip
      - tox
      - setuptools
    - require:
      - pkg: opencontrail_test_packages

install_vapor_and_dependencies:
  pip.installed:
    - requirements: salt://opencontrail/files/test_files/requirements.txt
    - require:
      - pip: install_python_packages

{{ test.working_dir }}:
  file.directory:
    - user: root
    - group: root
    - dir_mode: 755
    - require:
      - pip: install_vapor_and_dependencies

clone_fuel_plugin_contrail:
  git.latest:
    - name: https://github.com/openstack/fuel-plugin-contrail.git
    - target: {{ test.working_dir }}/fuel-plugin-contrail
    - require:
      - file: {{ test.working_dir }}

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/roles.yaml:
  file.managed:
    - source: salt://opencontrail/files/test_files/roles.yaml
    - user: root
    - group: root
    - template: jinja
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/exports.sh:
  file.managed:
    - source: salt://opencontrail/files/test_files/exports.sh
    - user: root
    - group: root
    - template: jinja
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/os_faults.json:
  file.managed:
    - source: salt://opencontrail/files/test_files/os_faults.json
    - user: root
    - group: root
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/pytest.ini:
  file.managed:
    - source: salt://opencontrail/files/test_files/pytest.ini
    - user: root
    - group: root
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/requirements.txt:
  file.managed:
    - source: salt://opencontrail/files/test_files/requirements.txt
    - user: root
    - group: root
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/vapor/conftest.py:
  file.managed:
    - source: salt://opencontrail/files/test_files/conftest.py
    - user: root
    - group: root
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/keystonerc:
  file.managed:
    - source: salt://opencontrail/files/test_files/keystonerc
    - user: root
    - group: root
    - template: jinja
    - require:
      - git: clone_fuel_plugin_contrail

{{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/keystonercv3:
  file.managed:
    - source: salt://opencontrail/files/test_files/keystonercv3
    - user: root
    - group: root
    - template: jinja
    - require:
      - git: clone_fuel_plugin_contrail

{%- endif %}

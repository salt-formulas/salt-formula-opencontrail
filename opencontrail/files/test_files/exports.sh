{%- from "opencontrail/map.jinja" import test with context %}
#!/bin/bash
export OS_USERNAME=admin
export OS_PASSWORD={{ test.identity.admin_password }}
export OS_PROJECT_NAME=admin
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://{{ test.identity.bind.private_address }}:{{ test.identity.bind.private_port}}/
export VIRTUAL_DISPLAY=1

export OS_FAULTS_CLOUD_DRIVER=tcpcloud

export CONTRAIL_ROLES_DISTRIBUTION_YAML={{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/roles.yaml
export CONTRAIL_API_URL=http://{{ test.url.api }}:8082/
export CONTRAIL_ANALYTICS_URL=http://{{ test.url.analytics}}:8081/

export OS_FAULTS_CONFIG={{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/os_faults.json
export K_PARAM='not destructive'
export OPENRC_ACTIVATE_CMD='source {{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/keystonerc; source {{ test.working_dir }}/fuel-plugin-contrail/plugin_test/vapor/keystonercv3'

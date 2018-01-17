{%- from "opencontrail/map.jinja" import database,common  with context %}
{%- if database.enabled %}

include:
- opencontrail.common

{% if database.cassandra.version == 1 %}

{{ database.cassandra_config }}cassandra.yaml:
  file.managed:
  - source: salt://opencontrail/files/cassandra.yaml.1
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

{{ database.cassandra_config }}cassandra-env.sh:
  file.managed:
  - source: salt://opencontrail/files/cassandra-env.sh.1
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

{% else %}

{{ database.cassandra_config }}cassandra.yaml:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/cassandra.yaml
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

{% if database.version >= 4.0 %}

{{ database.cassandra_config }}cassandra_analytics.yaml:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/cassandra_analytics.yaml
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

/usr/share/kafka/config/consumer.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/consumer.properties
  - template: jinja
  - makedirs: true

/usr/share/kafka/config/zookeeper.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/zookeeper.properties
  - template: jinja
  - makedirs: true

{% endif %}

{{ database.cassandra_config }}logback.xml:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/database/logback.xml
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

{{ database.cassandra_config }}cassandra-env.sh:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/database/cassandra-env.sh
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}

{% if database.version >= 4.0 %}
{{ database.cassandra_config }}cassandra-env-analytics.sh:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/database/cassandra-env-analytics.sh
  - template: jinja
  - makedirs: True
{% if grains.os_family == "RedHat" %}
  - require:
    - pkg: opencontrail_database_packages
{% endif %}
{% endif %}

{% endif %}

{%- if database.get('config_only', False) %}
opencontrail_database_doctrail:
  file.managed:
  - name: /usr/bin/doctrail
  - template: jinja
  - source: salt://opencontrail/files/{{ database.version }}/doctrail
  - mode: 755
{% endif %}

{%- if not database.get('config_only', False) %}

opencontrail_database_packages:
  pkg.installed:
  - names: {{ database.pkgs }}
  - force_yes: True
  - require_in:
    - /etc/zookeeper/conf/log4j.properties
    - /etc/contrail/contrail-database-nodemgr.conf
    - /etc/zookeeper/conf/zoo.cfg
    - /etc/default/zookeeper
    {%- if database.version >= 3.0 %}
    - /usr/share/kafka/config/server.properties
    {%- if database.version < 4.0 or grains.get('init') != 'systemd' %}
    - /etc/contrail/supervisord_database_files/contrail-database-nodemgr.ini
    {%- endif %}
    {%- endif %}
{% if grains.os_family == "Debian" %}
  - require:
    - file: {{ database.cassandra_config }}cassandra.yaml
    - file: {{ database.cassandra_config }}cassandra-env.sh
    - file: {{ database.cassandra_config }}logback.xml
{% endif %}

{% endif %}

/etc/zookeeper/conf/log4j.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/database/log4j.properties
  - makedirs: true


/etc/contrail/contrail-database-nodemgr.conf:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/contrail-database-nodemgr.conf
  - template: jinja

/etc/zookeeper/conf/zoo.cfg:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/zoo.cfg
  - template: jinja
  - makedirs: true

/etc/default/zookeeper:
  file.managed:
    - source: salt://opencontrail/files/{{ database.version }}/zookeeper
    - template: jinja

{% if database.version >= 4.0 %}
/etc/zookeeper/conf/zoo_analytics.cfg:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/zoo_analytics.cfg
  - template: jinja
  - makedirs: true

/etc/default/zookeeper_analytics:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/zookeeper_analytics
  - template: jinja
{% endif %}

/var/lib/zookeeper/myid:
  file.managed:
  - contents: '{{ database.id }}'
  - makedirs: true

{%- if database.version >= 3.0 %}

/usr/share/kafka/config/server.properties:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/server.properties
  - template: jinja
  - makedirs: true

{%- if database.version < 4.0 or grains.get('init') != 'systemd' %}
{%- if not database.get('config_only', False) %}
/etc/contrail/supervisord_database_files/contrail-database-nodemgr.ini:
  file.managed:
  - source: salt://opencontrail/files/{{ database.version }}/database/contrail-database-nodemgr.ini
{%- endif %}
{%- endif %}
{%- endif %}

{%- if not database.get('config_only', False) %}
{% if grains.os_family == "Debian" %}
#Stop cassandra started by init script - replaced by contrail-database
disable-cassandra-service:
  service.dead:
    - name: cassandra
    - enable: None
{% endif %}
{% endif %}

{%- if not database.get('config_only', False) %}

/var/lib/cassandra/data:
  file.directory:
  - user: cassandra
  - group: cassandra
  - makedirs: True

/var/lib/cassandra:
  file.directory:
  - user: cassandra
  - group: cassandra
  - require:
    - file: /var/lib/cassandra/data

zookeeper_service:
  service.running:
  - enable: true
  - name: zookeeper
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: /etc/zookeeper/conf/zoo.cfg
    - file: /var/lib/zookeeper/myid
    - file: /etc/zookeeper/conf/log4j.properties

opencontrail_database_services:
  service.running:
  - enable: true
{%- if common.vendor == "juniper" or (database.version >= 4.0 and grains.get('init') == 'systemd') %}
  - name: contrail-database
{%- else %}
  - name: supervisor-database
{%- endif %}
  - init_delay: 5
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: {{ database.cassandra_config }}cassandra.yaml
    - file: {{ database.cassandra_config }}cassandra-env.sh
    - file: {{ database.cassandra_config }}logback.xml
    - file: /etc/zookeeper/conf/zoo.cfg
    - file: /etc/default/zookeeper
    - file: /etc/contrail/contrail-database-nodemgr.conf
    - file: /var/lib/zookeeper/myid
    - file: /etc/zookeeper/conf/log4j.properties
    - file: /var/lib/cassandra/data
    - file: /etc/contrail/supervisord_database_files/contrail-database-nodemgr.ini
    - file: /usr/share/kafka/config/server.properties

opencontrail_zookeeper_service:
  service.running:
  - enable: true
  - name: zookeeper
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    - file: /etc/zookeeper/conf/zoo.cfg
    - file: /etc/default/zookeeper
    - file: /etc/zookeeper/conf/log4j.properties
    - file: /etc/contrail/supervisord_database_files/contrail-database-nodemgr.ini
    - file: /usr/share/kafka/config/server.properties

{%- if grains.get('virtual_subtype', None) == "Docker" %}

opencontrail_database_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://opencontrail/files/entrypoint.sh.database
  - mode: 755

{%- endif %}

{%- else %}
{%- if database.container_name is defined %}
{%- if salt['dockerng.exists'](database.container_name) %}
opencontrail_database_dockerng_services:
  dockerng_service.running:
    - services:
      - contrail-database
      - kafka
      - contrail-database-nodemgr
      - zookeeper
    - container: {{ database.container_name }}
    - watch:
      - file: {{ database.cassandra_config }}cassandra.yaml
      - file: {{ database.cassandra_config }}cassandra-env.sh
      - file: {{ database.cassandra_config }}logback.xml
      - file: /etc/zookeeper/conf/zoo.cfg
      - file: /etc/default/zookeeper
      - file: /etc/contrail/contrail-database-nodemgr.conf
      - file: /var/lib/zookeeper/myid
      - file: /etc/zookeeper/conf/log4j.properties
      - file: /usr/share/kafka/config/server.properties
{%- endif %}

{%- endif %}

{%- endif %}

{%- endif %}

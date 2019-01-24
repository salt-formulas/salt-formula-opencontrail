/usr/local/bin/contrail-cassandra-backup:
  file.managed:
  - user: root
  - group: root
  - mode: 755
  - source: salt://opencontrail/files/contrail-cassandra-backup
  - template: jinja

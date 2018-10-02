{%- from "opencontrail/map.jinja" import control, config, collector, web, database, compute with context %}

{%- set extra_states_map = {} %}

{%- for data in [control, config, collector, web, database, compute] %}

{%- if data.get('enabled', False) %}
  {%- if data.get('services_extra_states', False) %}
    {% do extra_states_map.update(data.get('services_extra_states')) %}
  {%- endif %}
{%- endif %}

{%- endfor %}

contrail_services_health_check:
  contrail_health.services_health:
    - healthy_states: ['active']
    - extra_states_map: {{ extra_states_map }}

#!/usr/bin/python
# Copyright 2018 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Verification of Contrail services states
'''


def __virtual__():
    '''
    Load Contrail Health state module
    '''
    return 'contrail_health'


def services_health(name, healthy_states=None, extra_states_map=None):
    services_states = __salt__['contrail_health.get_services_status']()

    healthy_states = healthy_states or ['active']
    extra_states_map = extra_states_map or {}

    if services_states:

        nonhealthy_services = []

        for service_name, state in services_states.items():
            if (state not in healthy_states and
                    state not in extra_states_map.get(service_name, [])):
                nonhealthy_services.append(service_name)

        if nonhealthy_services:
            comment = ("The following services didn't pass health check:\n" +
                       "\n".join(nonhealthy_services))
            result = False
        else:
            comment = ("All contrail services have health state:\n" +
                       "\n".join(services_states.keys()))
            result = True

    else:
        comment = ("Contrail services were not found.\n"
                   "If contrail services are working inside container(s) "
                   "(starting from version 4.0), please check "
                   "that related container(s) is (are) started.")
        result = False

    return {'name': name, 'changes': {}, 'comment': comment, 'result': result}

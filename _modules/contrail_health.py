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
import os
import subprocess


def __virtual__():
    '''
    Only load this module if contrail-status or doctrail utility
    (in case of containerized contrail version) is available.
    '''
    if _is_cmd_available('contrail-status') or _is_cmd_available('doctrail'):
        return 'contrail_health'
    return False


def _is_cmd_available(cmd_name):
    try:
        with open(os.devnull) as devnull:
            subprocess.Popen(
                [cmd_name], stdout=devnull, stderr=devnull
            ).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def get_services_status():

    if _is_cmd_available('contrail-status'):
        status_cmd_list = ['contrail-status']
    else:
        status_cmd_list = ['doctrail', 'all', 'contrail-status']

    cs_out = str(subprocess.check_output(status_cmd_list))
    status_map = {}

    for line in cs_out.split('\n'):
        line_list = line.split()
        if (not line.startswith("==") and "FOR NODE" not in line and
                len(line_list) >= 2):
            status_map[line_list[0].split(":")[0]] = line_list[1]

    return status_map

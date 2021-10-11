#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
#

import pytest
import docker
from docker import DockerClient

from north import config
from north.auth import create_launch_token


@pytest.fixture(scope='function')
def docker_cleanup():
    '''
    A function scope fixture for using docker. It will try to remove all left-over containers
    after the test function.
    '''
    # Before the test code

    yield

    # Remove old containers that might be leftover from failing tests
    if config.docker_url:
        docker_client = DockerClient(base_url=config.docker_url)
    else:
        docker_client = docker.from_env()

    docker_name_prefix_filter = dict(filters=dict(name=f'{config.docker_name_prefix}'))
    for container in docker_client.containers.list(**docker_name_prefix_filter):
        container.stop()
    for container in docker_client.containers.list(**docker_name_prefix_filter, all=True):
        container.remove()


def test_get_instances(api):
    response = api.get('instances')
    assert response.status_code == 200, response.text
    assert len(response.json()) == 0


@pytest.mark.parametrize('request_json, status_code', [
    pytest.param({'name': 'jupyter', 'paths': ['/']}, 200, id='ok'),
    pytest.param({'name': 'doesnotexist', 'paths': ['/']}, 422, id='tool-does-not-exist'),
    pytest.param({'paths': ['/']}, 422, id='name-is-missing'),
    pytest.param({'name': 'jupyter'}, 422, id='paths-is-missing')
])
def test_post_instances(api, request_json, status_code, docker_cleanup):
    token = create_launch_token(paths=['/'])
    response = api.post('instances/', headers=dict(Authorization=f'Bearer {token.token}'), json=request_json)
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()['path'] == "/container/0/"


def test_post_instances_already_running(api, docker_cleanup):
    token = create_launch_token(paths=['/'])
    request_json = {'name': 'jupyter', 'paths': ['/']}
    response = api.post('instances/', headers=dict(Authorization=f'Bearer {token.token}'), json=request_json)
    assert response.status_code == 200
    first_response = response.json()

    # Now we make another request to test what happens if the user has an instance running
    response = api.post('instances/', headers=dict(Authorization=f'Bearer {token.token}'), json=request_json)
    assert response.status_code == 200
    assert response.json() == first_response

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


@pytest.fixture(scope='session')
def docker_client() -> DockerClient:
    '''
    A session fixture for using docker. It will try to remove all left-over containers
    after the test session.
    '''
    if config.docker_url:
        docker_client = DockerClient(base_url=config.docker_url)
    else:
        docker_client = docker.from_env()

    yield docker_client

    # Remove old containrs that might be leftover from failing tests
    docker_name_prefix_filter = dict(filters=dict(name=f'{config.docker_name_prefix}-.*'))
    for container in docker_client.containers.list(**docker_name_prefix_filter):
        container.stop()
    for container in docker_client.containers.list(**docker_name_prefix_filter, all=True):
        container.remove()


def assert_container(docker_client: DockerClient, name: str, remove: bool = False):
    container = docker_client.containers.get(name)
    assert container is not None
    if remove:
        container.remove()


def test_run_hello(docker_client: DockerClient):
    name = f'{config.docker_name_prefix}-test-hello-world'
    results = docker_client.containers.run('ubuntu:latest', 'echo hello world', name=name)

    assert results == b'hello world\n', results
    assert_container(docker_client, name, remove=True)

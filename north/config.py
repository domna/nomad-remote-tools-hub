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

'''
This config file is based on pydantic's
[settings management](https://pydantic-docs.helpmanual.io/usage/settings/).
'''

from typing import Dict, Any, Optional
from pydantic import Field, BaseSettings
import yaml
import os.path
import os


class NorthConfig(BaseSettings):
    docker_url: Optional[str] = Field(
        None,
        description=(
            'The URL to remotely (or locally) connect to the docker engine API. '
            'If this is not given, the docker config will be read from the local env.'))

    docker_name_prefix: str = Field(
        'north',
        description=(
            'A prefix used for all container names. This can be used to avoid collisions '
            'with other services using the same docker environment.')
    )

    secret: str = Field(
        'this is a secret',
        description='The secret for generating JWT tokens and other cryptographic material.')

    version: str = Field(
        'v0.1.0', description='The current application version according to semantic versioning conventions')

    class Config:
        env_prefix = 'north_'
        case_sensitive = False

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings):

            return (
                init_settings,
                env_settings,
                yaml_config_settings_source, file_secret_settings)


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    if not os.path.exists('north.yaml'):
        return {}

    try:
        with open('north.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if data is None:
            return {}
        return data
    except yaml.YAMLError as e:
        raise e


config = NorthConfig()

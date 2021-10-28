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

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, validator, Field
# from pathlib import Path

# from north import config

# TODO This exemplifies pydantic models a little bit. But, this is just for demonstration.
# The models completed/rewritten and most descriptions are missing.


class ToolModel(BaseModel):
    ''' Model that describes an available tool. '''
    name: str
    description: str
    docker_image: str = Field(..., description='The docker image for this tool.')


all_tools: List[ToolModel] = [
    ToolModel(
        name='jupyter',
        description='Basic jupyter run with an empty notebook or on given notebook file.',
        docker_image='TODO'
    ),
    ToolModel(
        name='hyperspy',
        description='Run hyperspy on a arbitrary .hdf5 file.',
        docker_image='TODO'
    ),
    ToolModel(
        name='nionswift',
        description='Run Nion Swift to analyze data',
        docker_image='TODO'
    )
]

tools_map: Dict[str, ToolModel] = {tool.name: tool for tool in all_tools}


class InstanceModel(BaseModel):
    name: str
    paths: List[str]

    # Uncomment this when we have syntax for paths in kubernetes setup
    # and add validation for those too. It is commented now to let us
    # test on kubes without caring for validation.
    # @validator('paths')
    # def validate_path(cls, paths):  # pylint: disable=no-self-argument
    #     for path in paths:
    #         assert path[0] == '/', 'All paths should start with a leading /.'

    #         isAllowed = False
    #         for allowed_data_path in config.allowed_data_paths:
    #             if Path(allowed_data_path) in Path(path).parents or path == allowed_data_path:
    #                 isAllowed = True
    #         assert isAllowed, 'You can only request to mount allowed paths.'

    #     return paths

    @validator('name')
    def validate_name(cls, name):  # pylint: disable=no-self-argument
        assert name in tools_map, 'The requested tool does not exist in our list.'
        return name


class InstanceInDBModel(InstanceModel):
    ''' The Instance Model to use to store data internally '''
    docker_id: str


class InstanceResponseModel(BaseModel):
    ''' Response model with approprate instance information for the client '''
    path: str = ''
    channel_token: str


class Error(BaseModel):
    ''' An error model to represent generic error messages '''
    message: str


class ChannelUnavailableError(BaseModel):
    ''' An error model for the 503 HTTP error when requesting a container launch '''
    message: str = "There are no available channels to assign at the moment. Please try again."


class TokenModel(BaseModel):
    token: str
    claims: Optional[Dict[str, Any]]
    expires: Optional[int]

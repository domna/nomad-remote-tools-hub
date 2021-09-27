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

from typing import List, Dict, Optional
from pydantic import BaseModel, validator, Field

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
    )
]

tools_map: Dict[str, ToolModel] = {tool.name: tool for tool in all_tools}


class InstanceModel(BaseModel):
    name: str
    docker_id: Optional[str]
    tool_name: str

    @validator('tool_name')
    def validate_tool_name(cls, tool_name):  # pylint: disable=no-self-argument
        assert tool_name in tools_map, 'Tool must exist.'
        return tool_name

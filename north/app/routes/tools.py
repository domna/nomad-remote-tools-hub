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

from typing import List
from fastapi import APIRouter

from north.app.models import ToolModel, all_tools

router = APIRouter()
router_tag = 'tools'


@router.get(
    '/',
    tags=[router_tag],
    response_model=List[ToolModel],
    response_model_exclude_unset=True,
    response_model_exclude_none=True)
async def get_tools():
    return all_tools

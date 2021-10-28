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

import os
from pathlib import Path
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

router = APIRouter()
router_tag = 'resources'

resources_dir_path = Path(os.path.realpath(__file__)).parents[1] / 'resources'


@router.get("/sw.js", tags=[router_tag])
async def sw(response: Response):
    headers = {"Service-Worker-Allowed": '/'}  # We could limit this to the base url of North
    return FileResponse(str(resources_dir_path) + '/sw.js', headers=headers)


@router.get("/sw-test.html", tags=[router_tag])
async def swtest():
    return FileResponse(str(resources_dir_path) + '/sw-test.html')

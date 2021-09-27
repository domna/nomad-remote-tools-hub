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

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler as default_http_exception_handler

from north import config

from .routes import instances
from .routes import tools

app = FastAPI(
    title='NOMAD remote tools hub API',
    version=config.version,
    description=(
        'This is the API for the NOMAD remote tools hub. It allows to run dockerized '
        'tools remotely.'))

app.include_router(tools.router, prefix='/tools')
app.include_router(instances.router, prefix='/instances')


# A default 404 response with a link to the API dashboard for convinience
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code != 404:
        return await default_http_exception_handler(request, exc)

    try:
        accept = request.headers['accept']
    except Exception:
        accept = None

    if accept is not None and 'html' in accept:
        return HTMLResponse(status_code=404, content='''
            <html>
                <head><title>NOMAD remote tools hub app</title></head>
                <body>
                    <h1>NOMAD remote tools hub app</h1>
                    <h2>apis</h2>
                    <a href="/docs">OpenAPI dashboard</a>
                </body>
            </html>
            ''')

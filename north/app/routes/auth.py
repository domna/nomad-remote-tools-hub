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

from typing import Optional, List
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from north.app.models import TokenModel
from north.auth import create_token, verify_token, TokenError

router = APIRouter()
router_tag = 'auth'


def token_channel(request: Request) -> Optional[TokenModel]:
    ''' Dependency for all routes that require channel authorization '''
    authorization = request.headers.get('Authorization')
    if authorization is None:
        raise HTTPException(status_code=401, detail='Authorization is required.')

    return _token(request=request, claims=['channel'])


def token_launch(request: Request) -> Optional[TokenModel]:
    ''' Dependency for all routes that require launch authorization '''
    return _token(request=request, claims=['paths'])


def _token(request: Request, claims: List[str]) -> Optional[TokenModel]:
    authorization = request.headers.get('Authorization')
    if authorization is None:
        return None

    bearer, token = authorization.split(' ', 1)
    if bearer != 'Bearer':
        raise HTTPException(status_code=401, detail='Invalid authentication scheme.')

    try:
        return verify_token(token, claims=claims)
    except TokenError as e:
        raise HTTPException(status_code=401, detail=e.msg) from e


@router.get(
    '/channel/{channel}',
    tags=[router_tag])
async def authorize_channel(channel: int, token=Depends(token_channel)):
    '''
    Verifies channel token in the header and either raises HTTP 200 or 401.
    This is used by a proxy to authorize access to a docker container channel before
    relaying requests via that channel.
    '''
    if 'channel' not in token.claims:
        raise HTTPException(
            status_code=401, detail='Need to authorize with a channel token.')

    if token.claims['channel'] != channel:
        raise HTTPException(
            status_code=401, detail='You are not authorized to access this channel')

    return 'authorized'


@router.post(
    '/refresh',
    tags=[router_tag],
    response_model=TokenModel,
    response_model_exclude_unset=True,
    response_model_exclude_none=True)
async def refresh_token(token: TokenModel):
    '''
    Returns a new token. It will have the same claims as the given token, but a new
    expiry time.
    '''
    token = verify_token(token.token)
    return create_token(claims=token.claims)

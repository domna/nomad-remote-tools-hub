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
This module provide the necessary token create/verify functionality. Currently there
are two types of tokens, launch tokens and channel tokens.

The channel token allows to authorize access to a running container. The container is
accessed through a numbered channel via the north proxy. The token will be issued
when creating the instances.

The launch token allows to authorize that a container can be created and that certain
resources can be accessed through the container. The launch token might be optional.
In the NOMAD Oasis use-case, launch tokens might be issued by the NOMAD API to authorize
clients to create containers that access a users files and directories.

All tokens can exprire. Token can be re-issued by the north auth API.
'''

from north.app.models import TokenModel
from typing import List, Dict, Any, Optional
import jwt
from datetime import datetime, timedelta

from north import config


class TokenError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


def create_launch_token(paths: List[str], duration: timedelta = timedelta(minutes=10)) -> TokenModel:
    '''
    Creates a JWT token that contains a claim on a set of paths and is valid for the given
    duration.

    This could be issued for example by the NOMAD uploads API after authorizing access
    to certain paths. It could be used by 3rd-party products to authorize access to
    certain paths.

    # TODO more complex claims. E.g. Read/Write access, tool to launch, etc.

    Returns: The token as a string.
    '''

    claims = {
        'paths': paths
    }
    return create_token(claims, duration)


def create_channel_token(channel: int, duration: timedelta = timedelta(minutes=10)) -> TokenModel:
    '''
    Creates a JWT token that contains a claim on the given channel for the given
    duration starting now.

    Returns: The token as a string.
    '''

    claims = {
        'channel': channel
    }
    return create_token(claims, duration)


def create_token(claims: Optional[Dict[str, Any]], duration: timedelta = timedelta(minutes=10)) -> TokenModel:
    ''' Creates a JWT token with the given claims. '''
    if claims is None:
        claims = {}
    claims_to_encode = dict(exp=datetime.utcnow() + duration, **claims)
    token = jwt.encode(claims_to_encode, config.secret, algorithm='HS256')

    return TokenModel(token=token, expires=duration.seconds, claims=claims)


def verify_token(token: str, claims: List[str] = None) -> TokenModel:
    '''
    Verifies the given token. Checks its expiry and if the given claims are present.

    Returns: A dictionary with the given claims as keys and values taken from the token
        payload.

    Raises:
        TokenError: If the token could not be decoded, is experied, or did not contain
            the necessary claims.
    '''

    try:
        encoded_claims = jwt.decode(
            token, config.secret, algorithms=['HS256'],
            options=dict(require=['exp'] + claims if claims else []))
    except jwt.ExpiredSignatureError as e:
        raise TokenError('The token is expired.') from e
    except jwt.DecodeError as e:
        raise TokenError('The token could not be decoded.') from e

    expires = datetime.utcfromtimestamp(encoded_claims['exp']) - datetime.utcnow()
    token_claims = {
        key: value for key, value in encoded_claims.items() if key != 'exp'
    }

    return TokenModel(token=token, claims=token_claims, expires=expires.seconds)

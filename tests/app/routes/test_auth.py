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

from datetime import timedelta

from north.auth import create_channel_token, verify_token


def test_valid_channel(api):
    token = create_channel_token(channel=1)
    response = api.get('auth/channel/1', headers=dict(Authorization=f'Bearer {token.token}'))
    assert response.status_code == 200


def test_wrong_channel(api):
    token = create_channel_token(channel=2)
    response = api.get('auth/channel/1', headers=dict(Authorization=f'Bearer {token.token}'))
    assert response.status_code == 401


def test_missing_channel_token(api):
    response = api.get('auth/channel/1')
    assert response.status_code == 401


def test_bad_channel_token(api):
    response = api.get('auth/channel/1', headers=dict(Authorization='Bearer not a token'))
    assert response.status_code == 401


def test_expired_channel_token(api):
    token = create_channel_token(channel=1, duration=-timedelta(days=1))
    response = api.get('auth/channel/1', headers=dict(Authorization=f'Bearer {token.token}'))
    assert response.status_code == 401


def test_refresh(api):
    token = create_channel_token(channel=1)
    response = api.post('auth/refresh', json=token.dict())
    assert response.status_code == 200
    token_data = response.json()
    assert token_data['claims'] == verify_token(token_data['token']).claims

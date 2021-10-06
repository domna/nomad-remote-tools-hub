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
import pytest

from north.auth import TokenError, create_channel_token, create_launch_token, create_token, verify_token


def test_channel_token():
    token = create_channel_token(channel=1)
    token_model = verify_token(token.token, claims=['channel'])
    assert token_model.claims['channel'] == 1


def test_launch_token():
    token = create_launch_token(paths=['/my/folder'])
    token_model = verify_token(token.token, claims=['paths'])
    assert token_model.claims['paths'] == ['/my/folder']


def test_token_expiry():
    token = create_token(claims={}, duration=-timedelta(days=1))
    with pytest.raises(TokenError):
        verify_token(token.token, claims=[])

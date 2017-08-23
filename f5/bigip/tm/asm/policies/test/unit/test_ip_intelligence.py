# Copyright 2015 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from f5.bigip.tm.asm.policies.ip_intelligence import Ip_Intelligence
from f5.sdk_exception import UnsupportedOperation


import mock
import pytest


@pytest.fixture
def FakeIP():
    fake_policy = mock.MagicMock()
    fake_resp = Ip_Intelligence(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


class TestIPIntelligence(object):
    def test_update_raises(self, FakeIP):
        with pytest.raises(UnsupportedOperation):
            FakeIP.update()

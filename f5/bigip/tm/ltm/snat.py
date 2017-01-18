# coding=utf-8
#
# Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) Snat module.

REST URI
    ``http://localhost/mgmt/tm/ltm/snat``

GUI Path
    ``Local Traffic --> Snat``

REST Kind
    ``tm:ltm:snat:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


# ToDo This is a prime example of duplication, needs to be removed
class RequireOneOf(MissingRequiredCreationParameter):
    pass


class Snats(Collection):
    """BIG-IP® LTM Snat collection"""
    def __init__(self, ltm):
        super(Snats, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Snat]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:snat:snatstate': Snat}


class Snat(Resource):
    """BIG-IP® LTM Snat resource"""
    def __init__(self, snat_s):
        '''This represents a Snat.

        "origins" is our first example of a dict attribute, it appears to
        behave as expected.
        '''
        super(Snat, self).__init__(snat_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:snat:snatstate'
        self._meta_data['required_creation_parameters'].update(
            ('partition', 'origins'))

    def create(self, **kwargs):
        """Call this to create a new snat on the BIG-IP®.

        Uses HTTP POST to 'containing' URI to create a service associated with
        a new URI on the device.

        Note this is the one of two fundamental Resource operations that
        returns a different uri (in the returned object) than the uri the
        operation was called on.  The returned uri can be accessed as
        Object.selfLink, the actual uri used by REST operations on the object
        is Object._meta_data['uri'].  The _meta_data['uri'] is the same as
        Object.selfLink with the substring 'localhost' replaced with the value
        of Object._meta_data['BIG-IP']._meta_data['hostname'], and without
        query args, or hash fragments.

        The following is done prior to the POST
        * Ensures that one of ``automap``, ``snatpool``, ``translation``
          parameter is passed in.

        :param kwargs: All the key-values needed to create the resource
        :returns: An instance of the Python object that represents the device's
        uri-published resource.  The uri of the resource is part of the
        object's _meta_data.
        """
        required_one_of = ['automap', 'snatpool', 'translation']
        has_any = [x for x in iterkeys(kwargs) if x in required_one_of]

        # The rules for SNAT is that you must provide one, and only one,
        # of the `required_one_of` values above.
        if len(has_any) == 1:
            return self._create(**kwargs)

        raise RequireOneOf(
            "Creation requires one of the provided {0}".format(
                ', '.join(required_one_of)
            )
        )

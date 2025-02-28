# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module contains utility functions for API development work."""
from ansys.api.edb.v1.layout_obj_pb2 import LayoutObjTargetMessage

from ansys.edb.core.inner.factory import create_lyt_obj
from ansys.edb.core.utility.cache import get_cache


def map_list(iterable_to_operate_on, operator=None):
    """Apply the given operator to each member of an iterable and return the modified list.

    Parameters
    ---------
    iterable_to_operate_on
    operator
    """
    return list(
        iterable_to_operate_on if operator is None else map(operator, iterable_to_operate_on)
    )


def query_lyt_object_collection(owner, obj_type, unary_rpc, unary_streaming_rpc):
    """For the provided request, retrieve a collection of objects using the unary_rpc or unary_streaming_rpc methods \
    depending on whether caching is enabled."""
    items = []
    cache = get_cache()
    request = LayoutObjTargetMessage(target=owner.msg, type=obj_type.value)

    def add_msgs_to_items(edb_obj_collection_msg):
        nonlocal items
        for item in edb_obj_collection_msg.items:
            items.append(create_lyt_obj(item, obj_type))

    if cache is None:
        add_msgs_to_items(unary_rpc(request))
    else:
        for streamed_items in unary_streaming_rpc(request):
            add_msgs_to_items(streamed_items)
    return items

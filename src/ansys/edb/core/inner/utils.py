# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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


def map_list(iterable_to_operate_on, operator=None):
    """Apply the given operator to each member of an iterable and return the modified list.

    Parameters
    ----------
    iterable_to_operate_on
    operator
    """
    return list(iterable_to_operate_on if operator is None else map(operator, iterable_to_operate_on))


def ensure_is_list(obj):
    """If the object is a list, return it. Otherwise, return a list where the sole entry is the provided obj."""
    return obj if isinstance(obj, list) else [obj]


def query_lyt_object_collection(owner, obj_type, unary_rpc, unary_streaming_rpc, request_requires_type=True):
    """For the provided request, retrieve a collection of objects using the unary_rpc or unary_streaming_rpc methods \
    depending on whether caching is enabled.
    """
    from ansys.edb.core.utility.io_manager import get_cache

    request = LayoutObjTargetMessage(target=owner.msg, type=obj_type.value) if request_requires_type else owner.msg

    items = []
    cache = get_cache()

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


def stream_items_from_server(parser, stream, chunk_items_att_name):
    """Stream all items from the provided unary server stream and convert them to \
    the corresponding pyedb-core data type using the provided parser.
    """
    return [parser(chunk_entry) for chunk in stream for chunk_entry in getattr(chunk, chunk_items_att_name)]


def client_stream_iterator(
    data_to_stream,
    chunk_type,
    chunk_entry_creator,
    chunk_entries_getter,
    max_size=32000,
    starting_chunk=None,
):
    """Create an iterator of client side items to be used when streaming items to the server."""
    chunk = chunk_type() if starting_chunk is None else starting_chunk
    for data_entry in data_to_stream:
        chunk_entry = chunk_entry_creator(data_entry)
        if chunk.ByteSize() + chunk_entry.ByteSize() > max_size:
            yield chunk
            chunk = chunk_type()
        chunk_entries_getter(chunk).append(chunk_entry)
    yield chunk

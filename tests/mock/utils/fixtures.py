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

import random
import string

import pytest

from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.layout.layout import Layout
from ansys.edb.core.net.net import Net

from .test_utils import create_edb_obj_msg, generate_random_int


@pytest.fixture
def mocked_stub(mocker):
    def _stub(mod, cls):
        mock = mocker.Mock()
        path = f"{mod.__name__}.{cls.__name__}._{cls.__name__}__stub"
        mocker.patch(path, mock)
        return mock

    return _stub


@pytest.fixture(params=[True, False])
def bool_val(request):
    """Parameterized fixture that returns True and False values

    Returns
    -------
    bool
    """
    return request.param


@pytest.fixture
def edb_obj_msg():
    """Fixture for creating an EDBObjMessage.

    Returns
    -------
    EDBObjMessage
    """
    return create_edb_obj_msg()


@pytest.fixture
def random_str():
    """Fixture for creating a 10 character long string comprised of random ascii letters.

    Returns
    -------
    str
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


@pytest.fixture
def random_int():
    """Fixture for generating a random integer between 0 and 100,000.

    Returns
    -------
    int
    """
    return generate_random_int()


@pytest.fixture
def layouts(request):
    count = request.param if hasattr(request, "param") and request.param else 1
    return [Layout(create_edb_obj_msg()) for _ in range(count)]


@pytest.fixture
def layout(layouts):
    return layouts[0]


@pytest.fixture
def nets(request):
    count = request.param if hasattr(request, "param") and request.param else 1
    return [Net(create_edb_obj_msg()) for _ in range(count)]


@pytest.fixture
def net(nets):
    return nets[0]


@pytest.fixture
def layers(request):
    count = request.param if hasattr(request, "param") and request.param else 1
    return [Layer(create_edb_obj_msg()) for _ in range(count)]


@pytest.fixture
def layer(layers):
    return layers[0]


@pytest.fixture
def layer_ref(request):
    if isinstance(request.param, str):
        ret = request.getfixturevalue(request.param)
        if isinstance(ret, Layer) or isinstance(ret, str):
            return ret
        else:
            comment = (
                f"Invalid parameter for 'layer_ref'."
                f"Fixture '{request.param}' resolved to {type(ret)}. Must be either str or Layer."
            )
    else:
        comment = (
            "Invalid parameter for 'layer_ref'."
            "It must be a string name of another fixture that resolves to str or Layer."
        )

    raise RuntimeError(comment)

import random
import string

import pytest

from ansys.edb.layer.layer import Layer
from ansys.edb.layout.layout import Layout
from ansys.edb.net.net import Net

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

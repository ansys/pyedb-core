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

"""Pin pair model."""

import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.session import PinPairModelServiceStub, StubAccessor, StubType


class PinPairModel(Model):
    """Represents a pin pair model object."""

    __stub: PinPairModelServiceStub = StubAccessor(StubType.pin_pair_model)

    @classmethod
    def create(cls):
        """Create a pin pair model.

        Returns
        -------
        PinPairModel
            Pin pair model created.
        """
        return cls(cls.__stub.Create(empty_pb2.Empty()))

    def rlc(self, pin_pair):
        """Get the RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]

        Returns
        -------
        :class:`.Rlc`
        """
        res = self.__stub.GetRlc(messages.string_pair_property_message(self, pin_pair))
        if res.found:
            return parser.to_rlc(res.rlc)
        else:
            return None

    def set_rlc(self, pin_pair, rlc):
        """Set the RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        rlc : :class:`.Rlc`
        """
        self.__stub.SetRlc(messages.pin_pair_model_rlc_message(self, pin_pair, rlc))

    def delete_rlc(self, pin_pair):
        """Delete the RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        """
        self.__stub.DeleteRlc(messages.string_pair_property_message(self, pin_pair))

    def pin_pairs(self):
        """Get all pin pairs.

        Returns
        -------
        list[tuple[str, str]]
        """
        res = self.__stub.GetPinPairs(messages.edb_obj_message(self))
        return [(pair.first, pair.second) for pair in res.pairs]

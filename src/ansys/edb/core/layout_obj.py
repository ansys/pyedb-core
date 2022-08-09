"""Layout Object."""

import ansys.api.edb.v1.layout_obj_pb2 as layout_obj_pb2

from ansys.edb.core import ObjBase
import ansys.edb.core.messages as messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.layout import layout


class _QueryBuilder:
    @staticmethod
    def layout_obj_target_msg(layout_obj, layout_type):
        return layout_obj_pb2.LayoutObjTargetMessage(target=layout_obj.msg, type=layout_type.value)

    @staticmethod
    def get_product_property_type_msg(obj, prod_id, attr_it, layout_type):
        return layout_obj_pb2.GetProductPropertyTypeMessage(
            target=messages.get_product_property_message(obj, prod_id, attr_it),
            type=layout_type.value,
        )

    @staticmethod
    def set_product_property_type_msg(obj, prod_id, att_id, value, layout_type):
        return layout_obj_pb2.SetProductPropertyTypeMessage(
            target=messages.set_product_property_message(obj, prod_id, att_id, value),
            type=layout_type.value,
        )

    @staticmethod
    def get_product_property_ids_type_msg(obj, prod_id, layout_type):
        return layout_obj_pb2.GetProductPropertyIdsTypeMessage(
            target=messages.get_product_property_ids_message(obj, prod_id),
            type=layout_type.value,
        )


class LayoutObj(ObjBase):
    """Layout Object class."""

    layout_obj_type = LayoutObjType.INVALID_LAYOUT_OBJ

    @property
    def obj_type(self):
        """Get the layout object type.

        Returns
        -------
            LayoutObjType enum of the Layout Object.
        """
        return self.layout_type

    @property
    def layout(self):
        """Get the Layout of the layout object.

        Returns
        -------
            Layout of the Layout Object.
        """
        return layout.Layout(
            self.__stub.GetLayout(_QueryBuilder.layout_obj_target_msg(self, self.layout_type))
        )

    def delete(self):
        """Delete the layout object."""
        self.__stub.Delete(_QueryBuilder.layout_obj_target_msg(self, self.layout_type))

    def get_product_property(self, prod_id, attr_it):
        """Get the product property of the layout object with the given product and attribute ids.

        Parameters
        ----------
        prod_id : ProductIdType
        attr_it : int

        Returns
        -------
        str
        """
        return self.__stub.GetProductProperty(
            _QueryBuilder.get_product_property_type_msg(self, prod_id, attr_it, self.layout_type)
        ).value

    def set_product_property(self, prod_id, att_id, prop_value):
        """Set the product property of the layout object associated with the given product and attribute ids.

        Parameters
        ----------
        prod_id : ProductIdType
        attr_it : int
        prop_value : str
        """
        self.__stub.SetProductProperty(
            _QueryBuilder.set_product_property_type_msg(
                self, prod_id, att_id, prop_value, self.layout_type
            )
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute ids corresponding to the provided product id for the layout object.

        Parameters
        ----------
        prod_id : ProductIdType

        Returns
        -------
        list[int]
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            _QueryBuilder.get_product_property_ids_type_msg(self, prod_id, self.layout_type)
        ).ids
        return [attr_id for attr_id in attr_ids]

class ObjBase:
    def __init__(self, msg):
        self._msg = msg

    def is_null(self):
        return self._msg.impl_ptr_address == 0

    @property
    def id(self):
        return self._msg

from distutils.dir_util import copy_tree
import os
import platform
import random
import shutil
import string
import tempfile


class Scratch:
    """ """

    @property
    def path(self):
        """ """
        return self._scratch_path

    @property
    def is_empty(self):
        """ """
        return self._cleaned

    def __init__(self, local_path=None, permission=0o777, volatile=False):
        # set scratch path and create it if necessary
        if local_path is None:
            local_path = tempfile.gettempdir()
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        self._volatile = volatile
        self._cleaned = True
        char_set = string.ascii_uppercase + string.digits
        self._scratch_path = os.path.normpath(
            os.path.join(
                local_path,
                "pyedb_%s_scratch" % platform.python_version()
                + "".join(random.sample(char_set, 6)),
            )
        )
        if os.path.exists(self._scratch_path):
            try:
                self.remove()
            except:
                self._cleaned = False
        if self._cleaned:
            try:
                os.mkdir(self.path)
                os.chmod(self.path, permission)
            except:
                pass

    def remove(self):
        """ """
        try:
            # TODO check why on Anaconda 3.7 get errors with os.path.exists
            shutil.rmtree(self._scratch_path, ignore_errors=True)
        except:
            pass

    def copyfile(self, src_file, dst_filename=None):
        """

        Parameters
        ----------
        src_file : str
            Source File with fullpath
        dst_filename : str, optional
            Optional destination filename with extensione


        Returns
        -------

        """
        if dst_filename:
            dst_file = os.path.join(self.path, dst_filename)
        else:
            dst_file = os.path.join(self.path, os.path.basename(src_file))
        if os.path.exists(dst_file):
            try:
                os.unlink(dst_file)
            except OSError:  # pragma: no cover
                pass
        try:
            shutil.copy2(src_file, dst_file)
        except shutil.SameFileError:  # pragma: no cover
            pass

        return dst_file

    def copyfolder(self, src_folder, destfolder):
        """

        Parameters
        ----------
        src_folder :

        destfolder :


        Returns
        -------

        """
        copy_tree(src_folder, destfolder)
        return True

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if ex_type or self._volatile:
            self.remove()

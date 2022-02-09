from PySide2 import QtCore, QtWidgets, QtGui
from abc import abstractmethod
from dcc.math import vectormath

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAbstractTab(QtWidgets.QWidget):
    """
    Overload of QWidget used to outline the structure for alignment tabs.
    """

    FLOAT_PRECISION = 3
    SIGN = 1.0, -1.0
    ORIGIN = vectormath.ORIGIN
    AXIS_VECTORS = vectormath.X_AXIS_VECTOR, vectormath.Y_AXIS_VECTOR, vectormath.Z_AXIS_VECTOR

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        """
        Overloaded method called after a new instance has been created.

        :type parent: QtWidgets.QWidget
        :type f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QAbstractTab, self).__init__(parent=parent, f=f)

    def __build__(self):

        pass

    @abstractmethod
    def apply(self, preserveChildren=False):
        """
        Abstract method intended to be overloaded to define the custom alignment operation.

        :type preserveChildren: bool
        :rtype: None
        """

        pass

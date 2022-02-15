from PySide2 import QtCore, QtWidgets, QtGui
from abc import abstractmethod

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAbstractTab(QtWidgets.QWidget):
    """
    Overload of QWidget used to outline the structure for alignment tabs.
    """

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Private method called after a new instance has been created.

        :type parent: QtWidgets.QWidget
        :type f: int
        :rtype: None
        """

        # Call parent method
        #
        parent = kwargs.get('parent', None)
        f = kwargs.get('f', QtCore.Qt.WindowFlags())

        super(QAbstractTab, self).__init__(parent=parent, f=f)

        # Initialize user interface
        #
        self.__build__(*args, **kwargs)

    @abstractmethod
    def __build__(self, *args, **kwargs):
        """
        Private method used to build the user interface.

        :rtype: None
        """

        pass
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        pass

    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        pass

    @abstractmethod
    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Abstract method intended to be overloaded to define the custom alignment operation.

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        pass
    # endregion

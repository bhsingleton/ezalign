from Qt import QtCore, QtWidgets, QtGui
from abc import abstractmethod
from dcc import fnscene

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAbstractTab(QtWidgets.QWidget):
    """
    Overload of `QWidget` that outlines alignment tab behavior.
    """

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Private method called after a new instance has been created.

        :key parent: QtWidgets.QWidget
        :key f: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QAbstractTab, self).__init__(*args, **kwargs)

        # Declare private variables
        #
        self._scene = fnscene.FnScene()
    # endregion

    # region Properties
    @property
    def scene(self):
        """
        Getter method that returns the scene function set.

        :rtype: fnscene.FnScene
        """

        return self._scene
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

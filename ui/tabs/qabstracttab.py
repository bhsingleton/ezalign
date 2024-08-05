from Qt import QtCore, QtWidgets, QtGui
from abc import abstractmethod
from dcc import fnqt, fnscene
from dcc.ui.abstract import qabcmeta

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAbstractTab(QtWidgets.QWidget, metaclass=qabcmeta.QABCMeta):
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
        self._qt = fnqt.FnQt()
        self._scene = fnscene.FnScene()

    def __post_init__(self, *args, **kwargs):
        """
        Private method called after an instance has initialized.

        :rtype: None
        """

        self.__setup_ui__(*args, **kwargs)

    @abstractmethod
    def __setup_ui__(self, *args, **kwargs):
        """
        Private method that initializes the user interface.

        :rtype: None
        """

        pass
    # endregion

    # region Properties
    @property
    def qt(self):
        """
        Getter method that returns the qt function set.

        :rtype: fnqt.FnQt
        """

        return self._qt

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

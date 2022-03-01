from PySide2 import QtCore, QtWidgets, QtGui
from abc import abstractmethod
from dcc.ui import quicinterface, qmatrixedit, qvectoredit

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAbstractTab(quicinterface.QUicInterface, QtWidgets.QWidget):
    """
    Overload of QWidget used to outline the structure for alignment tabs.
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

        # Load user interface
        #
        self.preLoad()
        self.__load__(*args, **kwargs)
        self.postLoad()
    # endregion

    # region Methods
    @classmethod
    def customWidgets(cls):
        """
        Returns a dictionary of custom widgets used by this class.
        Overload this method to extend this dictionary!

        :rtype: dict[str:type]
        """

        customWidgets = super(QAbstractTab, cls).customWidgets()
        customWidgets['QMatrixEdit'] = qmatrixedit.QMatrixEdit
        customWidgets['QVectorEdit'] = qvectoredit.QVectorEdit

        return customWidgets

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

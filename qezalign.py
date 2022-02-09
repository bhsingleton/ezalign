from PySide2 import QtCore, QtWidgets, QtGui
from dcc.userinterface import qproxywindow
from ezalign.tabs import qaligntab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QEzAlign(qproxywindow.QProxyWindow):
    """
    Overload of QProxyWindow used to align node transforms.
    """

    __title__ = 'EzAlign'

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :keyword parent: QtWidgets.QWidget
        :keyword flags: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).__init__(*args, **kwargs)

        # Declare class variables
        #
        self._preserveChildren = False
        self._freezeTransform = False

    def __build__(self, **kwargs):
        """
        Private method used to build the user interface.

        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).__build__(**kwargs)

        # Create central widget
        #
        self.setMinimumSize(QtCore.QSize(315, 375))
        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())

        # Define tab layout
        #
        self.tabControl = QtWidgets.QTabWidget()
        self.tabControl.addTab(qaligntab.QAlignTab(), 'Align')

        self.centralWidget().layout().addWidget(self.tabControl)

        # Define main buttons
        #
        self.applyButton = QtWidgets.QPushButton('Apply')
        self.applyButton.pressed.connect(self.apply)

        self.applyOptionsButton = QtWidgets.QPushButton()
        self.applyOptionsButton.setFixedWidth(18)
        self.applyOptionsButton.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.applyLayout = QtWidgets.QHBoxLayout()
        self.applyLayout.setSpacing(2)
        self.applyLayout.addWidget(self.applyButton)
        self.applyLayout.addWidget(self.applyOptionsButton)

        self.preserveChildrenAction = QtCore.QAction('&Preserve Children')
        self.preserveChildrenAction.setCheckable(True)
        self.preserveChildrenAction.triggered.connect(self.preserveChildrenTriggered)

        self.freezeTransformAction = QtCore.QAction('&Freeze Transform')
        self.freezeTransformAction.setCheckable(True)
        self.freezeTransformAction.triggered.connect(self.freezeTransformTriggered)

        self.applyMenu = QtWidgets.QMenu(self.applyOptionsButton)
        self.applyMenu.addActions([self.preserveChildrenAction, self.freezeTransformAction])

        self.applyOptionsButton.setMenu(self.applyMenu)

        self.okayButton = QtWidgets.QPushButton('OK')
        self.okayButton.pressed.connect(self.okay)

        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.cancelButton.pressed.connect(self.cancel)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addLayout(self.applyLayout)
        self.buttonLayout.addWidget(self.okayButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.centralWidget().layout().addLayout(self.buttonLayout)
    # endregion

    # region Properties
    @property
    def preserveChildren(self):
        """
        Getter method used to return the preserve children flag.

        :rtype: bool
        """

        return self._preserveChildren

    @preserveChildren.setter
    def preserveChildren(self, preserveChildren):
        """
        Getter method used to return the preserve children flag.

        :type preserveChildren: bool
        :rtype: None
        """

        self.preserveChildrenAction.setChecked(preserveChildren)

    @property
    def freezeTransform(self):
        """
        Getter method used to return the freeze transform flag.

        :rtype: bool
        """

        return self._preserveChildren

    @freezeTransform.setter
    def freezeTransform(self, freezeTransform):
        """
        Getter method used to return the freeze transform flag.

        :type freezeTransform: bool
        :rtype: None
        """

        self.freezeTransformAction.setChecked(freezeTransform)
    # endregion

    # region Methods
    def loadSettings(self):
        """
        Loads the user settings.

        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).loadSettings()

        # Load user preferences
        #
        self.preserveChildren = self.settings.value('editor/preserveChildren', defaultValue=False, type=bool)
        self.freezeTransform = self.settings.value('editor/freezeTransform', defaultValue=False, type=bool)

    def saveSettings(self):
        """
        Saves the user settings.

        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).saveSettings()

        # Save user preferences
        #
        self.settings.setValue('editor/preserveChildren', self.preserveChildren)
        self.settings.setValue('editor/freezeTransform', self.freezeTransform)

    def currentTab(self):
        """
        Returns the tab that is currently being displayed.

        :rtype: QAbstractTab
        """

        return self.tabControl.currentWidget()
    # endregion

    # region Slots
    def apply(self, *args, **kwargs):
        """
        Slot method called whenever the user clicks the apply button.
        This method will apply a transform matrix to the active selection.
        This functionality changes based on the selected tab index.

        :rtype: None
        """

        currentTab = self.currentTab()

        if currentTab is not None:
            currentTab.apply(preserveChildren=self.preserveChildren, freezeTransform=self.freezeTransform)

    def okay(self, *args, **kwargs):
        """
        Slot method called whenever the user clicks the okay button.
        This method will close the UI after applying the selected operation.

        :rtype: None
        """

        self.apply()
        self.close()

    def cancel(self, *args, **kwargs):
        """
        Slot method called whenever the user clicks the cancel button.
        This method will close the UI.

        :rtype: None
        """

        self.close()
        
    def preserveChildrenTriggered(self, *args, **kwargs):
        """
        Slot method called whenever the user triggers the preserve children check box.

        :rtype: None
        """

        self._preserveChildren = self.sender().isChecked()

    def freezeTransformTriggered(self, *args, **kwargs):
        """
        Slot method called whenever the user triggers the freeze transform check box.

        :rtype: None
        """

        self._freezeTransform = self.sender().isChecked()
    # endregion

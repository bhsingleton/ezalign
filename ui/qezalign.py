from Qt import QtCore, QtWidgets, QtGui
from dcc.ui import qsingletonwindow, qdropdownbutton, qpersistentmenu
from .tabs import qaligntab, qaimtab, qmatrixtab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QEzAlign(qsingletonwindow.QSingletonWindow):
    """
    Overload of QProxyWindow used to align node transforms.
    """

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Private method called after a new instance has been created.

        :key parent: QtWidgets.QWidget
        :key flags: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).__init__(*args, **kwargs)

        # Declare public variables
        #
        self.tabControl = None
        self.alignTab = None
        self.aimTab = None
        self.matrixTab = None

        self.buttonsWidget = None
        self.buttonsLayout = None
        self.applyPushButton = None
        self.okayPushButton = None
        self.cancelPushButton = None
        self.applyMenu = None
        self.preserveChildrenAction = None
        self.freezeTransformAction = None

    def __setup_ui__(self, *args, **kwargs):
        """
        Private method that initializes the user interface.

        :rtype: None
        """

        # Initialize main window
        #
        self.setWindowTitle("|| Ez'Align")
        self.setMinimumSize(QtCore.QSize(300, 350))

        # Initialize central widget
        #
        centralLayout = QtWidgets.QVBoxLayout()
        centralLayout.setObjectName('centralLayout')

        centralWidget = QtWidgets.QWidget()
        centralWidget.setObjectName('centralWidget')
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

        # Initialize tab widget
        #
        self.tabControl = QtWidgets.QTabWidget(parent=self)
        self.tabControl.setObjectName('tabControl')
        self.tabControl.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.alignTab = qaligntab.QAlignTab(parent=self.tabControl)
        self.aimTab = qaimtab.QAimTab(parent=self.tabControl)
        self.matrixTab = qmatrixtab.QMatrixTab(parent=self.tabControl)

        self.tabControl.addTab(self.alignTab, 'Align')
        self.tabControl.addTab(self.aimTab, 'Aim')
        self.tabControl.addTab(self.matrixTab, 'Matrix')

        centralLayout.addWidget(self.tabControl)

        # Initialize buttons
        #
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName('buttonsLayout')
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)

        self.buttonsWidget = QtWidgets.QWidget()
        self.buttonsWidget.setObjectName('buttonsWidget')
        self.buttonsWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.buttonsWidget.setFixedHeight(24)
        self.buttonsWidget.setLayout(self.buttonsLayout)

        self.applyPushButton = qdropdownbutton.QDropDownButton('Apply')
        self.applyPushButton.setObjectName('applyPushButton')
        self.applyPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))
        self.applyPushButton.setMouseTracking(True)
        self.applyPushButton.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.applyPushButton.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.applyPushButton.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.applyPushButton.clicked.connect(self.on_applyPushButton_clicked)

        self.okayPushButton = QtWidgets.QPushButton('Okay')
        self.okayPushButton.setObjectName('okayPushButton')
        self.okayPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))
        self.okayPushButton.clicked.connect(self.on_okayPushButton_clicked)

        self.cancelPushButton = QtWidgets.QPushButton('Cancel')
        self.cancelPushButton.setObjectName('cancelPushButton')
        self.cancelPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))
        self.cancelPushButton.clicked.connect(self.on_cancelPushButton_clicked)

        self.buttonsLayout.addWidget(self.applyPushButton)
        self.buttonsLayout.addWidget(self.okayPushButton)
        self.buttonsLayout.addWidget(self.cancelPushButton)

        centralLayout.addWidget(self.buttonsWidget)

        # Initialize apply menu
        #
        self.applyMenu = qpersistentmenu.QPersistentMenu(parent=self.applyPushButton)
        self.applyMenu.setObjectName('applyMenu')

        self.preserveChildrenAction = QtWidgets.QAction('&Preserve Children', self.applyMenu)
        self.preserveChildrenAction.setObjectName('preserveChildrenAction')
        self.preserveChildrenAction.setCheckable(True)

        self.freezeTransformAction = QtWidgets.QAction('&Freeze Transform', self.applyMenu)
        self.freezeTransformAction.setObjectName('freezeTransformAction')
        self.freezeTransformAction.setCheckable(True)

        self.applyMenu.addActions([self.preserveChildrenAction, self.freezeTransformAction])

        self.applyPushButton.setMenu(self.applyMenu)
    # endregion

    # region Properties
    @property
    def preserveChildren(self):
        """
        Getter method used to return the preserve children flag.

        :rtype: bool
        """

        return self.preserveChildrenAction.isChecked()

    @preserveChildren.setter
    def preserveChildren(self, preserveChildren):
        """
        Getter method used to return the preserve children flag.

        :type preserveChildren: bool
        :rtype: None
        """

        if isinstance(preserveChildren, bool):

            self.preserveChildrenAction.setChecked(preserveChildren)

    @property
    def freezeTransform(self):
        """
        Getter method used to return the freeze transform flag.

        :rtype: bool
        """

        return self.freezeTransformAction.isChecked()

    @freezeTransform.setter
    def freezeTransform(self, freezeTransform):
        """
        Getter method used to return the freeze transform flag.

        :type freezeTransform: bool
        :rtype: None
        """

        if isinstance(freezeTransform, bool):

            self.freezeTransformAction.setChecked(freezeTransform)
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).loadSettings(settings)

        # Load user settings
        #
        self.setCurrentTabIndex(settings.value('editor/currentTabIndex', defaultValue=0, type=int))
        self.preserveChildren = bool(settings.value('editor/preserveChildren', defaultValue=0, type=int))
        self.freezeTransform = bool(settings.value('editor/freezeTransform', defaultValue=0, type=int))

        # Load tab settings
        #
        for tab in self.iterTabs():

            tab.loadSettings(settings)

    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).saveSettings(settings)

        # Save user preferences
        #
        settings.setValue('editor/currentTabIndex', self.currentTabIndex())
        settings.setValue('editor/preserveChildren', int(self.preserveChildren))
        settings.setValue('editor/freezeTransform', int(self.freezeTransform))

        # Save tab settings
        #
        for tab in self.iterTabs():

            tab.saveSettings(settings)

    def currentTab(self):
        """
        Returns the tab widget that is currently open.

        :rtype: QAbstractTab
        """

        return self.tabControl.currentWidget()

    def currentTabIndex(self):
        """
        Returns the active tab index.

        :rtype: int
        """

        return self.tabControl.currentIndex()

    def setCurrentTabIndex(self, currentIndex):
        """
        Updates the active tab index.

        :type currentIndex: int
        :rtype: None
        """

        if isinstance(currentIndex, int):

            self.tabControl.setCurrentIndex(currentIndex)

    def iterTabs(self):
        """
        Returns a generator that yields tab widgets.

        :rtype: iter
        """

        for i in range(self.tabControl.count()):

            yield self.tabControl.widget(i)
    # endregion

    # region Slots
    @QtCore.Slot(int)
    def on_tabControl_currentChanged(self, index):
        """
        Adds the tooltip to apply and okay buttons.

        :type index: int
        :rtype: None
        """

        tab = self.sender().widget(index)

        if tab is not None:

            toolTip = tab.whatsThis()
            self.applyPushButton.setToolTip(toolTip)
            self.okayPushButton.setToolTip(toolTip)

    @QtCore.Slot()
    def on_applyPushButton_clicked(self):
        """
        Clicked slot method responsible for applying the selected operation.

        :rtype: None
        """

        currentTab = self.currentTab()

        if currentTab is not None:

            currentTab.apply(preserveChildren=self.preserveChildren, freezeTransform=self.freezeTransform)

    @QtCore.Slot(bool)
    def on_okayPushButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for applying the selected operation the closing the user interface.

        :type checked: bool
        :rtype: None
        """

        self.applyButton.click()
        self.close()

    @QtCore.Slot(bool)
    def on_cancelPushButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for closing the user interface.

        :type checked: bool
        :rtype: None
        """

        self.close()
    # endregion

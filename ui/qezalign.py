from PySide2 import QtCore, QtWidgets, QtGui
from dcc.ui import quicwindow

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QEzAlign(quicwindow.QUicWindow):
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

        # Declare private variables
        #
        self._freezeTransform = False
        self._preserveChildren = False

        # Declare public variables
        #
        self.tabControl = None
        self.alignTab = None
        self.aimTab = None
        self.matrixTab = None

        self.buttonsWidget = None
        self.applyPushButton = None
        self.okayPushButton = None
        self.cancelPushButton = None

        self.applyMenu = None
        self.preserveChildrenAction = None
        self.freezeTransformAction = None
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

        self.freezeTransformAction.setChecked(freezeTransform)
    # endregion

    # region Methods
    def postLoad(self, *args, **kwargs):
        """
        Called after the user interface has been loaded.

        :rtype: None
        """

        # Assign tool button menu
        #
        self.applyMenu = QtWidgets.QMenu(parent=self.applyPushButton)
        self.applyMenu.setObjectName('applyMenu')

        self.preserveChildrenAction = QtWidgets.QAction('&Preserve Children', self.applyMenu)
        self.preserveChildrenAction.setObjectName('preserveChildrenAction')
        self.preserveChildrenAction.setCheckable(True)

        self.freezeTransformAction = QtWidgets.QAction('&Freeze Transform', self.applyMenu)
        self.freezeTransformAction.setObjectName('freezeTransformAction')
        self.freezeTransformAction.setCheckable(True)

        self.applyMenu.addActions([self.preserveChildrenAction, self.freezeTransformAction])
        self.applyPushButton.setMenu(self.applyMenu)

    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).loadSettings(settings)

        # Load user preferences
        #
        self.tabControl.setCurrentIndex(settings.value('editor/currentTabIndex', defaultValue=0))
        self.preserveChildren = bool(settings.value('editor/preserveChildren', defaultValue=0))
        self.freezeTransform = bool(settings.value('editor/freezeTransform', defaultValue=0))

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
        Returns the tab index that currently open.

        :rtype: int
        """

        return self.tabControl.currentIndex()

    def iterTabs(self):
        """
        Returns a generator that yields tab widgets.

        :rtype: iter
        """

        for i in range(self.tabControl.count()):

            yield self.tabControl.widget(i)
    # endregion

    # region Slots
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

    @QtCore.Slot(bool)
    def on_preserveChildrenAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for updating the preserve children flag.

        :type checked: bool
        :rtype: None
        """

        self._preserveChildren = self.sender().isChecked()

    @QtCore.Slot(bool)
    def on_freezeTransformAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for updating the freeze transform flag.

        :type checked: bool
        :rtype: None
        """

        self._freezeTransform = self.sender().isChecked()
    # endregion

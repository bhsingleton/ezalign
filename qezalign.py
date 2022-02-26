from PySide2 import QtCore, QtWidgets, QtGui
from dcc.userinterface import quicwindow, qmatrixedit, qvectoredit
from ezalign.tabs import qaligntab, qaimtab, qmatrixtab, qtimetab

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

        :keyword parent: QtWidgets.QWidget
        :keyword flags: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QEzAlign, self).__init__(*args, **kwargs)
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
    @classmethod
    def customWidgets(cls):
        """
        Returns a dictionary of custom widgets used by this class.

        :rtype: dict[str:type]
        """

        customWidgets = super(QEzAlign, cls).customWidgets()
        customWidgets['QAlignTab'] = qaligntab.QAlignTab
        customWidgets['QAimTab'] = qaimtab.QAimTab
        customWidgets['QMatrixTab'] = qmatrixtab.QMatrixTab
        customWidgets['QTimeTab'] = qtimetab.QTimeTab

        return customWidgets

    def postLoad(self):
        """
        Called after the user interface has been loaded.

        :rtype: None
        """

        # Assign tool button menu
        #
        self.preserveChildrenAction = QtWidgets.QAction('&Preserve Children')
        self.preserveChildrenAction.setCheckable(True)
        self.preserveChildrenAction.triggered.connect(self.preserveChildrenAction_triggered)

        self.freezeTransformAction = QtWidgets.QAction('&Freeze Transform')
        self.freezeTransformAction.setCheckable(True)
        self.freezeTransformAction.triggered.connect(self.freezeTransformAction_triggered)

        self.applyMenu = QtWidgets.QMenu(self.applyToolButton)
        self.applyMenu.addActions([self.preserveChildrenAction, self.freezeTransformAction])
        self.applyToolButton.setMenu(self.applyMenu)

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
        self.tabControl.setCurrentIndex(self.settings.value('editor/currentTabIndex', defaultValue=0, type=int))
        self.preserveChildren = self.settings.value('editor/preserveChildren', defaultValue=False, type=bool)
        self.freezeTransform = self.settings.value('editor/freezeTransform', defaultValue=False, type=bool)

        for tab in self.iterTabs():

            tab.loadSettings(self.settings)

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
        self.settings.setValue('editor/currentTabIndex', self.currentTabIndex())
        self.settings.setValue('editor/preserveChildren', self.preserveChildren)
        self.settings.setValue('editor/freezeTransform', self.freezeTransform)

        for tab in self.iterTabs():

            tab.saveSettings(self.settings)

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
    def applyButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for applying the selected operation.

        :type checked: bool
        :rtype: None
        """

        currentTab = self.currentTab()

        if currentTab is not None:

            currentTab.apply(preserveChildren=self.preserveChildren, freezeTransform=self.freezeTransform)

    def okayButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for applying the selected operation the closing the user interface.

        :type checked: bool
        :rtype: None
        """

        self.applyButton.click()
        self.close()

    def cancelButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for closing the user interface.

        :type checked: bool
        :rtype: None
        """

        self.close()

    def preserveChildrenAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for updating the preserve children flag.

        :type checked: bool
        :rtype: None
        """

        self._preserveChildren = self.sender().isChecked()

    def freezeTransformAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for updating the freeze transform flag.

        :type checked: bool
        :rtype: None
        """

        self._freezeTransform = self.sender().isChecked()
    # endregion

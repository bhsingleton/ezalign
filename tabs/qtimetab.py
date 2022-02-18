import json

from PySide2 import QtCore, QtWidgets, QtGui
from dcc import fnscene, fntransform
from dcc.userinterface import qrollout, qiconlibrary, qdivider, qtimespinbox, qseparator
from ezalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QMatchXYZWidget(QtWidgets.QWidget):
    """
    Overload of QWidget used to edit match flags for XYZ transform components.
    """

    # region Dunderscores
    def __init__(self, title, parent=None):
        """
        Private method called after a new instance has been created.

        :type title: str
        :type parent: QtWidgets.QWidget
        :rtype: None
        """

        # Call parent method
        #
        super(QMatchXYZWidget, self).__init__(parent=parent)

        # Assign horizontal layout
        #
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setSpacing(0)

        # Create push buttons
        #
        self.matchPushButton = QtWidgets.QPushButton(title)
        self.matchPushButton.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.matchPushButton.setFixedHeight(24)
        self.matchPushButton.setMinimumWidth(24)
        self.matchPushButton.setCheckable(True)
        self.matchPushButton.toggled.connect(self.matchPushButton_toggled)

        self.matchXPushButton = QtWidgets.QPushButton('X')
        self.matchXPushButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.matchXPushButton.setFixedSize(QtCore.QSize(15, 24))
        self.matchXPushButton.setCheckable(True)

        self.matchYPushButton = QtWidgets.QPushButton('Y')
        self.matchYPushButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.matchYPushButton.setFixedSize(QtCore.QSize(15, 24))
        self.matchYPushButton.setCheckable(True)

        self.matchZPushButton = QtWidgets.QPushButton('Z')
        self.matchZPushButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.matchZPushButton.setFixedSize(QtCore.QSize(15, 24))
        self.matchZPushButton.setCheckable(True)

        self.layout().addWidget(self.matchPushButton)
        self.layout().addWidget(self.matchXPushButton)
        self.layout().addWidget(self.matchYPushButton)
        self.layout().addWidget(self.matchZPushButton)

        self.matchButtonGroup = QtWidgets.QButtonGroup(parent=self)
        self.matchButtonGroup.setExclusive(False)
        self.matchButtonGroup.addButton(self.matchXPushButton, id=0)
        self.matchButtonGroup.addButton(self.matchYPushButton, id=1)
        self.matchButtonGroup.addButton(self.matchZPushButton, id=2)
        self.matchButtonGroup.idToggled.connect(self.matchButtonGroup_idToggled)
    # endregion

    # region Methods
    def matches(self):
        """
        Returns a list of state values for each button.

        :rtype: list[bool, bool, bool]
        """

        return [x.isChecked() for x in self.matchButtonGroup.buttons()]

    def setMatches(self, matches):
        """
        Updates the match state for each button.

        :type matches: list[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matches):

            self.matchButtonGroup.button(index).setChecked(match)
    # endregion

    # region Slots
    def matchPushButton_toggled(self, state):
        """
        Toggled slot method responsible for overriding the button group state.

        :type state: bool
        :rtype: None
        """

        for button in self.matchButtonGroup.buttons():

            button.setChecked(state)

    def matchButtonGroup_idToggled(self, id):
        """
        Id toggled slot method responsible for syncing the master button with the button group.

        :type id: int
        :rtype: None
        """

        isChecked = self.matchPushButton.isChecked()
        matches = self.matches()

        if isChecked and not all(matches):

            self.matchPushButton.setChecked(False)
            self.setMatches(matches)

        elif not isChecked and all(matches):

            self.matchPushButton.setChecked(True)

        else:

            pass
    # endregion


class QAlignRollout(qrollout.QRollout):
    """
    Overload of QRollout used to align transforms over time.
    """

    # region Dunderscores
    def __init__(self, title, parent=None, f=QtCore.Qt.WindowFlags()):
        """
        Private method called after a new instance has been created.

        :type parent: QtWidgets.QWidget
        :type f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QAlignRollout, self).__init__(title, parent=parent, f=f)

        # Assign vertical layout
        #
        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('CentralLayout')
        self.centralLayout.setSpacing(4)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setObjectName('CentralWidget')
        self.centralWidget.setLayout(self.centralLayout)

        self.layout().addWidget(self.centralWidget)

        # Create node widgets
        #
        self.sourceButton = QtWidgets.QPushButton('Parent')
        self.sourceButton.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.sourceButton.setFixedHeight(24)
        self.sourceButton.setMinimumWidth(48)
        self.sourceButton.setToolTip('Picks the node to align to.')
        self.sourceButton.clicked.connect(self.button_clicked)

        self.switchButton = QtWidgets.QPushButton(qiconlibrary.getIconByName('switch'), '')
        self.switchButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.switchButton.setFixedSize(QtCore.QSize(24, 24))
        self.switchButton.clicked.connect(self.switchButton_clicked)

        self.targetButton = QtWidgets.QPushButton('Child')
        self.targetButton.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.targetButton.setFixedHeight(24)
        self.targetButton.setMinimumWidth(48)
        self.targetButton.setToolTip('Picks the node to be aligned.')
        self.targetButton.clicked.connect(self.button_clicked)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addWidget(self.sourceButton)
        self.buttonLayout.addWidget(self.switchButton)
        self.buttonLayout.addWidget(self.targetButton)

        self.centralLayout.addLayout(self.buttonLayout)
        self.centralLayout.addWidget(qdivider.QDivider(QtCore.Qt.Horizontal))

        # Create time range widgets
        #
        self.startCheckBox = QtWidgets.QCheckBox('Start:')
        self.startCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.startCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.startCheckBox.setChecked(True)
        self.startCheckBox.stateChanged.connect(self.startCheckBox_stateChanged)

        self.startSpinBox = qtimespinbox.QTimeSpinBox()
        self.startSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.startSpinBox.setFixedHeight(24)
        self.startSpinBox.setMinimumWidth(24)
        self.startSpinBox.setDefaultType(qtimespinbox.DefaultType.StartTime)
        self.startSpinBox.setValue(0)

        self.endCheckBox = QtWidgets.QCheckBox('End:')
        self.endCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.endCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.endCheckBox.setChecked(True)
        self.endCheckBox.stateChanged.connect(self.endCheckBox_stateChanged)

        self.endSpinBox = qtimespinbox.QTimeSpinBox()
        self.endSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.endSpinBox.setFixedHeight(24)
        self.endSpinBox.setMinimumWidth(24)
        self.endSpinBox.setDefaultType(qtimespinbox.DefaultType.EndTime)
        self.endSpinBox.setValue(1)

        self.stepCheckBox = QtWidgets.QCheckBox('Step:')
        self.stepCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.stepCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.stepCheckBox.setChecked(True)
        self.stepCheckBox.stateChanged.connect(self.stepCheckBox_stateChanged)

        self.stepSpinBox = QtWidgets.QSpinBox()
        self.stepSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.stepSpinBox.setFixedHeight(24)
        self.stepSpinBox.setMinimumWidth(24)
        self.stepSpinBox.setMinimum(1)
        self.stepSpinBox.setValue(1)

        self.timeRangeLayout = QtWidgets.QHBoxLayout()
        self.timeRangeLayout.addWidget(self.startCheckBox)
        self.timeRangeLayout.addWidget(self.startSpinBox)
        self.timeRangeLayout.addWidget(self.endCheckBox)
        self.timeRangeLayout.addWidget(self.endSpinBox)
        self.timeRangeLayout.addWidget(self.stepCheckBox)
        self.timeRangeLayout.addWidget(self.stepSpinBox)

        self.centralLayout.addLayout(self.timeRangeLayout)
        self.centralLayout.addWidget(qdivider.QDivider(QtCore.Qt.Horizontal))

        # Create match transform widgets
        #
        self.matchTranslateXYZWidget = QMatchXYZWidget('Pos')
        self.matchRotateXYZWidget = QMatchXYZWidget('Rot')
        self.matchScaleXYZWidget = QMatchXYZWidget('Scale')

        self.matchLayout = QtWidgets.QHBoxLayout()
        self.matchLayout.addWidget(self.matchTranslateXYZWidget)
        self.matchLayout.addWidget(self.matchRotateXYZWidget)
        self.matchLayout.addWidget(self.matchScaleXYZWidget)

        self.centralLayout.addLayout(self.matchLayout)
        self.centralLayout.addWidget(qdivider.QDivider(QtCore.Qt.Horizontal))

        # Create maintain offset widgets
        #
        self.maintainOffsetLabel = QtWidgets.QLabel('Maintain Offset:')
        self.maintainTranslateCheckBox = QtWidgets.QCheckBox('Position')
        self.maintainRotateCheckBox = QtWidgets.QCheckBox('Rotation')
        self.maintainScaleCheckBox = QtWidgets.QCheckBox('Scale')

        self.maintainOffsetLayout = QtWidgets.QHBoxLayout()
        self.maintainOffsetLayout.addWidget(self.maintainOffsetLabel)
        self.maintainOffsetLayout.addWidget(self.maintainTranslateCheckBox)
        self.maintainOffsetLayout.addWidget(self.maintainRotateCheckBox)
        self.maintainOffsetLayout.addWidget(self.maintainScaleCheckBox)

        self.centralLayout.addLayout(self.maintainOffsetLayout)

        # Insert additional menu actions
        #
        self.addAlignmentAction = QtWidgets.QAction('Add Alignment', parent=self.customContextMenu)
        self.removeAlignmentAction = QtWidgets.QAction('Remove Alignment', parent=self.customContextMenu)

        self.customContextMenu.insertActions(
            self.expandAction,
            [
                self.addAlignmentAction,
                self.removeAlignmentAction,
                qseparator.QSeparator('', parent=self.customContextMenu)
            ]
        )

    def __getstate__(self):
        """
        Private method that returns a state object for this instance.

        :rtype: dict
        """

        return {
            'isChecked': self.isChecked(),
            'expanded': self.expanded(),
            'sourceName': self.sourceName,
            'targetName': self.targetName,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'step': self.step,
            'matchTranslate': self.matchTranslate,
            'matchRotate': self.matchRotate,
            'matchScale': self.matchScale,
            'maintainTranslate': self.maintainTranslate,
            'maintainRotate': self.maintainRotate,
            'maintainScale': self.maintainScale
        }

    def __setstate__(self, state):
        """
        Private method that updates the instance from a state object.

        :type state: dict
        :rtype: None
        """

        self.setChecked(state.get('isChecked', True))
        self.setExpanded(state.get('expanded', True))
        self.sourceName = state.get('sourceName', '')
        self.targetName = state.get('targetName', '')
        self.startTime = state.get('startTime', 0)
        self.endTime = state.get('endTime', 1)
        self.step = state.get('step', 1)
        self.matchTranslate = state.get('matchTranslate', [True, True, True])
        self.matchRotate = state.get('matchRotate', [True, True, True])
        self.matchScale = state.get('matchScale', [False, False, False])
        self.maintainTranslate = (state.get('maintainTranslate', False))
        self.maintainRotate = (state.get('maintainRotate', False))
        self.maintainScale = (state.get('maintainScale', False))
    # endregion

    # region Properties
    @property
    def sourceName(self):
        """
        Getter method that returns the source node name.

        :rtype: str
        """

        return self.sourceButton.text()

    @sourceName.setter
    def sourceName(self, sourceName):
        """
        Setter method that updates the source node name.

        :type sourceName: str
        :rtype: None
        """

        self.sourceButton.setText(sourceName)
        self.invalidate()

    @property
    def targetName(self):
        """
        Getter method that returns the target node name.

        :rtype: str
        """

        return self.targetButton.text()

    @targetName.setter
    def targetName(self, targetName):
        """
        Setter method that updates the target node name.

        :type targetName: str
        :rtype: None
        """

        self.targetButton.setText(targetName)
        self.invalidate()

    @property
    def startTime(self):
        """
        Getter method that returns the start time.

        :rtype: int
        """

        return self.startSpinBox.value()

    @startTime.setter
    def startTime(self, startTime):
        """
        Setter method that updates the start time.

        :type startTime: int
        :rtype: None
        """

        self.startSpinBox.setValue(startTime)

    @property
    def endTime(self):
        """
        Getter method that returns the end time.

        :rtype: int
        """

        return self.endSpinBox.value()

    @endTime.setter
    def endTime(self, endTime):
        """
        Setter method that updates the end time.

        :type endTime: int
        :rtype: None
        """

        self.endSpinBox.setValue(endTime)

    @property
    def step(self):
        """
        Getter method that returns the step interval.

        :rtype: int
        """

        return self.stepSpinBox.value()

    @step.setter
    def step(self, step):
        """
        Setter method that updates the step interval.

        :type step: int
        :rtype: None
        """

        self.stepSpinBox.setValue(step)

    @property
    def matchTranslate(self):
        """
        Getter method that returns the match translate flag.

        :rtype: list[bool, bool, bool]
        """

        return self.matchTranslateXYZWidget.matches()

    @matchTranslate.setter
    def matchTranslate(self, matchTranslate):
        """
        Setter method that updates the match translate flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchTranslateXYZWidget.setMatches(matchTranslate)

    @property
    def matchRotate(self):
        """
        Getter method that returns the match rotate flag.

        :rtype: list[bool, bool, bool]
        """

        return self.matchRotateXYZWidget.matches()

    @matchRotate.setter
    def matchRotate(self, matchRotate):
        """
        Setter method that updates the match rotate flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchRotateXYZWidget.setMatches(matchRotate)

    @property
    def matchScale(self):
        """
        Getter method that returns the match scale flag.

        :rtype: list[bool, bool, bool]
        """

        return self.matchScaleXYZWidget.matches()

    @matchScale.setter
    def matchScale(self, matchScale):
        """
        Setter method that updates the match scale flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchScaleXYZWidget.setMatches(matchScale)
    
    @property
    def maintainTranslate(self):
        """
        Getter method that returns the maintain translate flag.
        
        :rtype: bool
        """
        
        return self.maintainTranslateCheckBox.isChecked()
    
    @maintainTranslate.setter
    def maintainTranslate(self, maintainTranslate):
        """
        Setter method that updates the maintain translate flag.

        :rtype: bool
        """
        
        self.maintainTranslateCheckBox.setChecked(maintainTranslate)
    
    @property
    def maintainRotate(self):
        """
        Getter method that returns the maintain rotate flag.

        :rtype: bool
        """

        return self.maintainRotateCheckBox.isChecked()

    @maintainRotate.setter
    def maintainRotate(self, maintainRotate):
        """
        Setter method that updates the maintain rotate flag.

        :rtype: bool
        """

        self.maintainRotateCheckBox.setChecked(maintainRotate)

    @property
    def maintainScale(self):
        """
        Getter method that returns the maintain scale flag.

        :rtype: bool
        """

        return self.maintainScaleCheckBox.isChecked()

    @maintainScale.setter
    def maintainScale(self, maintainScale):
        """
        Setter method that updates the maintain scale flag.

        :rtype: bool
        """

        self.maintainScaleCheckBox.setChecked(maintainScale)
    # endregion

    # region Methods
    def invalidate(self):
        """
        Re-concatenates the title of this rollout.

        :rtype: None
        """

        self.setTitle('Align %s to %s' % (self.targetName, self.sourceName))

    def apply(self):
        """
        Aligns the target node to the source node over the specified amount of time.

        :rtype: None
        """

        # Initialize source interface
        #
        fnSource = fntransform.FnTransform()
        isSourceValid = fnSource.trySetObject(self.sourceName)

        if not isSourceValid:

            log.warning('Unable to locate parent node: %s!' % self.sourceName)
            return

        # Initialize target interface
        #
        fnTarget = fntransform.FnTransform()
        isTargetValid = fnTarget.trySetObject(self.targetName)

        if not isTargetValid:

            log.warning('Unable to locate child node: %s!' % self.sourceName)
            return

        # Collect skip flags
        #
        skipTranslateX, skipTranslateY, skipTranslateZ = (not x for x in self.matchTranslate)
        skipRotateX, skipRotateY, skipRotateZ = (not x for x in self.matchRotate)
        skipScaleX, skipScaleY, skipScaleZ = (not x for x in self.matchScale)

        # Calculate offset matrix
        #
        offsetMatrix = fnTarget.offsetMatrix(
            fnSource.object(),
            maintainTranslate=self.maintainTranslate,
            maintainRotate=self.maintainRotate,
            maintainScale=self.maintainScale
        )

        # Iterate through time range
        #
        fnScene = fnscene.FnScene()
        fnScene.enableAutoKey()

        for i in range(self.startTime, self.endTime, self.step):

            fnScene.setTime(i)
            fnTarget.copyTransform(
                fnSource.object(),
                offsetMatrix=offsetMatrix,
                skipTranslateX=skipTranslateX, skipTranslateY=skipTranslateY, skipTranslateZ=skipTranslateZ,
                skipRotateX=skipRotateX, skipRotateY=skipRotateY, skipRotateZ=skipRotateZ,
                skipScaleX=skipScaleX, skipScaleY=skipScaleY, skipScaleZ=skipScaleZ
            )

        fnScene.disableAutoKey()
    # endregion

    # region Slots
    def button_clicked(self, checked=False):
        """
        Clicked slot method responsible for updating the source name.

        :type checked: bool
        :rtype: None
        """

        fnTransform = fntransform.FnTransform()

        selection = fnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount > 0:

            fnTransform.setObject(selection[0])

            self.sender().setText(fnTransform.name())
            self.invalidate()

    def switchButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for switch the parent and child nodes.

        :type checked: bool
        :rtype: None
        """

        self.sourceName, self.targetName = self.targetName, self.sourceName

    def startCheckBox_stateChanged(self, state):
        """
        State changed slot method responsible for enabling the associated spin box.

        :type state: bool
        :rtype:
        """

        self.startSpinBox.setEnabled(state)

    def endCheckBox_stateChanged(self, state):
        """
        State changed slot method responsible for enabling the associated spin box.

        :type state: bool
        :rtype:
        """

        self.endSpinBox.setEnabled(state)

    def stepCheckBox_stateChanged(self, state):
        """
        State changed slot method responsible for enabling the associated spin box.

        :type state: bool
        :rtype:
        """

        self.stepSpinBox.setEnabled(state)
    # endregion


class QTimeTab(qabstracttab.QAbstractTab):
    """
    Overload of QAbstractTab used to align a series of transforms over time.
    """

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :keyword parent: QtWidgets.QWidget
        :keyword f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QTimeTab, self).__init__(*args, **kwargs)

    def __build__(self, *args, **kwargs):
        """
        Private method used to build the user interface.

        :rtype: None
        """

        # Call parent method
        #
        super(QTimeTab, self).__build__(*args, **kwargs)

        # Assign vertical layout
        #
        self.setLayout(QtWidgets.QVBoxLayout())

        # Create sequence scroll area
        #
        self.containerLayout = QtWidgets.QVBoxLayout()
        self.containerLayout.setAlignment(QtCore.Qt.AlignTop)
        self.containerLayout.setSpacing(4)

        self.containerWidget = QtWidgets.QWidget()
        self.containerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.containerWidget.setLayout(self.containerLayout)

        self.alignScrollArea = QtWidgets.QScrollArea()
        self.alignScrollArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.alignScrollArea.setWidget(self.containerWidget)
        self.alignScrollArea.setWidgetResizable(True)

        self.layout().addWidget(self.alignScrollArea)
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        # Clear all previous alignments
        #
        self.clearAlignments()

        # Load object states
        # If there aren't any then create a default alignment
        #
        states = json.loads(settings.value('tabs/time/alignments', defaultValue='[]', type=str))
        numStates = len(states)

        if numStates > 0:

            for state in states:

                alignment = self.addAlignment()
                alignment.__setstate__(state)

        else:

            self.addAlignment()

    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        settings.setValue('tabs/time/alignments', json.dumps([x.__getstate__() for x in self.iterAlignments()]))

    def numAlignments(self):
        """
        Evaluates the number of alignments.

        :rtype: int
        """

        return self.containerLayout.count()

    def evaluateNumAlignments(self):
        """
        Evaluates the number of enabled alignments.

        :rtype: int
        """

        return len(self.alignments(skipUnchecked=True)) > 0

    def iterAlignments(self, skipUnchecked=False):
        """
        Returns a generator that yields alignment rollouts.

        :type skipUnchecked: bool
        :rtype: iter
        """

        # Iterate through layout items
        #
        for i in range(self.numAlignments()):

            alignment = self.containerLayout.itemAt(i).widget()

            if skipUnchecked and not alignment.isChecked():

                continue

            else:

                yield alignment

    def alignments(self, skipUnchecked=False):
        """
        Returns a list of alignment rollouts.

        :type skipUnchecked: bool
        :rtype: list[QAlignRollout]
        """

        return list(self.iterAlignments(skipUnchecked=skipUnchecked))

    def addAlignment(self):
        """
        Adds a new alignment rollout to the scroll area.

        :rtype: QAlignRollout
        """

        rollout = QAlignRollout('')
        rollout.setCheckable(True)
        rollout.showCheckBox()
        rollout.showGripper()
        rollout.addAlignmentAction.triggered.connect(self.addAlignmentAction_triggered)
        rollout.removeAlignmentAction.triggered.connect(self.removeAlignmentAction_triggered)

        self.containerLayout.addWidget(rollout)

        return rollout

    def clearAlignments(self):
        """
        Removes all of the current alignments.

        :rtype: None
        """

        for alignment in reversed(self.alignments()):

            alignment.deleteLater()

    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Aligns the active selection to the user defined matrix.

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        # Check if any alignments are enabled
        #
        if self.evaluateNumAlignments() == 0:

            return

        # Iterate through alignments
        #
        for alignment in self.iterAlignments(skipUnchecked=True):

            alignment.apply()
    # endregion

    # region Slots
    def addAlignmentAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for adding a new alignment.

        :type checked: bool
        :rtype: None
        """

        self.addAlignment()

    def removeAlignmentAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for removing the associated rollout.

        :type checked: bool
        :rtype: None
        """

        numAlignments = self.numAlignments()

        if numAlignments > 1:

            rollout = self.sender().parentWidget().parentWidget()
            rollout.deleteLater()
    # endregion

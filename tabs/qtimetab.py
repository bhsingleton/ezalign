import json

from PySide2 import QtCore, QtWidgets, QtGui
from dcc import fnscene, fntransform
from dcc.ui import qrollout, qiconlibrary, qdivider, qtimespinbox, qxyzwidget, qseparator
from ezalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAlignRollout(qrollout.QRollout):
    """
    Overload of QRollout used to align transforms over time.
    """

    # region Dunderscores
    def __init__(self, title, **kwargs):
        """
        Private method called after a new instance has been created.

        :type parent: QtWidgets.QWidget
        :type f: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QAlignRollout, self).__init__(title, **kwargs)

        # Assign vertical layout
        #
        self.centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.centralLayout)

        # Create node widgets
        #
        self.sourcePushButton = QtWidgets.QPushButton('Parent')
        self.sourcePushButton.setObjectName('sourcePushButton')
        self.sourcePushButton.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.sourcePushButton.setFixedHeight(24)
        self.sourcePushButton.setMinimumWidth(48)
        self.sourcePushButton.setToolTip('Picks the node to align to.')
        self.sourcePushButton.clicked.connect(self.pushButton_clicked)

        self.switchPushButton = QtWidgets.QPushButton(qiconlibrary.getIconByName('switch'), '')
        self.switchPushButton.setObjectName('switchButton')
        self.switchPushButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.switchPushButton.setFixedSize(QtCore.QSize(24, 24))
        self.switchPushButton.clicked.connect(self.switchPushButton_clicked)

        self.targetPushButton = QtWidgets.QPushButton('Child')
        self.targetPushButton.setObjectName('targetButton')
        self.targetPushButton.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.targetPushButton.setFixedHeight(24)
        self.targetPushButton.setMinimumWidth(48)
        self.targetPushButton.setToolTip('Picks the node to be aligned.')
        self.targetPushButton.clicked.connect(self.pushButton_clicked)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName('buttonLayout')
        self.buttonLayout.addWidget(self.sourcePushButton)
        self.buttonLayout.addWidget(self.switchPushButton)
        self.buttonLayout.addWidget(self.targetPushButton)

        self.centralLayout.addLayout(self.buttonLayout)
        self.centralLayout.addWidget(qdivider.QDivider(QtCore.Qt.Horizontal))

        # Create time range widgets
        #
        self.startCheckBox = QtWidgets.QCheckBox('Start:')
        self.startCheckBox.setObjectName('startCheckBox')
        self.startCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.startCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.startCheckBox.setChecked(True)
        self.startCheckBox.stateChanged.connect(self.startCheckBox_stateChanged)

        self.startSpinBox = qtimespinbox.QTimeSpinBox()
        self.startSpinBox.setObjectName('startSpinBox')
        self.startSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.startSpinBox.setFixedHeight(24)
        self.startSpinBox.setMinimumWidth(24)
        self.startSpinBox.setDefaultType(qtimespinbox.DefaultType.StartTime)
        self.startSpinBox.setValue(0)

        self.endCheckBox = QtWidgets.QCheckBox('End:')
        self.endCheckBox.setObjectName('endCheckBox')
        self.endCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.endCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.endCheckBox.setChecked(True)
        self.endCheckBox.stateChanged.connect(self.endCheckBox_stateChanged)

        self.endSpinBox = qtimespinbox.QTimeSpinBox()
        self.endSpinBox.setObjectName('endSpinBox')
        self.endSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.endSpinBox.setFixedHeight(24)
        self.endSpinBox.setMinimumWidth(24)
        self.endSpinBox.setDefaultType(qtimespinbox.DefaultType.EndTime)
        self.endSpinBox.setValue(1)

        self.stepCheckBox = QtWidgets.QCheckBox('Step:')
        self.stepCheckBox.setObjectName('stepCheckBox')
        self.stepCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.stepCheckBox.setFixedSize(QtCore.QSize(48, 24))
        self.stepCheckBox.setChecked(True)
        self.stepCheckBox.stateChanged.connect(self.stepCheckBox_stateChanged)

        self.stepSpinBox = QtWidgets.QSpinBox()
        self.stepSpinBox.setObjectName('stepSpinBox')
        self.stepSpinBox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.stepSpinBox.setFixedHeight(24)
        self.stepSpinBox.setMinimumWidth(24)
        self.stepSpinBox.setMinimum(1)
        self.stepSpinBox.setValue(1)

        self.timeRangeLayout = QtWidgets.QHBoxLayout()
        self.timeRangeLayout.setObjectName('timeRangeLayout')
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
        self.matchTranslateWidget = qxyzwidget.QXyzWidget('Pos')
        self.matchTranslateWidget.setObjectName('matchTranslateWidget')
        self.matchTranslateWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.matchTranslateWidget.setFixedHeight(24)

        self.matchRotateWidget = qxyzwidget.QXyzWidget('Rot')
        self.matchRotateWidget.setObjectName('matchRotateWidget')
        self.matchRotateWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.matchRotateWidget.setFixedHeight(24)

        self.matchScaleWidget = qxyzwidget.QXyzWidget('Scale')
        self.matchScaleWidget.setObjectName('matchScaleWidget')
        self.matchScaleWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.matchScaleWidget.setFixedHeight(24)

        self.matchLayout = QtWidgets.QHBoxLayout()
        self.matchLayout.setObjectName('matchLayout')
        self.matchLayout.setContentsMargins(0, 0, 0, 0)
        self.matchLayout.addWidget(self.matchTranslateWidget)
        self.matchLayout.addWidget(self.matchRotateWidget)
        self.matchLayout.addWidget(self.matchScaleWidget)

        self.centralLayout.addLayout(self.matchLayout)
        self.centralLayout.addWidget(qdivider.QDivider(QtCore.Qt.Horizontal))

        # Create maintain offset widgets
        #
        self.maintainLabel = QtWidgets.QLabel('Maintain:')
        self.maintainLabel.setObjectName('maintainOffsetLabel')
        self.maintainLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maintainLabel.setFixedHeight(24)
        self.maintainLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.maintainTranslateCheckBox = QtWidgets.QCheckBox('Position')
        self.maintainTranslateCheckBox.setObjectName('maintainTranslateCheckBox')
        self.maintainTranslateCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maintainTranslateCheckBox.setFixedHeight(24)

        self.maintainRotateCheckBox = QtWidgets.QCheckBox('Rotation')
        self.maintainRotateCheckBox.setObjectName('maintainRotateCheckBox')
        self.maintainRotateCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maintainRotateCheckBox.setFixedHeight(24)

        self.maintainScaleCheckBox = QtWidgets.QCheckBox('Scale')
        self.maintainScaleCheckBox.setObjectName('maintainScaleCheckBox')
        self.maintainScaleCheckBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maintainScaleCheckBox.setFixedHeight(24)

        self.maintainLayout = QtWidgets.QHBoxLayout()
        self.maintainLayout.setObjectName('maintainLayout')
        self.maintainLayout.addWidget(self.maintainLabel)
        self.maintainLayout.addWidget(self.maintainTranslateCheckBox)
        self.maintainLayout.addWidget(self.maintainRotateCheckBox)
        self.maintainLayout.addWidget(self.maintainScaleCheckBox)

        self.centralLayout.addLayout(self.maintainLayout)

        # Insert additional menu actions
        #
        menu = self.menu()

        self.addAlignmentAction = QtWidgets.QAction('Add Alignment', parent=menu)
        self.removeAlignmentAction = QtWidgets.QAction('Remove Alignment', parent=menu)

        menu.insertActions(
            menu.actions()[0],
            [
                self.addAlignmentAction,
                self.removeAlignmentAction,
                qseparator.QSeparator('', parent=menu)
            ]
        )

    def __getstate__(self):
        """
        Private method that returns a state object for this instance.

        :rtype: dict
        """

        return {
            'isChecked': self.isChecked(),
            'isExpanded': self.isExpanded(),
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

        return self.sourcePushButton.text()

    @sourceName.setter
    def sourceName(self, sourceName):
        """
        Setter method that updates the source node name.

        :type sourceName: str
        :rtype: None
        """

        self.sourcePushButton.setText(sourceName)
        self.invalidate()

    @property
    def targetName(self):
        """
        Getter method that returns the target node name.

        :rtype: str
        """

        return self.targetPushButton.text()

    @targetName.setter
    def targetName(self, targetName):
        """
        Setter method that updates the target node name.

        :type targetName: str
        :rtype: None
        """

        self.targetPushButton.setText(targetName)
        self.invalidate()

    @property
    def startTime(self):
        """
        Getter method that returns the start time.

        :rtype: int
        """

        if self.startCheckBox.isChecked():

            return self.startSpinBox.value()

        else:

            return fnscene.FnScene().getStartTime()

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

        if self.endCheckBox.isChecked():

            return self.endSpinBox.value()

        else:

            return fnscene.FnScene().getEndTime()

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

        return self.matchTranslateWidget.matches()

    @matchTranslate.setter
    def matchTranslate(self, matchTranslate):
        """
        Setter method that updates the match translate flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchTranslateWidget.setMatches(matchTranslate)

    @property
    def matchRotate(self):
        """
        Getter method that returns the match rotate flag.

        :rtype: list[bool, bool, bool]
        """

        return self.matchRotateWidget.matches()

    @matchRotate.setter
    def matchRotate(self, matchRotate):
        """
        Setter method that updates the match rotate flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchRotateWidget.setMatches(matchRotate)

    @property
    def matchScale(self):
        """
        Getter method that returns the match scale flag.

        :rtype: list[bool, bool, bool]
        """

        return self.matchScaleWidget.matches()

    @matchScale.setter
    def matchScale(self, matchScale):
        """
        Setter method that updates the match scale flag.

        :rtype: list[bool, bool, bool]
        """

        self.matchScaleWidget.setMatches(matchScale)
    
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
    def pushButton_clicked(self, checked=False):
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

    def switchPushButton_clicked(self, checked=False):
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
        Private method called after a new instance has been created.

        :key parent: QtWidgets.QWidget
        :key f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QTimeTab, self).__init__(*args, **kwargs)
    # endregion

    # region Methods
    def postLoad(self):
        """
        Called after the user interface has been loaded.

        :rtype: None
        """

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scrollAreaContents.setLayout(layout)

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

        return self.scrollAreaContents.layout().count()

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
        layout = self.scrollAreaContents.layout()

        for i in range(self.numAlignments()):

            alignment = layout.itemAt(i).widget()

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
        rollout.setGrippable(True)
        rollout.addAlignmentAction.triggered.connect(self.on_addAlignmentAction_triggered)
        rollout.removeAlignmentAction.triggered.connect(self.on_removeAlignmentAction_triggered)

        self.scrollAreaContents.layout().addWidget(rollout)

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
    @QtCore.Slot(bool)
    def on_addAlignmentAction_triggered(self, checked=False):
        """
        Triggered slot method responsible for adding a new alignment.

        :type checked: bool
        :rtype: None
        """

        self.addAlignment()

    @QtCore.Slot(bool)
    def on_removeAlignmentAction_triggered(self, checked=False):
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

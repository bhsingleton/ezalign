import numpy
import json

from PySide2 import QtCore, QtWidgets, QtGui
from copy import deepcopy
from dcc import fnnode, fntransform, fnmesh
from dcc.math import matrixmath, vectormath
from dcc.userinterface import qmatrixedit
from ezalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QMatrixTab(qabstracttab.QAbstractTab):
    """
    Overload of QAbstractTab used to align transforms to a custom matrix.
    """

    # region Dunderscores
    __decimals__ = 3
    __axis__ = vectormath.X_AXIS_VECTOR, vectormath.Y_AXIS_VECTOR, vectormath.Z_AXIS_VECTOR

    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :keyword parent: QtWidgets.QWidget
        :keyword f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QMatrixTab, self).__init__(*args, **kwargs)

        # Declare class variables
        #
        self._origin = numpy.array([0.0, 0.0, 0.0])
        self._forwardAxis = 0
        self._forwardVector = numpy.array([1.0, 0.0, 0.0])
        self._upAxis = 1
        self._upVector = numpy.array([0.0, 1.0, 0.0])
        
    def __build__(self, *args, **kwargs):
        """
        Private method used to build the user interface.

        :rtype: None
        """

        # Call parent method
        #
        super(QMatrixTab, self).__build__(*args, **kwargs)

        # Assign vertical layout
        #
        self.setLayout(QtWidgets.QVBoxLayout())

        # Create matrix group box
        #
        self.matrixLayout = QtWidgets.QHBoxLayout()
        self.matrixLayout.setSpacing(8)
        self.matrixLayout.setContentsMargins(0, 0, 0, 0)

        self.matrixGroupBox = QtWidgets.QGroupBox('4x4 Matrix:')
        self.matrixGroupBox.setLayout(self.matrixLayout)

        self.layout().addWidget(self.matrixGroupBox)

        # Create matrix labels
        #
        self.xAxisLabel = QtWidgets.QLabel('X-Axis:')
        self.xAxisLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.xAxisLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.xAxisLabel.setFixedSize(QtCore.QSize(60, 24))

        self.yAxisLabel = QtWidgets.QLabel('Y-Axis:')
        self.yAxisLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.yAxisLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.yAxisLabel.setFixedSize(QtCore.QSize(60, 24))

        self.zAxisLabel = QtWidgets.QLabel('Z-Axis:')
        self.zAxisLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.zAxisLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.zAxisLabel.setFixedSize(QtCore.QSize(60, 24))

        self.originButton = QtWidgets.QPushButton('Origin:')
        self.originButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.originButton.setFixedSize(QtCore.QSize(60, 24))
        self.originButton.setToolTip('LMB averages the center positions.')
        self.originButton.clicked.connect(self.originButton_clicked)

        self.labelLayout = QtWidgets.QVBoxLayout()
        self.labelLayout.setSpacing(8)
        self.labelLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout.addWidget(self.xAxisLabel)
        self.labelLayout.addWidget(self.yAxisLabel)
        self.labelLayout.addWidget(self.zAxisLabel)
        self.labelLayout.addWidget(self.originButton)

        # Create matrix widget
        #
        self.matrixEdit = qmatrixedit.QMatrixEdit(4, 4, parent=self)

        self.matrixLayout.addLayout(self.labelLayout)
        self.matrixLayout.addWidget(self.matrixEdit)

        # Create forward axis group box
        #
        self.forwardAxisLayout = QtWidgets.QHBoxLayout()

        self.forwardAxisGroupBox = QtWidgets.QGroupBox('Forward Axis:')
        self.forwardAxisGroupBox.setLayout(self.forwardAxisLayout)

        self.forwardAxisButton = QtWidgets.QPushButton('Pick')
        self.forwardAxisButton.setToolTip('LMB averages the center positions. Ctrl+LMB gets the axis vector. Alt+LMB averages the vertex normals.')
        self.forwardAxisButton.clicked.connect(self.forwardAxisButton_clicked)

        self.forwardXRadioButton = QtWidgets.QRadioButton('X')
        self.forwardYRadioButton = QtWidgets.QRadioButton('Y')
        self.forwardZRadioButton = QtWidgets.QRadioButton('Z')

        self.forwardAxisButtonGroup = QtWidgets.QButtonGroup(parent=self)
        self.forwardAxisButtonGroup.addButton(self.forwardXRadioButton, id=0)
        self.forwardAxisButtonGroup.addButton(self.forwardYRadioButton, id=1)
        self.forwardAxisButtonGroup.addButton(self.forwardZRadioButton, id=2)
        self.forwardAxisButtonGroup.buttons()[0].setChecked(True)
        self.forwardAxisButtonGroup.idClicked.connect(self.forwardAxisButtonGroup_idClicked)

        self.forwardAxisLayout.addWidget(self.forwardAxisButton)
        self.forwardAxisLayout.addWidget(self.forwardXRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardYRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardZRadioButton)

        self.layout().addWidget(self.forwardAxisGroupBox)

        # Create up axis group box
        #
        self.upAxisLayout = QtWidgets.QHBoxLayout()

        self.upAxisGroupBox = QtWidgets.QGroupBox('Up Axis:')
        self.upAxisGroupBox.setLayout(self.upAxisLayout)

        self.upAxisButton = QtWidgets.QPushButton('Pick')
        self.upAxisButton.setToolTip('LMB averages the center positions. Ctrl+LMB gets the axis vector. Alt+LMB averages the vertex normals.')
        self.upAxisButton.clicked.connect(self.upAxisButton_clicked)

        self.upXRadioButton = QtWidgets.QRadioButton('X')
        self.upYRadioButton = QtWidgets.QRadioButton('Y')
        self.upZRadioButton = QtWidgets.QRadioButton('Z')

        self.upAxisButtonGroup = QtWidgets.QButtonGroup(parent=self)
        self.upAxisButtonGroup.addButton(self.upXRadioButton, id=0)
        self.upAxisButtonGroup.addButton(self.upYRadioButton, id=1)
        self.upAxisButtonGroup.addButton(self.upZRadioButton, id=2)
        self.upAxisButtonGroup.buttons()[1].setChecked(True)
        self.upAxisButtonGroup.idClicked.connect(self.upAxisButtonGroup_idClicked)

        self.upAxisLayout.addWidget(self.upAxisButton)
        self.upAxisLayout.addWidget(self.upXRadioButton)
        self.upAxisLayout.addWidget(self.upYRadioButton)
        self.upAxisLayout.addWidget(self.upZRadioButton)

        self.layout().addWidget(self.upAxisGroupBox)
    # endregion

    # region Properties
    @property
    def origin(self):
        """
        Getter method that returns the origin.

        :rtype: numpy.array
        """

        return self._origin
    
    @origin.setter
    def origin(self, point):
        """
        Setter method that updates the origin.

        :type point: numpy.array
        :rtype: None
        """

        self._origin = numpy.copy(point)
        self.invalidate()
        
    @property
    def forwardAxis(self):
        """
        Getter method that returns the forward axis flag.

        :rtype: int
        """

        return self._forwardAxis

    @forwardAxis.setter
    def forwardAxis(self, forwardAxis):
        """
        Setter method that updates the forward axis flag.

        :type forwardAxis: int
        :rtype: None
        """

        if self._forwardAxis != forwardAxis and self._forwardAxis != self._upAxis:

            self._forwardAxis = forwardAxis

            self.forwardAxisButtonGroup.buttons()[forwardAxis].setChecked(True)
            self.invalidate()

    @property
    def forwardVector(self):
        """
        Getter method that returns the forward vector.

        :rtype: numpy.array
        """

        return self._forwardVector

    @forwardVector.setter
    def forwardVector(self, forwardVector):
        """
        Setter method that updates the forward vector.

        :type forwardVector: numpy.array
        :rtype: None
        """

        self._forwardVector = numpy.copy(forwardVector)
        self.invalidate()

    @property
    def upAxis(self):
        """
        Getter method that returns the up axis field value.

        :rtype: int
        """

        return self._upAxis

    @upAxis.setter
    def upAxis(self, upAxis):
        """
        Setter method used to update the forward axis flag.

        :type upAxis: int
        :rtype: None
        """

        if self._upAxis != upAxis and self._upAxis != self._forwardAxis:

            self._upAxis = upAxis

            self.upAxisButtonGroup.buttons()[upAxis].setChecked(True)
            self.invalidate()

    @property
    def upVector(self):
        """
        Getter method that returns the up vector.

        :rtype: numpy.array
        """

        return self._upVector

    @upVector.setter
    def upVector(self, upVector):
        """
        Setter method that updates the forward vector.

        :type upVector: numpy.array
        :rtype: None
        """

        self._upVector = numpy.copy(upVector)
        self.invalidate()
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        self.origin = json.loads(settings.value('tabs/matrix/origin', defaultValue='[0.0, 0.0, 0.0]', type=str))

        self.forwardAxis = settings.value('tabs/matrix/forwardAxis', defaultValue=0, type=int)
        self.forwardVector = json.loads(settings.value('tabs/matrix/forwardVector', defaultValue='[1.0, 0.0, 0.0]', type=str))

        self.upAxis = settings.value('tabs/matrix/upAxis', defaultValue=1, type=int)
        self.upVector = json.loads(settings.value('tabs/matrix/upVector', defaultValue='[0.0, 1.0, 0.0]', type=str))
        
    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        settings.setValue('tabs/matrix/origin', json.dumps(self.origin.tolist()))

        settings.setValue('tabs/matrix/forwardAxis', self.forwardAxis)
        settings.setValue('tabs/matrix/forwardVector', json.dumps(self.forwardVector.tolist()))

        settings.setValue('tabs/matrix/upAxis', self.upAxis)
        settings.setValue('tabs/matrix/upVector', json.dumps(self.upVector.tolist()))

    def remainingAxis(self):
        """
        Getter method that returns the unused axis.

        :rtype: int
        """

        return [x for x in [0, 1, 2] if x not in (self.forwardAxis, self.upAxis)][0]

    def invalidate(self):
        """
        Invalidates the transformation matrix.

        :rtype: None
        """

        # Compose aim matrix
        #
        log.debug('Origin: %s' % self.origin)
        log.debug('Forward Axis: %s, Forward Vector: %s' % (self.forwardAxis, self.forwardVector))
        log.debug('Up Axis: %s, Up Vector: %s' % (self.upAxis, self.upVector))

        matrix = matrixmath.createAimMatrix(
            self.forwardAxis, self.forwardVector,
            self.upAxis, self.upVector,
            origin=self.origin
        )

        # Update matrix widget
        #
        log.debug('Matrix = %s' % matrix)
        self.matrixEdit.setMatrix(matrix)

    @staticmethod
    def getAxisVector(node, axis=0):
        """
        Returns the axis vector from the supplied node.

        :type node: Any
        :type axis: int
        :rtype: numpy.matrix
        """

        fnTransform = fntransform.FnTransform(node)
        worldMatrix = fnTransform.worldMatrix()

        return matrixmath.breakMatrix(worldMatrix, normalize=True)[axis]

    @staticmethod
    def getCenterPosition():
        """
        Returns the center position of the active selection.
        Support for shapes is currently limited to meshes at this time.

        :rtype: numpy.array
        """

        # Evaluate active selection
        #
        fnNode = fnnode.FnNode()

        selection = fnNode.getActiveSelection()
        selectionCount = len(selection)

        center = numpy.array([0.0, 0.0, 0.0])

        if selectionCount == 0:

            log.warning('No transform nodes found in active selection!')
            return center

        # Iterate through selection
        #
        fnTransform = fntransform.FnTransform()
        fnMesh = fnmesh.FnMesh()

        weight = 1.0 / selectionCount

        for (index, obj) in enumerate(selection):

            # Check if selection contains a component
            #
            fnNode.setObject(obj)

            if fnNode.isMesh():

                fnMesh.setObject(obj)
                vertexIndices = fnMesh.selectedVertices()
                centerPoint = sum([numpy.array(x) for x in fnMesh.iterVertices(*vertexIndices)]) / len(vertexIndices)

                center += centerPoint * weight

            elif fnNode.isTransform():

                fnTransform.setObject(obj)
                translation = numpy.array(fnTransform.translation(worldSpace=True))

                center += translation * weight

            else:

                continue

        return center

    @staticmethod
    def getAveragedNormal():
        """
        Returns the averaged normal vector from the active selection.

        :rtype: numpy.array
        """

        # Evaluate active selection
        #
        fnMesh = fnmesh.FnMesh()

        selection = fnMesh.getActiveSelection()
        selectionCount = len(selection)

        normal = numpy.array([1.0, 0.0, 0.0])

        if selectionCount != 1:

            log.warning('No meshes found in active selection!')
            return normal

        # Iterate through component selection
        #
        success = fnMesh.trySetObject(selection[0])

        if success:

            vertexIndices = fnMesh.selectedVertices()
            normals = [numpy.array(x) for x in fnMesh.iterVertexNormals(*vertexIndices)]

            return vectormath.normalizeVector(sum(normals) / len(normals))

        else:

            return normal

    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Aligns the active selection to the user defined matrix.

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        # Get active selection
        #
        fnTransform = fntransform.FnTransform()

        selection = fnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 1:

            log.warning('apply() expects one selected node (%s given)!' % selectionCount)
            return

        # Get exclusive matrix
        #
        success = fnTransform.trySetObject(selection[0])

        if success:

            # Compose matrix in parent space
            #
            parentInverseMatrix = fnTransform.parentInverseMatrix()
            worldMatrix = self.matrixEdit.matrix()
            matrix = worldMatrix * parentInverseMatrix

            fnTransform.snapshot()
            fnTransform.setMatrix(matrix, preserveChildren=preserveChildren)

            # Check if transform should be frozen
            #
            if freezeTransform:

                fnTransform.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                fnTransform.assumeSnapshot()
    # endregion

    # region Slots
    def forwardAxisButtonGroup_idClicked(self, forwardAxis):
        """
        ID clicked slot method responsible for updating the forward axis flag.

        :type forwardAxis: int
        :rtype: None
        """

        # Make sure there's no axis conflict
        #
        if forwardAxis != self.upAxis:

            self._forwardAxis = forwardAxis

        else:

            self.sender().buttons()[self.forwardAxis].setChecked(True)

    def upAxisButtonGroup_idClicked(self, upAxis):
        """
        ID clicked slot method responsible for updating the up axis flag.

        :type upAxis: int
        :rtype: None
        """

        # Make sure there's no axis conflict
        #
        if upAxis != self.forwardAxis:

            self._upAxis = upAxis

        else:

            self.sender().buttons()[self.upAxis].setChecked(True)

    def originButton_clicked(self, *args, **kwargs):
        """
        Slot method called whenever the user clicks the position button.

        :rtype: None
        """

        self.origin = self.getCenterPosition()

    def forwardAxisButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for updating the forward vector.

        :type checked: bool
        :rtype: None
        """

        # Check if anything is selected
        #
        selection = fntransform.FnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount > 0:

            # Evaluate keyboard modifiers
            #
            modifiers = QtWidgets.QApplication.keyboardModifiers()

            if modifiers == QtCore.Qt.ControlModifier:

                self.forwardVector = self.getAxisVector(selection[0], axis=self.forwardAxis)

            elif modifiers == QtCore.Qt.AltModifier:

                self.forwardVector = self.getAveragedNormal()

            else:

                self.forwardVector = vectormath.normalizeVector(self.getCenterPosition() - self.origin)

        else:

            self.forwardVector = self.__axis__[self.forwardAxis]

    def upAxisButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for updating the up vector.

        :type checked: bool
        :rtype: None
        """

        # Check if anything is selected
        #
        selection = fntransform.FnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount:

            # Evaluate keyboard modifiers
            #
            modifiers = QtWidgets.QApplication.keyboardModifiers()

            if modifiers == QtCore.Qt.ControlModifier:

                self.upVector = self.getAxisVector(selection[0], axis=self.upAxis)

            elif modifiers == QtCore.Qt.AltModifier:

                self.upVector = self.getAveragedNormal()

            else:

                self.upVector = vectormath.normalizeVector(self.getCenterPosition() - self.origin)

        else:

            self.upVector = self.__axis__[self.upAxis]
    # endregion

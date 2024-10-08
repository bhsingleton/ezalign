import json

from Qt import QtCore, QtWidgets, QtGui
from dcc import fnnode, fntransform, fnmesh
from dcc.dataclasses import vector, boundingbox, transformationmatrix
from dcc.ui import qmatrixedit
from . import qabstracttab

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
    __axis__ = vector.Vector.xAxis, vector.Vector.yAxis, vector.Vector.zAxis

    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :key parent: QtWidgets.QWidget
        :key f: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QMatrixTab, self).__init__(*args, **kwargs)

        # Declare private variables
        #
        self._origin = vector.Vector.zero
        self._forwardAxis = -1
        self._forwardVector = vector.Vector.xAxis
        self._upAxis = -1
        self._upVector = vector.Vector.yAxis

    def __setup_ui__(self, *args, **kwargs):
        """
        Private method that initializes the user interface.

        :rtype: None
        """

        # Initialize widget
        #
        self.setWhatsThis('Select the node to paste the transformation matrix onto.')

        # Initialize central layout
        #
        centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(centralLayout)

        # Declare public variables
        #
        self.matrixLayout = QtWidgets.QVBoxLayout()
        self.matrixLayout.setObjectName('matrixLayout')

        self.matrixGroupBox = QtWidgets.QGroupBox('4x4 Matrix:')
        self.matrixGroupBox.setObjectName('matrixGroupBox')
        self.matrixGroupBox.setLayout(self.matrixLayout)
        self.matrixGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.matrixGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.originPushButton = QtWidgets.QPushButton('Origin')
        self.originPushButton.setObjectName('originPushButton')
        self.originPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.originPushButton.setFixedHeight(24)
        self.originPushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.originPushButton.setToolTip('Averages the position of the selected nodes or mesh components.')
        self.originPushButton.clicked.connect(self.on_originPushButton_clicked)

        self.matrixEdit = qmatrixedit.QMatrixEdit()
        self.matrixEdit.setObjectName('matrixEdit')
        self.matrixEdit.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.matrixEdit.setRowLabels(['X-Axis:', 'Y-Axis:', 'Z-Axis:', 'Origin:'])
        self.matrixEdit.replaceLabel(3, self.originPushButton)

        self.matrixLayout.addWidget(self.matrixEdit)

        centralLayout.addWidget(self.matrixGroupBox)

        # Initialize forward-axis group-box
        #
        self.forwardAxisLayout = QtWidgets.QHBoxLayout()
        self.forwardAxisLayout.setObjectName('forwardAxisLayout')
        
        self.forwardAxisGroupBox = QtWidgets.QGroupBox('Forward Axis:')
        self.forwardAxisGroupBox.setObjectName('forwardAxisGroupBox')
        self.forwardAxisGroupBox.setLayout(self.forwardAxisLayout)
        self.forwardAxisGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.forwardAxisGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.forwardAxisPushButton = QtWidgets.QPushButton('Pick')
        self.forwardAxisPushButton.setObjectName('forwardAxisPushButton')
        self.forwardAxisPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.forwardAxisPushButton.setFixedHeight(24)
        self.forwardAxisPushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.forwardAxisPushButton.setToolTip('Calculates the forward vector from the active selection relative to the origin.')
        self.forwardAxisPushButton.clicked.connect(self.on_forwardAxisPushButton_clicked)

        self.forwardXRadioButton = QtWidgets.QRadioButton('X')
        self.forwardXRadioButton.setObjectName('forwardXRadioButton')
        self.forwardXRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardXRadioButton.setFixedHeight(24)
        self.forwardXRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.forwardYRadioButton = QtWidgets.QRadioButton('Y')
        self.forwardYRadioButton.setObjectName('forwardYRadioButton')
        self.forwardYRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardYRadioButton.setFixedHeight(24)
        self.forwardYRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.forwardZRadioButton = QtWidgets.QRadioButton('Z')
        self.forwardZRadioButton.setObjectName('forwardZRadioButton')
        self.forwardZRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardZRadioButton.setFixedHeight(24)
        self.forwardZRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.forwardAxisButtonGroup = QtWidgets.QButtonGroup(self.forwardAxisGroupBox)
        self.forwardAxisButtonGroup.setObjectName('forwardAxisButtonGroup')
        self.forwardAxisButtonGroup.setExclusive(True)
        self.forwardAxisButtonGroup.addButton(self.forwardXRadioButton, id=0)
        self.forwardAxisButtonGroup.addButton(self.forwardYRadioButton, id=1)
        self.forwardAxisButtonGroup.addButton(self.forwardZRadioButton, id=2)
        self.forwardAxisButtonGroup.idClicked.connect(self.on_forwardAxisButtonGroup_idClicked)

        self.forwardAxisLayout.addWidget(self.forwardAxisPushButton)
        self.forwardAxisLayout.addWidget(self.forwardXRadioButton, alignment=QtCore.Qt.AlignCenter)
        self.forwardAxisLayout.addWidget(self.forwardYRadioButton, alignment=QtCore.Qt.AlignCenter)
        self.forwardAxisLayout.addWidget(self.forwardZRadioButton, alignment=QtCore.Qt.AlignCenter)
        
        centralLayout.addWidget(self.forwardAxisGroupBox)

        # Initialize up-axis group-box
        #
        self.upAxisLayout = QtWidgets.QHBoxLayout()
        self.upAxisLayout.setObjectName('upAxisLayout')

        self.upAxisGroupBox = QtWidgets.QGroupBox('Up Axis:')
        self.upAxisGroupBox.setObjectName('upAxisGroupBox')
        self.upAxisGroupBox.setLayout(self.upAxisLayout)
        self.upAxisGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.upAxisGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.upAxisPushButton = QtWidgets.QPushButton('Pick')
        self.upAxisPushButton.setObjectName('upAxisPushButton')
        self.upAxisPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.upAxisPushButton.setFixedHeight(24)
        self.upAxisPushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.upAxisPushButton.setToolTip('Calculates the up vector from the active selection relative to the origin.')
        self.upAxisPushButton.clicked.connect(self.on_upAxisPushButton_clicked)

        self.upXRadioButton = QtWidgets.QRadioButton('X')
        self.upXRadioButton.setObjectName('upXRadioButton')
        self.upXRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upXRadioButton.setFixedHeight(24)
        self.upXRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.upYRadioButton = QtWidgets.QRadioButton('Y')
        self.upYRadioButton.setObjectName('upYRadioButton')
        self.upYRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upYRadioButton.setFixedHeight(24)
        self.upYRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.upZRadioButton = QtWidgets.QRadioButton('Z')
        self.upZRadioButton.setObjectName('upZRadioButton')
        self.upZRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upZRadioButton.setFixedHeight(24)
        self.upZRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.upAxisButtonGroup = QtWidgets.QButtonGroup(self.upAxisGroupBox)
        self.upAxisButtonGroup.setObjectName('upAxisButtonGroup')
        self.upAxisButtonGroup.setExclusive(True)
        self.upAxisButtonGroup.addButton(self.upXRadioButton, id=0)
        self.upAxisButtonGroup.addButton(self.upYRadioButton, id=1)
        self.upAxisButtonGroup.addButton(self.upZRadioButton, id=2)
        self.upAxisButtonGroup.idClicked.connect(self.on_upAxisButtonGroup_idClicked)

        self.upAxisLayout.addWidget(self.upAxisPushButton)
        self.upAxisLayout.addWidget(self.upXRadioButton, alignment=QtCore.Qt.AlignCenter)
        self.upAxisLayout.addWidget(self.upYRadioButton, alignment=QtCore.Qt.AlignCenter)
        self.upAxisLayout.addWidget(self.upZRadioButton, alignment=QtCore.Qt.AlignCenter)

        centralLayout.addWidget(self.upAxisGroupBox)
    # endregion

    # region Properties
    @property
    def origin(self):
        """
        Getter method that returns the origin.

        :rtype: vector.Vector
        """

        return self._origin
    
    @origin.setter
    def origin(self, point):
        """
        Setter method that updates the origin.

        :type point: vector.Vector
        :rtype: None
        """
        
        if isinstance(point, (list, tuple, vector.Vector)):

            self._origin = vector.Vector(*point)
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

        isDifferent = forwardAxis != self._forwardAxis
        isValid = forwardAxis != self._upAxis

        if (isDifferent and isValid) and isinstance(forwardAxis, int):

            self._forwardAxis = forwardAxis

            self.forwardAxisButtonGroup.buttons()[forwardAxis].setChecked(True)
            self.invalidate()

    @property
    def forwardVector(self):
        """
        Getter method that returns the forward vector.

        :rtype: vector.Vector
        """

        return self._forwardVector

    @forwardVector.setter
    def forwardVector(self, forwardVector):
        """
        Setter method that updates the forward vector.

        :type forwardVector: vector.Vector
        :rtype: None
        """

        if isinstance(forwardVector, (list, tuple, vector.Vector)):

            self._forwardVector = vector.Vector(*forwardVector)
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

        isDifferent = upAxis != self._upAxis
        isValid = upAxis != self._forwardAxis

        if (isDifferent and isValid) and isinstance(upAxis, int):

            self._upAxis = upAxis

            self.upAxisButtonGroup.buttons()[upAxis].setChecked(True)
            self.invalidate()

    @property
    def upVector(self):
        """
        Getter method that returns the up vector.

        :rtype: vector.Vector
        """

        return self._upVector

    @upVector.setter
    def upVector(self, upVector):
        """
        Setter method that updates the forward vector.

        :type upVector: vector.Vector
        :rtype: None
        """

        if isinstance(upVector, (list, tuple, vector.Vector)):

            self._upVector = vector.Vector(*upVector)
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

        settings.setValue('tabs/matrix/origin', json.dumps(self.origin.toList()))

        settings.setValue('tabs/matrix/forwardAxis', self.forwardAxis)
        settings.setValue('tabs/matrix/forwardVector', json.dumps(self.forwardVector.toList()))

        settings.setValue('tabs/matrix/upAxis', self.upAxis)
        settings.setValue('tabs/matrix/upVector', json.dumps(self.upVector.toList()))

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

        # Redundancy check
        #
        if not ((0 <= self.forwardAxis < 3) and (0 <= self.upAxis < 3) and self.forwardAxis != self.upAxis):

            return

        # Compose aim matrix
        #
        log.debug(f'Origin: {self.origin}')
        log.debug(f'Forward Axis: {self.forwardAxis}, Forward Vector: {self.forwardVector}')
        log.debug(f'Up Axis: {self.upAxis}, Up Vector: {self.upVector}')

        matrix = transformationmatrix.TransformationMatrix(row4=self.origin)
        matrix.lookAt(forwardVector=self.forwardVector, forwardAxis=self.forwardAxis, upVector=self.upVector, upAxis=self.upAxis)

        # Update matrix widget
        #
        log.debug(f'Matrix = {matrix}')
        self.matrixEdit.setMatrix(matrix)

    @staticmethod
    def getAxisVector(node, axis=0):
        """
        Returns the axis vector from the supplied node.

        :type node: Any
        :type axis: int
        :rtype: transformationmatrix.TransformationMatrix
        """

        fnTransform = fntransform.FnTransform(node)
        worldMatrix = fnTransform.worldMatrix()
        row = worldMatrix[axis]

        return vector.Vector(row[0], row[1], row[2]).normalize()

    def getCenterPosition(self):
        """
        Returns the center position of the active selection.
        Support for shapes is currently limited to meshes at this time.

        :rtype: vector.Vector
        """

        # Evaluate active selection
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount == 0:

            log.warning('No transform nodes found in active selection!')
            return vector.Vector.zero

        # Iterate through selection and expand bounding box
        #
        node = fnnode.FnNode()
        transform = fntransform.FnTransform()
        mesh = fnmesh.FnMesh()

        boundingBox = boundingbox.BoundingBox()

        for (index, obj) in enumerate(selection):

            # Check if selection contains a component
            #
            node.setObject(obj)

            if node.isMesh():

                mesh.setObject(obj)
                vertexIndices = mesh.selectedVertices()
                vertexPoints = mesh.getVertices(*vertexIndices, worldSpace=True)

                boundingBox.expand(*vertexPoints)

            elif node.isTransform():

                transform.setObject(obj)
                translation = transform.translation(worldSpace=True)

                boundingBox.expand(translation)

            else:

                continue

        # Return bounding box center
        #
        return boundingBox.center()

    def getAveragedNormal(self):
        """
        Returns the averaged normal vector from the active selection.

        :rtype: numpy.array
        """

        # Evaluate active selection
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        normal = vector.Vector(1.0, 0.0, 0.0)

        if selectionCount != 1:

            log.warning('No meshes found in active selection!')
            return normal

        # Iterate through component selection
        #
        fnMesh = fnmesh.FnMesh()
        success = fnMesh.trySetObject(selection[0])

        if success:

            vertexIndices = fnMesh.selectedVertices()
            normals = list(fnMesh.iterVertexNormals(*vertexIndices))

            return (sum(normals) / len(normals)).normalize()

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
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 1:

            log.warning('apply() expects one selected node (%s given)!' % selectionCount)
            return

        # Get exclusive matrix
        #
        node = fntransform.FnTransform()
        success = node.trySetObject(selection[0])

        if success:

            # Compose matrix in parent space
            #
            parentInverseMatrix = node.parentInverseMatrix()
            worldMatrix = self.matrixEdit.matrix()
            matrix = worldMatrix * parentInverseMatrix

            node.snapshot()
            node.setMatrix(matrix, skipScale=True, preserveChildren=preserveChildren)

            # Check if transform should be frozen
            #
            if freezeTransform:

                node.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                node.assumeSnapshot()
    # endregion

    # region Slots
    @QtCore.Slot(int)
    def on_forwardAxisButtonGroup_idClicked(self, forwardAxis):
        """
        Slot method for the forwardAxisButtonGroup's `idClicked` signal.
        This method updates the current forward axis.

        :type forwardAxis: int
        :rtype: None
        """

        # Make sure there's no axis conflict
        #
        if forwardAxis != self.upAxis:

            self._forwardAxis = forwardAxis
            self.invalidate()

        else:

            self.sender().buttons()[self.forwardAxis].setChecked(True)

    @QtCore.Slot(int)
    def on_upAxisButtonGroup_idClicked(self, upAxis):
        """
        Slot method for the upAxisButtonGroup's `idClicked` signal.
        This method updates the current up axis.

        :type upAxis: int
        :rtype: None
        """

        # Make sure there's no axis conflict
        #
        if upAxis != self.forwardAxis:

            self._upAxis = upAxis
            self.invalidate()

        else:

            self.sender().buttons()[self.upAxis].setChecked(True)

    @QtCore.Slot(bool)
    def on_originPushButton_clicked(self, checked=False):
        """
        Slot method for the originPushButton's `clicked` signal.
        This method updates the current point of origin.

        :type checked: bool
        :rtype: None
        """

        self.origin = self.getCenterPosition()

    @QtCore.Slot(bool)
    def on_forwardAxisPushButton_clicked(self, checked=False):
        """
        Slot method for the forwardAxisPushButton's `clicked` signal.
        This method updates the internal forward vector.

        :type checked: bool
        :rtype: None
        """

        # Check if anything is selected
        #
        selection = self.scene.getActiveSelection()
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

                self.forwardVector = (self.getCenterPosition() - self.origin).normalize()

        else:

            self.forwardVector = self.__axis__[self.forwardAxis]

    @QtCore.Slot(bool)
    def on_upAxisPushButton_clicked(self, checked=False):
        """
        Slot method for the upAxisPushButton's `clicked` signal.
        This method updates the internal up vector.

        :type checked: bool
        :rtype: None
        """

        # Check if anything is selected
        #
        selection = self.scene.getActiveSelection()
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

                self.upVector = (self.getCenterPosition() - self.origin).normalize()

        else:

            self.upVector = self.__axis__[self.upAxis]
    # endregion

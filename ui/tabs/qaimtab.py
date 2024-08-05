import json

from Qt import QtCore, QtWidgets, QtGui
from dcc import fntransform
from dcc.dataclasses import vector, transformationmatrix
from dcc.ui import qvectoredit
from . import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAimTab(qabstracttab.QAbstractTab):
    """
    Overload of `QAbstractTab` that implements aim transform logic.
    """

    # region Dunderscores
    __sign__ = (1.0, -1.0)
    __decimals__ = 3
    __origin__ = vector.Vector.zero
    __axes__ = 'xyz'
    __axis_vectors__ = vector.Vector.xAxis, vector.Vector.yAxis, vector.Vector.zAxis

    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :key parent: QtWidgets.QWidget
        :key f: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QAimTab, self).__init__(*args, **kwargs)

        # Declare private variables
        #
        self._forwardAxis = -1
        self._upAxis = -1
        self._worldUpObject = fntransform.FnTransform()

    def __setup_ui__(self, *args, **kwargs):
        """
        Private method that initializes the user interface.

        :rtype: None
        """

        # Initialize central layout
        #
        centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(centralLayout)

        # Initialize forward-axis group-box
        #
        self.forwardAxisLayout = QtWidgets.QHBoxLayout()
        self.forwardAxisLayout.setObjectName('forwardAxisLayout')
        
        self.forwardAxisGroupBox = QtWidgets.QGroupBox('Forward Axis:')
        self.forwardAxisGroupBox.setObjectName('forwardAxisGroupBox')
        self.forwardAxisGroupBox.setLayout(self.forwardAxisLayout)
        self.forwardAxisGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.forwardXRadioButton = QtWidgets.QRadioButton('X')
        self.forwardXRadioButton.setObjectName('forwardXRadioButton')
        self.forwardXRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardXRadioButton.setFixedHeight(24)
        
        self.forwardYRadioButton = QtWidgets.QRadioButton('Y')
        self.forwardYRadioButton.setObjectName('forwardYRadioButton')
        self.forwardYRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardYRadioButton.setFixedHeight(24)
        
        self.forwardZRadioButton = QtWidgets.QRadioButton('Z')
        self.forwardZRadioButton.setObjectName('forwardZRadioButton')
        self.forwardZRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardZRadioButton.setFixedHeight(24)
        
        self.forwardAxisSignComboBox = QtWidgets.QComboBox()
        self.forwardAxisSignComboBox.setObjectName('forwardAxisSignComboBox')
        self.forwardAxisSignComboBox.addItems(['+', '-'])
        self.forwardAxisSignComboBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.forwardAxisSignComboBox.setFixedHeight(24)

        self.forwardAxisButtonGroup = QtWidgets.QButtonGroup(self.forwardAxisGroupBox)
        self.forwardAxisButtonGroup.setObjectName('forwardAxisButtonGroup')
        self.forwardAxisButtonGroup.setExclusive(True)
        self.forwardAxisButtonGroup.addButton(self.forwardXRadioButton, id=0)
        self.forwardAxisButtonGroup.addButton(self.forwardYRadioButton, id=1)
        self.forwardAxisButtonGroup.addButton(self.forwardZRadioButton, id=2)
        self.forwardAxisButtonGroup.idClicked.connect(self.on_forwardAxisButtonGroup_idClicked)

        self.forwardAxisLayout.addWidget(self.forwardXRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardYRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardZRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardAxisSignComboBox)

        centralLayout.addWidget(self.forwardAxisGroupBox)

        # Initialize up-axis group-box
        #
        self.upAxisLayout = QtWidgets.QHBoxLayout()
        self.upAxisLayout.setObjectName('upAxisLayout')

        self.upAxisGroupBox = QtWidgets.QGroupBox('Up Axis:')
        self.upAxisGroupBox.setObjectName('upAxisGroupBox')
        self.upAxisGroupBox.setLayout(self.upAxisLayout)
        self.upAxisGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.upXRadioButton = QtWidgets.QRadioButton('X')
        self.upXRadioButton.setObjectName('upXRadioButton')
        self.upXRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upXRadioButton.setFixedHeight(24)

        self.upYRadioButton = QtWidgets.QRadioButton('Y')
        self.upYRadioButton.setObjectName('upYRadioButton')
        self.upYRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upYRadioButton.setFixedHeight(24)

        self.upZRadioButton = QtWidgets.QRadioButton('Z')
        self.upZRadioButton.setObjectName('upZRadioButton')
        self.upZRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upZRadioButton.setFixedHeight(24)

        self.upAxisSignComboBox = QtWidgets.QComboBox()
        self.upAxisSignComboBox.setObjectName('upAxisSignComboBox')
        self.upAxisSignComboBox.addItems(['+', '-'])
        self.upAxisSignComboBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.upAxisSignComboBox.setFixedHeight(24)

        self.upAxisButtonGroup = QtWidgets.QButtonGroup(self.upAxisGroupBox)
        self.upAxisButtonGroup.setObjectName('upAxisButtonGroup')
        self.upAxisButtonGroup.setExclusive(True)
        self.upAxisButtonGroup.addButton(self.upXRadioButton, id=0)
        self.upAxisButtonGroup.addButton(self.upYRadioButton, id=1)
        self.upAxisButtonGroup.addButton(self.upZRadioButton, id=2)
        self.upAxisButtonGroup.idClicked.connect(self.on_upAxisButtonGroup_idClicked)

        self.upAxisLayout.addWidget(self.upXRadioButton)
        self.upAxisLayout.addWidget(self.upYRadioButton)
        self.upAxisLayout.addWidget(self.upZRadioButton)
        self.upAxisLayout.addWidget(self.upAxisSignComboBox)

        centralLayout.addWidget(self.upAxisGroupBox)

        # Initialize world-up type widget
        #
        self.worldUpTypeLayout = QtWidgets.QHBoxLayout()
        self.worldUpTypeLayout.setObjectName('worldUpTypeLayout')
        self.worldUpTypeLayout.setContentsMargins(0, 0, 0, 0)

        self.worldUpTypeWidget = QtWidgets.QWidget()
        self.worldUpTypeWidget.setObjectName('worldUpTypeWidget')
        self.worldUpTypeWidget.setLayout(self.worldUpTypeLayout)
        self.worldUpTypeWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.worldUpTypeWidget.setFixedHeight(24)

        self.worldUpTypeLabel = QtWidgets.QLabel('Type:')
        self.worldUpTypeLabel.setObjectName('worldUpTypeLabel')
        self.worldUpTypeLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.worldUpTypeLabel.setFixedWidth(40)
        self.worldUpTypeLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.worldUpTypeComboBox = QtWidgets.QComboBox()
        self.worldUpTypeComboBox.setObjectName('worldUpTypeComboBox')
        self.worldUpTypeComboBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))
        self.worldUpTypeComboBox.addItems(['Scene Up', 'Object Up', 'Object Rotation Up', 'Vector'])
        self.worldUpTypeComboBox.setItemData(0, 'Copies the up-vector from the scene-up axis.', role=QtCore.Qt.ToolTipRole)
        self.worldUpTypeComboBox.setItemData(1, 'Calculates the up-vector from the forward vector between the origin and world-up object.', role=QtCore.Qt.ToolTipRole)
        self.worldUpTypeComboBox.setItemData(2, "Copies the up-vector from the world-up object's axis vectors.", role=QtCore.Qt.ToolTipRole)
        self.worldUpTypeComboBox.setItemData(3, 'Copies the up-vector from the custom vector widget.', role=QtCore.Qt.ToolTipRole)

        self.worldUpTypeLayout.addWidget(self.worldUpTypeLabel)
        self.worldUpTypeLayout.addWidget(self.worldUpTypeComboBox)

        # Initialize world-up vector widget
        #
        self.worldUpVectorLayout = QtWidgets.QHBoxLayout()
        self.worldUpVectorLayout.setObjectName('worldUpVectorLayout')
        self.worldUpVectorLayout.setContentsMargins(0, 0, 0, 0)

        self.worldUpVectorWidget = QtWidgets.QWidget()
        self.worldUpVectorWidget.setObjectName('worldUpVectorWidget')
        self.worldUpVectorWidget.setLayout(self.worldUpVectorLayout)
        self.worldUpVectorWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.worldUpVectorWidget.setFixedHeight(24)

        self.worldUpVectorLabel = QtWidgets.QLabel('Vector:')
        self.worldUpVectorLabel.setObjectName('worldUpVectorLabel')
        self.worldUpVectorLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.worldUpVectorLabel.setFixedWidth(40)
        self.worldUpVectorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.worldUpVectorEdit = qvectoredit.QVectorEdit()
        self.worldUpVectorEdit.setObjectName('worldUpVectorEdit')
        self.worldUpVectorEdit.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))

        self.worldUpVectorPushButton = QtWidgets.QPushButton('Pick')
        self.worldUpVectorPushButton.setObjectName('worldUpVectorPushButton')
        self.worldUpVectorPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.worldUpVectorPushButton.setFixedWidth(60)
        self.worldUpVectorPushButton.clicked.connect(self.on_worldUpVectorPushButton_clicked)

        self.worldUpVectorLayout.addWidget(self.worldUpVectorLabel)
        self.worldUpVectorLayout.addWidget(self.worldUpVectorEdit)
        self.worldUpVectorLayout.addWidget(self.worldUpVectorPushButton)

        # Initialize world-up object widget
        #
        self.worldUpObjectLayout = QtWidgets.QHBoxLayout()
        self.worldUpObjectLayout.setObjectName('worldUpObjectLayout')
        self.worldUpObjectLayout.setContentsMargins(0, 0, 0, 0)

        self.worldUpObjectWidget = QtWidgets.QWidget()
        self.worldUpObjectWidget.setObjectName('worldUpObjectWidget')
        self.worldUpObjectWidget.setLayout(self.worldUpObjectLayout)
        self.worldUpObjectWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.worldUpObjectWidget.setFixedHeight(24)

        self.worldUpObjectLabel = QtWidgets.QLabel('Object:')
        self.worldUpObjectLabel.setObjectName('worldUpObjectLabel')
        self.worldUpObjectLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.worldUpObjectLabel.setFixedWidth(40)
        self.worldUpObjectLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.worldUpObjectLineEdit = QtWidgets.QLineEdit('')
        self.worldUpObjectLineEdit.setObjectName('worldUpObjectLineEdit')
        self.worldUpObjectLineEdit.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred))
        self.worldUpObjectLineEdit.setReadOnly(True)
        self.worldUpObjectLineEdit.setPlaceholderText('World Up Object Name')
        self.worldUpObjectLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.worldUpObjectPushButton = QtWidgets.QPushButton('Pick')
        self.worldUpObjectPushButton.setObjectName('worldUpObjectPushButton')
        self.worldUpObjectPushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.worldUpObjectPushButton.setFixedWidth(60)
        self.worldUpObjectPushButton.clicked.connect(self.on_worldUpObjectPushButton_clicked)

        self.worldUpObjectLayout.addWidget(self.worldUpObjectLabel)
        self.worldUpObjectLayout.addWidget(self.worldUpObjectLineEdit)
        self.worldUpObjectLayout.addWidget(self.worldUpObjectPushButton)

        # Initialize world-up group-box
        #
        self.worldUpLayout = QtWidgets.QVBoxLayout()
        self.worldUpLayout.setObjectName('worldUpLayout')

        self.worldUpGroupBox = QtWidgets.QGroupBox('World Up:')
        self.worldUpGroupBox.setObjectName('worldUpGroupBox')
        self.worldUpGroupBox.setLayout(self.worldUpLayout)
        self.worldUpGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.worldUpLayout.addWidget(self.worldUpTypeWidget)
        self.worldUpLayout.addWidget(self.worldUpVectorWidget)
        self.worldUpLayout.addWidget(self.worldUpObjectWidget)

        centralLayout.addWidget(self.worldUpGroupBox)
    # endregion

    # region Properties
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
        Setter method used to update the forward axis flag.

        :type forwardAxis: int
        :rtype: None
        """

        isDifferent = forwardAxis != self._forwardAxis
        isValid = forwardAxis != self._upAxis

        if (isDifferent and isValid) and isinstance(forwardAxis, int):

            self._forwardAxis = forwardAxis
            self.forwardAxisButtonGroup.buttons()[forwardAxis].setChecked(True)

    @property
    def forwardAxisSign(self):
        """
        Getter method that returns the forward axis sign.

        :rtype: float
        """

        return self.__sign__[self.forwardAxisSignComboBox.currentIndex()]

    @forwardAxisSign.setter
    def forwardAxisSign(self, forwardAxisSign):
        """
        Setter method that updates the forward axis sign.

        :type forwardAxisSign: float
        :rtype: None
        """

        if isinstance(forwardAxisSign, float):

            self.forwardAxisSignComboBox.setCurrentIndex(self.__sign__.index(forwardAxisSign))

    @property
    def upAxis(self):
        """
        Getter method that returns the up axis flag.

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

    @property
    def upAxisSign(self):
        """
        Getter method that returns the up axis sign.

        :rtype: float
        """

        return self.__sign__[self.upAxisSignComboBox.currentIndex()]

    @upAxisSign.setter
    def upAxisSign(self, upAxisSign):
        """
        Setter method that updates the forward axis sign.

        :type upAxisSign: float
        :rtype: None
        """

        if isinstance(upAxisSign, float):

            self.upAxisSignComboBox.setCurrentIndex(self.__sign__.index(upAxisSign))

    @property
    def worldUpType(self):
        """
        Getter method that returns the world up type.

        :rtype: int
        """

        return self.worldUpTypeComboBox.currentIndex()

    @worldUpType.setter
    def worldUpType(self, worldUpType):
        """
        Setter method that updates the world up type.

        :type worldUpType: int
        :rtype: None
        """

        if isinstance(worldUpType, int):

            self.worldUpTypeComboBox.setCurrentIndex(worldUpType)

    @property
    def worldUpVector(self):
        """
        Getter method that returns the world up vector.

        :rtype: vector.Vector
        """

        return self.worldUpVectorEdit.vector()

    @worldUpVector.setter
    def worldUpVector(self, worldUpVector):
        """
        Setter method that updates the world up vector.

        :type worldUpVector: vector.Vector
        :rtype: None
        """

        if isinstance(worldUpVector, (list, tuple, vector.Vector)):

            self.worldUpVectorEdit.setVector(worldUpVector)

    @property
    def worldUpObject(self):
        """
        Getter method that returns the world up object.

        :rtype: fntransform.FnTransform
        """

        return self._worldUpObject
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        self.forwardAxis = settings.value('tabs/aim/forwardAxis', defaultValue=0, type=int)
        self.forwardAxisSign = settings.value('tabs/aim/forwardAxisSign', defaultValue=1.0, type=float)

        self.upAxis = settings.value('tabs/aim/upAxis', defaultValue=1, type=int)
        self.upAxisSign = settings.value('tabs/aim/upAxisSign', defaultValue=1.0, type=float)

        self.worldUpType = settings.value('tabs/aim/worldUpType', defaultValue=0, type=int)
        self.worldUpVector = json.loads(settings.value('tabs/aim/worldUpVector', defaultValue='[0.0, 0.0, 1.0]', type=str))

    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        settings.setValue('tabs/aim/forwardAxis', self.forwardAxis)
        settings.setValue('tabs/aim/forwardAxisSign', self.forwardAxisSign)

        settings.setValue('tabs/aim/upAxis', self.upAxis)
        settings.setValue('tabs/aim/upAxisSign', self.upAxisSign)

        settings.setValue('tabs/aim/worldUpType', self.worldUpType)
        settings.setValue('tabs/aim/worldUpVector', json.dumps(self.worldUpVector.toList()))

    def forwardVector(self, start, end, normalize=False):
        """
        Returns the forward vector between two nodes.

        :type start: Any
        :type end: Any
        :type normalize: bool
        :rtype: vector.Vector
        """

        # Get forward vector between nodes
        #
        startNode = fntransform.FnTransform(start)
        endNode = fntransform.FnTransform(end)

        startPoint = startNode.translation(worldSpace=True)
        endPoint = endNode.translation(worldSpace=True)
        forwardVector = endPoint - startPoint

        # Check if vector should be normalized
        #
        if normalize:

            return forwardVector.normalize()

        else:

            return forwardVector

    def upVector(self, start, end, normalize=False):
        """
        Returns the up vector based on the selected world up settings.

        :type start: Any
        :type end: Any
        :type normalize: bool
        :rtype: vector.Vector
        """

        # Inspect world up type
        #
        if self.worldUpType == 0:  # Scene

            return self.sceneUpVector()

        elif self.worldUpType == 1:  # Object

            return self.worldUpObjectVector(start)

        elif self.worldUpType == 2:  # Object Rotation Up

            return self.worldUpObjectRotationVector()

        elif self.worldUpType == 3:  # Vector

            return self.worldUpVector.normal()

        else:

            raise RuntimeError('upVector() expects a valid world up type (%s given)!' % self.worldUpType)

    def perpendicularVector(self, nodes):
        """
        Returns the perpendicular vector from the supplied nodes.
        This function is intended to be used with limbs in order to derive a pole vector.

        :type nodes: List[Any]
        :rtype: vector.Vector
        """

        # Verify there are enough nodes
        #
        numNodes = len(nodes)

        if not numNodes >= 3:

            log.warning('perpendicularVector() expects at least 3 nodes (%s given)!' % numNodes)
            return

        # Iterate through nodes
        #
        startNode = fntransform.FnTransform(nodes[0])
        endNode = fntransform.FnTransform()

        origin = startNode.translation(worldSpace=True)
        vectors = []

        for i in range(1, numNodes, 2):

            startNode.setObject(nodes[i])
            endNode.setObject(nodes[i + 1])

            startPoint = startNode.translation(worldSpace=True)
            endPoint = endNode.translation(worldSpace=True)

            cross = (startPoint - origin).normalize() ^ (endPoint - origin).normalize()
            vectors.append(cross)

        return self.averageVectors(vectors, normalize=True)

    def axisVector(self, node, axis):
        """
        Returns the axis vector from the supplied node.

        :type node: Any
        :type axis: int
        :rtype: vector.Vector
        """

        worldMatrix = fntransform.FnTransform(node).worldMatrix()
        rows = worldMatrix.decompose(normalize=True)

        return rows[axis]

    def averageVectors(self, vectors, normalize=False):
        """
        Returns the averaged vector from a list of vectors.

        :type vectors: List[vector.Vector]
        :type normalize: bool
        :rtype: vector.Vector
        """

        vec = sum(vectors) / len(vectors)

        if normalize:

            vec.normalize()

        return vec

    def remainingAxis(self):
        """
        Getter method used to return the unused axis.

        :rtype: int
        """

        return [x for x in [0, 1, 2] if x not in (self.forwardAxis, self.upAxis)][0]

    def sceneUpVector(self):
        """
        Returns the current scene up vector.

        :rtype: vector.Vector
        """

        upAxis = self.scene.getUpAxis()
        index = self.__axes__.index(upAxis.lower())

        return self.__axis_vectors__[index].copy()

    def worldUpObjectVector(self, start, normalize=False):
        """
        Returns the world up object vector.

        :type start: Any
        :type normalize: bool
        :rtype: vector.Vector
        """

        # Check if world up object is valid
        #
        worldUpObjectVector = self.worldUpVector.copy()

        if self.worldUpObject.isValid():

            startNode = fntransform.FnTransform(start)
            startPoint = startNode.translation(worldSpace=True)
            endPoint = self.worldUpObject.translation(worldSpace=True)

            worldUpObjectVector = (endPoint - startPoint)

        else:

            log.warning('Unable to locate world up object!')

        # Check if vector should be normalized
        #
        if normalize:

            return worldUpObjectVector.normalize()

        else:

            return worldUpObjectVector

    def worldUpObjectRotationVector(self):
        """
        Returns the world up rotation vector from the world up object.
        If the world up object is invalid then the world up vector is returned instead.

        :rtype: vector.Vector
        """

        if self.worldUpObject.isValid():

            worldMatrix = self.worldUpObjectMatrix()
            xAxis, yAxis, zAxis, position = worldMatrix.decompose(normalize=True)

            return ((xAxis * self.worldUpVector.x) + (yAxis * self.worldUpVector.y) + (zAxis * self.worldUpVector.z)).normalize()

        else:

            return self.worldUpVector.normal()

    def worldUpObjectMatrix(self):
        """
        Returns the world up matrix from the world up object.
        If the world up object is invalid then an identity matrix is returned instead.

        :rtype: transformationmatrix.TransformationMatrix
        """

        # Check if world up object is alive
        #
        if self.worldUpObject.isValid():

            return self.worldUpObject.worldMatrix()

        else:

            return transformationmatrix.TransformationMatrix()

    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Aims the active selection to each subsequent node in the selection.
        By default, this operation will always preserve children!

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        # Get active selection
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if not selectionCount >= 2:

            log.warning('apply() expects at least two selected node (%s given)!' % selectionCount)
            return

        # Iterate through selection
        #
        startNode = fntransform.FnTransform()

        for i in range(selectionCount - 1):  # Make sure to skip the last item!

            # Get dag paths to nodes
            #
            start, end = selection[i], selection[i+1]
            startNode.setObject(start)

            origin = startNode.translation(worldSpace=True)
            forwardVector = self.forwardVector(start, end, normalize=True)
            upVector = self.upVector(start, end, normalize=True)

            # Compose aim matrix in parent space
            #
            matrix = transformationmatrix.TransformationMatrix(row4=origin)
            matrix.lookAt(
                forwardVector=forwardVector, forwardAxis=self.forwardAxis, forwardAxisSign=self.forwardAxisSign,
                upVector=upVector, upAxis=self.upAxis, upAxisSign=self.upAxisSign,
            )

            matrix *= startNode.parentInverseMatrix()

            # Apply matrix to start node
            # Best to skip scale since we could accidentally zero it out
            #
            log.info('Applying aim matrix to: %s' % startNode.name())

            startNode.snapshot()
            startNode.setMatrix(matrix, skipTranslate=True, skipScale=True)

            if freezeTransform:

                startNode.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                startNode.assumeSnapshot()
    # endregion

    # region Slots
    @QtCore.Slot(int)
    def on_forwardAxisButtonGroup_idClicked(self, index):
        """
        Slot method for the forwardAxisButtonGroup's `idClicked` signal.
        This method updates the current forward axis.

        :type index: int
        :rtype: None
        """

        if index != self.upAxis:

            self._forwardAxis = index

        else:

            self.sender().buttons()[self.forwardAxis].setChecked(True)

    @QtCore.Slot(int)
    def on_upAxisButtonGroup_idClicked(self, index):
        """
        Slot method for the upAxisButtonGroup's `idClicked` signal.
        This method updates the current up axis.

        :type index: int
        :rtype: None
        """

        if index != self.forwardAxis:

            self._upAxis = index

        else:

            self.sender().buttons()[self.upAxis].setChecked(True)

    @QtCore.Slot(bool)
    def on_worldUpVectorPushButton_clicked(self, checked=False):
        """
        Slot method for the worldUpVectorButton's `clicked` signal.
        The method updates the current world-up vector.

        :type checked: bool
        :rtype: None
        """

        # Get active selection
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        worldUpVector = vector.Vector()

        if selectionCount == 0:

            QtWidgets.QMessageBox.warning(self, "Ez'Align", 'No nodes selected!')
            return

        elif selectionCount == 1:

            worldUpVector = self.axisVector(selection[0], self.upAxis)  # Copy axis vector

        elif selectionCount == 2:

            worldUpVector = self.forwardVector(selection[0], selection[1], normalize=True)  # Calculate the forward vector

        else:

            worldUpVector = self.perpendicularVector(selection)  # Calculate the perpendicular vector

        # Update vector edit
        #
        self.worldUpVectorEdit.setVector(worldUpVector)

    @QtCore.Slot(bool)
    def on_worldUpObjectPushButton_clicked(self, checked=False):
        """
        Slot method for the worldUpObjectButton's `clicked` signal.
        This method updates the current world-up object.

        :type checked: bool
        :rtype: None
        """

        # Inspect active selection
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 1:

            QtWidgets.QMessageBox.warning(self, "Ez'Align", 'Only 1 selected node required!')
            return

        # Store object handle
        #
        success = self.worldUpObject.trySetObject(selection[0])

        if success:

            self.worldUpObjectLineEdit.setText(self.worldUpObject.name())
    # endregion

import numpy
import json

from PySide2 import QtCore, QtWidgets, QtGui
from copy import deepcopy
from dcc import fntransform, fnscene
from dcc.math import vectormath, matrixmath
from dcc.userinterface import qlineeditgroup
from ezalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAimTab(qabstracttab.QAbstractTab):
    """
    Overload of QAbstractTab used to align transforms based on an aim matrix.
    """

    # region Dunderscores
    __sign__ = (1.0, -1.0)
    __decimals__ = 3
    __origin__ = deepcopy(vectormath.ORIGIN)
    __axis__ = 'xyz'
    __vectors__ = vectormath.X_AXIS_VECTOR, vectormath.Y_AXIS_VECTOR, vectormath.Z_AXIS_VECTOR

    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :keyword parent: QtWidgets.QWidget
        :keyword f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QAimTab, self).__init__(*args, **kwargs)

        # Declare class variables
        #
        self._forwardAxis = 0
        self._upAxis = 1
        self._worldUpVector = numpy.array([1.0, 0.0, 0.0])
        self._worldUpObject = fntransform.FnTransform()

    def __build__(self, *args, **kwargs):
        """
        Private method used to build the user interface.

        :rtype: None
        """

        # Call parent method
        #
        super(QAimTab, self).__build__(*args, **kwargs)

        # Assign vertical layout
        #
        self.setLayout(QtWidgets.QVBoxLayout())

        # Create forward axis group box
        #
        self.forwardAxisLayout = QtWidgets.QHBoxLayout()

        self.forwardAxisGroupBox = QtWidgets.QGroupBox('Forward Axis:')
        self.forwardAxisGroupBox.setLayout(self.forwardAxisLayout)

        self.forwardXRadioButton = QtWidgets.QRadioButton('X')
        self.forwardYRadioButton = QtWidgets.QRadioButton('Y')
        self.forwardZRadioButton = QtWidgets.QRadioButton('Z')

        self.forwardAxisButtonGroup = QtWidgets.QButtonGroup(parent=self)
        self.forwardAxisButtonGroup.addButton(self.forwardXRadioButton, id=0)
        self.forwardAxisButtonGroup.addButton(self.forwardYRadioButton, id=1)
        self.forwardAxisButtonGroup.addButton(self.forwardZRadioButton, id=2)
        self.forwardAxisButtonGroup.buttons()[0].setChecked(True)
        self.forwardAxisButtonGroup.idClicked.connect(self.forwardAxisButtonGroup_idClicked)

        self.forwardAxisSignComboBox = QtWidgets.QComboBox()
        self.forwardAxisSignComboBox.addItems(['+', '-'])
        self.forwardAxisSignComboBox.setEditable(False)
        self.forwardAxisSignComboBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.forwardAxisSignComboBox.setFixedSize(QtCore.QSize(48, 24))

        self.forwardAxisLayout.addWidget(self.forwardXRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardYRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardZRadioButton)
        self.forwardAxisLayout.addWidget(self.forwardAxisSignComboBox)

        self.layout().addWidget(self.forwardAxisGroupBox)

        # Create up axis group box
        #
        self.upAxisLayout = QtWidgets.QHBoxLayout()

        self.upAxisGroupBox = QtWidgets.QGroupBox('Up Axis:')
        self.upAxisGroupBox.setLayout(self.upAxisLayout)

        self.upXRadioButton = QtWidgets.QRadioButton('X')
        self.upYRadioButton = QtWidgets.QRadioButton('Y')
        self.upZRadioButton = QtWidgets.QRadioButton('Z')

        self.upAxisButtonGroup = QtWidgets.QButtonGroup(parent=self)
        self.upAxisButtonGroup.addButton(self.upXRadioButton, id=0)
        self.upAxisButtonGroup.addButton(self.upYRadioButton, id=1)
        self.upAxisButtonGroup.addButton(self.upZRadioButton, id=2)
        self.upAxisButtonGroup.buttons()[1].setChecked(True)
        self.upAxisButtonGroup.idClicked.connect(self.upAxisButtonGroup_idClicked)

        self.upAxisSignComboBox = QtWidgets.QComboBox()
        self.upAxisSignComboBox.addItems(['+', '-'])
        self.upAxisSignComboBox.setEditable(False)
        self.upAxisSignComboBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.upAxisSignComboBox.setFixedSize(QtCore.QSize(48, 24))

        self.upAxisLayout.addWidget(self.upXRadioButton)
        self.upAxisLayout.addWidget(self.upYRadioButton)
        self.upAxisLayout.addWidget(self.upZRadioButton)
        self.upAxisLayout.addWidget(self.upAxisSignComboBox)

        self.layout().addWidget(self.upAxisGroupBox)

        # Create world up group box
        #
        self.worldUpLayout = QtWidgets.QGridLayout()

        self.worldUpGroupBox = QtWidgets.QGroupBox('World Up:')
        self.worldUpGroupBox.setLayout(self.worldUpLayout)

        self.layout().addWidget(self.worldUpGroupBox)

        # Create world up type items
        #
        self.worldUpTypeLabel = QtWidgets.QLabel('Type:')
        self.worldUpTypeLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.worldUpTypeComboBox = QtWidgets.QComboBox()
        self.worldUpTypeComboBox.addItems(['Scene Up', 'Object Up', 'Object Rotation Up', 'Vector'])
        self.worldUpTypeComboBox.setEditable(False)

        self.worldUpLayout.addWidget(self.worldUpTypeLabel, 0, 0)
        self.worldUpLayout.addWidget(self.worldUpTypeComboBox, 0, 1)

        # Create world up vector items
        #
        self.validator = QtGui.QDoubleValidator(-1.0, 1.0, self.__decimals__, self)
        self.validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        self.worldUpVectorLabel = QtWidgets.QLabel('Vector:')
        self.worldUpVectorLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.worldUpVectorXLineEdit = QtWidgets.QLineEdit('1.0')
        self.worldUpVectorXLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.worldUpVectorXLineEdit.setFixedHeight(24)
        self.worldUpVectorXLineEdit.setValidator(self.validator)
        self.worldUpVectorXLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.worldUpVectorYLineEdit = QtWidgets.QLineEdit('0.0')
        self.worldUpVectorYLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.worldUpVectorYLineEdit.setFixedHeight(24)
        self.worldUpVectorYLineEdit.setValidator(self.validator)
        self.worldUpVectorYLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.worldUpVectorZLineEdit = QtWidgets.QLineEdit('0.0')
        self.worldUpVectorZLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.worldUpVectorZLineEdit.setFixedHeight(24)
        self.worldUpVectorZLineEdit.setValidator(self.validator)
        self.worldUpVectorZLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.worldUpVectorLineEditGroup = qlineeditgroup.QLineEditGroup(parent=self)
        self.worldUpVectorLineEditGroup.addLineEdit(self.worldUpVectorXLineEdit, id=0)
        self.worldUpVectorLineEditGroup.addLineEdit(self.worldUpVectorYLineEdit, id=1)
        self.worldUpVectorLineEditGroup.addLineEdit(self.worldUpVectorZLineEdit, id=2)
        self.worldUpVectorLineEditGroup.idTextChanged.connect(self.worldUpVectorLineEditGroup_idTextChanged)

        self.worldUpVectorButton = QtWidgets.QPushButton('Pick')
        self.worldUpVectorButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.worldUpVectorButton.setFixedSize(QtCore.QSize(48, 24))
        self.worldUpVectorButton.clicked.connect(self.worldUpVectorButton_clicked)

        self.worldUpVectorLayout = QtWidgets.QHBoxLayout()
        self.worldUpVectorLayout.addWidget(self.worldUpVectorXLineEdit)
        self.worldUpVectorLayout.addWidget(self.worldUpVectorYLineEdit)
        self.worldUpVectorLayout.addWidget(self.worldUpVectorZLineEdit)
        self.worldUpVectorLayout.addWidget(self.worldUpVectorButton)

        self.worldUpLayout.addWidget(self.worldUpVectorLabel, 1, 0)
        self.worldUpLayout.addLayout(self.worldUpVectorLayout, 1, 1)

        # Create world up object items
        #
        self.worldUpObjectLabel = QtWidgets.QLabel('Object:')
        self.worldUpObjectLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.worldUpObjectLineEdit = QtWidgets.QLineEdit('')
        self.worldUpObjectLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.worldUpObjectLineEdit.setFixedHeight(24)
        self.worldUpObjectLineEdit.setReadOnly(True)

        self.worldUpObjectButton = QtWidgets.QPushButton('Pick')
        self.worldUpObjectButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.worldUpObjectButton.setFixedSize(QtCore.QSize(48, 24))
        self.worldUpObjectButton.clicked.connect(self.worldUpObjectButton_clicked)

        self.worldUpObjectLayout = QtWidgets.QHBoxLayout()
        self.worldUpObjectLayout.addWidget(self.worldUpObjectLineEdit)
        self.worldUpObjectLayout.addWidget(self.worldUpObjectButton)

        self.worldUpLayout.addWidget(self.worldUpObjectLabel, 2, 0)
        self.worldUpLayout.addLayout(self.worldUpObjectLayout, 2, 1)
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

        if self._forwardAxis != forwardAxis:

            self._forwardAxis = forwardAxis
            self.forwardAxisButtonGroup.buttons()[forwardAxis].setChecked(True)

    @property
    def forwardAxisSign(self):
        """
        Getter method that returns the forward axis sign.

        :rtype: int
        """

        return self.__sign__[self.forwardAxisSignComboBox.currentIndex()]

    @forwardAxisSign.setter
    def forwardAxisSign(self, forwardAxisSign):
        """
        Setter method that updates the forward axis sign.

        :type forwardAxisSign: int
        :rtype: None
        """

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

        if self._upAxis != upAxis:

            self._upAxis = upAxis
            self.upAxisButtonGroup.buttons()[upAxis].setChecked(True)

    @property
    def upAxisSign(self):
        """
        Getter method that returns the up axis sign.

        :rtype: int
        """

        return self.__sign__[self.upAxisSignComboBox.currentIndex()]

    @upAxisSign.setter
    def upAxisSign(self, upAxisSign):
        """
        Setter method that updates the forward axis sign.

        :type upAxisSign: int
        :rtype: None
        """

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

        self.worldUpTypeComboBox.setCurrentIndex(worldUpType)

    @property
    def worldUpVector(self):
        """
        Getter method that returns the world up vector.

        :rtype: numpy.array
        """

        return self._worldUpVector

    @worldUpVector.setter
    def worldUpVector(self, worldUpVector):
        """
        Setter method that updates the world up vector.

        :type worldUpVector: numpy.array
        :rtype: None
        """

        if not numpy.array_equal(self._worldUpVector, worldUpVector):

            self.worldUpVectorXLineEdit.setText(str(self._worldUpVector[0]))
            self.worldUpVectorYLineEdit.setText(str(self._worldUpVector[1]))
            self.worldUpVectorZLineEdit.setText(str(self._worldUpVector[2]))

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
        self.forwardAxisSign = settings.value('tabs/aim/forwardAxisSign', defaultValue=0, type=int)

        self.upAxis = settings.value('tabs/aim/upAxis', defaultValue=1, type=int)
        self.upAxisSign = settings.value('tabs/aim/upAxisSign', defaultValue=0, type=int)

        self.worldUpType = settings.value('tabs/aim/worldUpType', defaultValue=0, type=int)
        self.worldUpVector = json.loads(settings.value('tabs/aim/worldUpVector', defaultValue='[1.0, 0.0, 0.0]', type=str))

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
        settings.setValue('tabs/aim/worldUpVector', json.dumps(self.worldUpVector.tolist()))

    def forwardVector(self, start, end, normalize=False):
        """
        Returns the forward vector between two nodes.

        :type start: Any
        :type end: Any
        :type normalize: bool
        :rtype: numpy.array
        """

        # Get forward vector between nodes
        #
        fnStart = fntransform.FnTransform(start)
        fnEnd = fntransform.FnTransform(end)

        startPoint = numpy.array(fnStart.translation(worldSpace=True))
        endPoint = numpy.array(fnEnd.translation(worldSpace=True))
        forwardVector = endPoint - startPoint

        # Check if vector should be normalized
        #
        if normalize:

            return vectormath.normalizeVector(forwardVector)

        else:

            return forwardVector

    def upVector(self, start, end, normalize=False):
        """
        Returns the up vector based on the selected world up settings.

        :type start: Any
        :type end: Any
        :type normalize: bool
        :rtype: numpy.array
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

            return vectormath.normalizeVector(self.worldUpVector)

        else:

            raise RuntimeError('Unknown world up type detected!')

    def perpendicularVector(self, nodes):
        """
        Returns the perpendicular vector from the supplied nodes.
        This function is intended to be used with limbs in order to derive a pole vector.

        :type nodes: list[om.MObject]
        :rtype: om.MVector
        """

        # Verify there are enough nodes
        #
        numNodes = len(nodes)

        if not numNodes >= 3:

            log.warning('perpendicularVector() expects at least 3 nodes (%s given)!' % numNodes)
            return

        # Iterate through nodes
        #
        fnStart = fntransform.FnTransform(nodes[0])
        fnEnd = fntransform.FnTransform()

        origin = fnStart.translation(worldSpace=True)
        vectors = []

        for i in range(1, numNodes, 2):

            fnStart.setObject(nodes[i])
            fnEnd.setObject(nodes[i+1])

            startPoint = numpy.array(fnStart.translation(worldSpace=True))
            endPoint = numpy.array(fnEnd.translation(worldSpace=True))

            cross = numpy.cross(vectormath.normalizeVector(startPoint - origin), vectormath.normalizeVector(endPoint - origin))
            vectors.append(cross)

        return self.averageVectors(vectors, normalize=True)

    def averageVectors(self, vectors, normalize=False):
        """
        Returns the averaged vector from a list of vectors.

        :type vectors: list[numpy.array]
        :type normalize: bool
        :rtype: numpy.array
        """

        vector = sum(vectors) / len(vectors)

        if normalize:

            vectormath.normalizeVector(vector)

        return vector

    def remainingAxis(self):
        """
        Getter method used to return the unused axis.

        :rtype: int
        """

        return [x for x in [0, 1, 2] if x not in (self.forwardAxis, self.upAxis)][0]

    def sceneUpVector(self):
        """
        Returns the current scene up vector.

        :rtype: numpy.array
        """

        fnScene = fnscene.FnScene()
        upAxis = fnScene.getUpAxis()
        index = self.__axes__.index(upAxis.lower())

        return deepcopy(self.__vectors__[index])

    def worldUpObjectVector(self, start, normalize=False):
        """
        Returns the world up object vector.

        :type start: Any
        :type normalize: bool
        :rtype: numpy.array
        """

        # Check if world up object is valid
        #
        worldUpObjectVector = deepcopy(self.worldUpVector)

        if self.worldUpObject.isValid():

            fnStart = fntransform.FnTransform(start)
            startPoint = numpy.array(fnStart.translation(worldSpace=True))
            endPoint = numpy.array(self.worldUpObject.translation(worldSpace=True))

            worldUpObjectVector = (endPoint - startPoint)

        else:

            log.warning('Unable to locate world up object!')

        # Check if vector should be normalized
        #
        if normalize:

            return vectormath.normalizeVector(worldUpObjectVector)

        else:

            return worldUpObjectVector

    def worldUpObjectRotationVector(self):
        """
        Returns the world up rotation vector from the world up object.
        If the world up object is invalid then the world up vector is returned instead.

        :rtype: numpy.matrix
        """

        if self.worldUpObject.isValid():

            worldMatrix = self.worldUpObjectMatrix()
            x, y, z, p = matrixmath.breakMatrix(worldMatrix, normalize=True)

            return numpy.array(
                [
                    x * self.worldUpVector[0],
                    y * self.worldUpVector[1],
                    z * self.worldUpVector[2]
                ]
            )

        else:

            return deepcopy(self.worldUpVector)

    def worldUpObjectMatrix(self):
        """
        Returns the world up matrix from the world up object.
        If the world up object is invalid then an identity matrix is returned instead.

        :rtype: numpy.matrix
        """

        # Check if world up object is alive
        #
        if self.worldUpObject.isValid():

            return self.worldUpObject.worldMatrix()

        else:

            return deepcopy(matrixmath.IDENTITY_MATRIX)

    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Aims the active selection to each subsequent node in the selection.
        By default this operation will always preserve children!

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        # Get active selection
        #
        selection = fntransform.FnTransform.getActiveSelection()
        selectionCount = len(selection)

        if not selectionCount >= 2:

            log.warning('apply() expects at least two selected node (%s given)!' % selectionCount)
            return

        # Iterate through selection
        #
        fnTransform = fntransform.FnTransform()

        for i in range(selectionCount - 1):  # Make sure to skip the last item!

            # Get dag paths to nodes
            #
            start, end = selection[i], selection[i+1]
            fnTransform.setObject(start)

            origin = numpy.array(fnTransform.translation(worldSpace=True))
            forwardVector = self.forwardVector(start, end, normalize=True)
            upVector = self.upVector(start, end, normalize=True)

            # Compose aim matrix in parent space
            #
            matrix = matrixmath.createAimMatrix(
                self.forwardAxis, forwardVector,
                self.upAxis, upVector,
                origin=origin,
                forwardAxisSign=self.forwardAxisSign,
                upAxisSign=self.upAxisSign
            )

            matrix *= fnTransform.parentInverseMatrix()

            # Apply matrix to start node
            # Best to skip scale since we could accidentally zero it out
            #
            log.info('Applying aim matrix to: %s' % fnTransform.name())

            fnTransform.snapshot()
            fnTransform.setMatrix(matrix, skipTranslate=True, skipScale=True)

            if freezeTransform:

                fnTransform.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                fnTransform.assumeSnapshot()
    # endregion

    # region Slots
    def forwardAxisButtonGroup_idClicked(self, index):
        """
        Id clicked slot method responsible for updating the forward axis.

        :type index: int
        :rtype: None
        """

        if index != self.upAxis:

            self.forwardAxis = index

        else:

            self.sender().buttons()[self.forwardAxis].setChecked(True)

    def upAxisButtonGroup_idClicked(self, index):
        """
        Id clicked slot method responsible for updating the up axis.

        :type index: int
        :rtype: None
        """

        if index != self.forwardAxis:

            self.upAxis = index

        else:

            self.sender().buttons()[self.upAxis].setChecked(True)

    def worldUpVectorLineEditGroup_idTextChanged(self, index):
        """
        ID text changed slot method responsible for updating the world up vector.

        :type index: int
        :rtype: None
        """

        group = self.sender()
        lineEdit = group[index]

        self.worldUpVector[index] = float(lineEdit.text())

    def worldUpVectorButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for updating the world up vector.

        :type checked: bool
        :rtype: None
        """

        # Get active selection
        #
        selection = self.worldUpObject.getActiveSelection()
        selectionCount = len(selection)

        worldUpVector = numpy.array([0.0, 0.0, 0.0])

        if selectionCount == 0:

            log.warning('worldUpVectorButton_clicked() expects at least one selected node (%s given)!' % selectionCount)
            return

        elif selectionCount == 1:

            worldUpVector = self.getAxisVector(selection[0], axis=self.upAxis)

        elif selectionCount == 2:

            # Calculate the forward vector
            #
            worldUpVector = self.forwardVector(selection[0], selection[1], normalize=True)

        else:

            # Calculate the perpendicular vector
            #
            worldUpVector = self.perpendicularVector(selection)

        # Assign vector to text fields
        #
        self.worldUpVectorXLineEdit.setText(str(worldUpVector[0]))
        self.worldUpVectorYLineEdit.setText(str(worldUpVector[1]))
        self.worldUpVectorZLineEdit.setText(str(worldUpVector[2]))

    def worldUpObjectButton_clicked(self, checked=False):
        """
        Clicked slot method responsible for updating the world up object.

        :type checked: bool
        :rtype: None
        """

        # Inspect active selection
        #
        selection = self.worldUpObject.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 1:

            log.warning('worldUpObjectButton_clicked() expects one selected node (%s given)!' % selectionCount)
            return

        # Store object handle
        #
        success = self.worldUpObject.trySetObject(selection[0])

        if success:

            self.worldUpObjectLineEdit.setText(self.worldUpObject.name())
    # endregion

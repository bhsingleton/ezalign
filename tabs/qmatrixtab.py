import json

from Qt import QtCore, QtWidgets, QtGui
from dcc import fnnode, fntransform, fnmesh
from dcc.dataclasses import vector, transformationmatrix
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

        # Declare class variables
        #
        self._origin = vector.Vector.zero
        self._forwardAxis = 0
        self._forwardVector = vector.Vector.xAxis
        self._upAxis = 1
        self._upVector = vector.Vector.yAxis
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

        if self._forwardAxis != forwardAxis and self._forwardAxis != self._upAxis:

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

        if self._upAxis != upAxis and self._upAxis != self._forwardAxis:

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

        self._upVector = vector.Vector(*upVector)
        self.invalidate()
    # endregion

    # region Methods
    def postLoad(self):
        """
        Called after the user interface has been loaded.

        :rtype: None
        """

        self.forwardAxisButtonGroup.setId(self.forwardXRadioButton, 0)
        self.forwardAxisButtonGroup.setId(self.forwardYRadioButton, 1)
        self.forwardAxisButtonGroup.setId(self.forwardZRadioButton, 2)

        self.upAxisButtonGroup.setId(self.upXRadioButton, 0)
        self.upAxisButtonGroup.setId(self.upYRadioButton, 1)
        self.upAxisButtonGroup.setId(self.upZRadioButton, 2)

    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        self.origin = json.loads(settings.value('tabs/matrix/origin', defaultValue='[0.0, 0.0, 0.0]'))

        self.forwardAxis = settings.value('tabs/matrix/forwardAxis', defaultValue=0)
        self.forwardVector = json.loads(settings.value('tabs/matrix/forwardVector', defaultValue='[1.0, 0.0, 0.0]'))

        self.upAxis = settings.value('tabs/matrix/upAxis', defaultValue=1)
        self.upVector = json.loads(settings.value('tabs/matrix/upVector', defaultValue='[0.0, 1.0, 0.0]'))
        
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

        # Compose aim matrix
        #
        log.debug('Origin: %s' % self.origin)
        log.debug('Forward Axis: %s, Forward Vector: %s' % (self.forwardAxis, self.forwardVector))
        log.debug('Up Axis: %s, Up Vector: %s' % (self.upAxis, self.upVector))

        matrix = transformationmatrix.TransformationMatrix(row4=self.origin)
        matrix.lookAt(forwardVector=self.forwardVector, forwardAxis=self.forwardAxis, upVector=self.upVector, upAxis=self.upAxis)

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
        :rtype: transformationmatrix.TransformationMatrix
        """

        fnTransform = fntransform.FnTransform(node)
        worldMatrix = fnTransform.worldMatrix()

        return vector.Vector(*worldMatrix[axis]).normalize()

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

        center = vector.Vector()

        if selectionCount == 0:

            log.warning('No transform nodes found in active selection!')
            return center

        # Iterate through selection
        #
        node = fnnode.FnNode()
        transform = fntransform.FnTransform()
        mesh = fnmesh.FnMesh()

        weight = 1.0 / selectionCount

        for (index, obj) in enumerate(selection):

            # Check if selection contains a component
            #
            node.setObject(obj)

            if node.isMesh():

                mesh.setObject(obj)
                vertexIndices = mesh.selectedVertices()
                centerPoint = (sum(list(mesh.iterVertices(*vertexIndices, worldSpace=True))) / len(vertexIndices))

                center += centerPoint * weight

            elif transform.isTransform():

                transform.setObject(obj)
                translation = transform.translation(worldSpace=True)

                center += translation * weight

            else:

                continue

        return center

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
            node.setMatrix(matrix, preserveChildren=preserveChildren)

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

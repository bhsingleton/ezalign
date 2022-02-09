import numpy

from PySide2 import QtCore, QtWidgets, QtGui
from dcc import fntransform
from dcc.math import matrixmath
from quickalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAlignTab(qabstracttab.QAbstractTab):
    """
    Overload of QAbstractTab used to align two transforms.
    """

    def __init__(self, *args, **kwargs):
        """
        Overloaded method called after a new instance has been created.

        :keyword parent: QtWidgets.QWidget
        :keyword f: int
        :rtype: None
        """

        # Call parent method
        #
        super(QAlignTab, self).__init__(*args, **kwargs)

        # Assign vertical layout
        #
        self.setLayout(QtWidgets.QVBoxLayout())

        # Create position group box
        #
        self.translateLayout = QtWidgets.QHBoxLayout()

        self.translateGroupBox = QtWidgets.QGroupBox('Align Translation:')
        self.translateGroupBox.setLayout(self.translateLayout)

        self.translateXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.translateYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.translateZCheckBox = QtWidgets.QCheckBox('Z-Axis')

        self.translateLayout.addWidget(self.translateXCheckBox)
        self.translateLayout.addWidget(self.translateYCheckBox)
        self.translateLayout.addWidget(self.translateZCheckBox)

        self.layout().addWidget(self.translateGroupBox)

        # Create the source object properties
        #
        self.sourceLayout = QtWidgets.QVBoxLayout()

        self.sourceGroupBox = QtWidgets.QGroupBox('Source Object:')
        self.sourceGroupBox.setLayout(self.sourceLayout)

        self.sourceMinRadioButton = QtWidgets.QRadioButton('Minimum')
        self.sourceMinRadioButton.setToolTip("Aligns the point on the object's bounding box with the lowest X, Y, and Z values with the chosen point on the other object.")

        self.sourceCenterRadioButton = QtWidgets.QRadioButton('Center')
        self.sourceCenterRadioButton.setToolTip("Aligns the center of the object's bounding box with the chosen point on the other object.")

        self.sourcePivotRadioButton = QtWidgets.QRadioButton('Pivot Point')
        self.sourcePivotRadioButton.setToolTip("Aligns the object's pivot point with the chosen point on the other object.")

        self.sourceMaxRadioButton = QtWidgets.QRadioButton('Maximum')
        self.sourceMaxRadioButton.setToolTip("Aligns the point on the object's bounding box with the highest X, Y, and Z values with the chosen point on the other object.")

        self.sourceRadioButtons = (self.sourceMinRadioButton, self.sourceCenterRadioButton, self.sourcePivotRadioButton, self.sourceMaxRadioButton)

        self.sourceLayout.addWidget(self.sourceMinRadioButton)
        self.sourceLayout.addWidget(self.sourceCenterRadioButton)
        self.sourceLayout.addWidget(self.sourcePivotRadioButton)
        self.sourceLayout.addWidget(self.sourceMaxRadioButton)

        # Create target properties
        #
        self.targetLayout = QtWidgets.QVBoxLayout()

        self.targetGroupBox = QtWidgets.QGroupBox('Target Object:')
        self.targetGroupBox.setLayout(self.targetLayout)

        self.targetMinRadioButton = QtWidgets.QRadioButton('Minimum')
        self.targetMinRadioButton.setToolTip("Aligns the point on the object's bounding box with the lowest X, Y, and Z values with the chosen point on the other object.")

        self.targetCenterRadioButton = QtWidgets.QRadioButton('Center')
        self.targetCenterRadioButton.setToolTip("Aligns the center of the object's bounding box with the chosen point on the other object.")

        self.targetPivotRadioButton = QtWidgets.QRadioButton('Pivot Point')
        self.targetPivotRadioButton.setToolTip("Aligns the object's pivot point with the chosen point on the other object.")

        self.targetMaxRadioButton = QtWidgets.QRadioButton('Maximum')
        self.targetMaxRadioButton.setToolTip("Aligns the point on the object's bounding box with the highest X, Y, and Z values with the chosen point on the other object.")

        self.targetRadioButtons = (self.targetMinRadioButton, self.targetCenterRadioButton, self.targetPivotRadioButton, self.targetMaxRadioButton)

        self.targetLayout.addWidget(self.targetMinRadioButton)
        self.targetLayout.addWidget(self.targetCenterRadioButton)
        self.targetLayout.addWidget(self.targetPivotRadioButton)
        self.targetLayout.addWidget(self.targetMaxRadioButton)

        # Create the object layout
        #
        self.objectLayout = QtWidgets.QHBoxLayout()

        self.objectLayout.addWidget(self.sourceGroupBox)
        self.objectLayout.addWidget(self.targetGroupBox)

        self.layout().addLayout(self.objectLayout)

        # Create the rotation group box
        #
        self.rotationLayout = QtWidgets.QHBoxLayout()

        self.rotationGroupBox = QtWidgets.QGroupBox('Align Rotation:')
        self.rotationGroupBox.setLayout(self.rotationLayout)

        self.rotateXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.rotateYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.rotateZCheckBox = QtWidgets.QCheckBox('Z-Axis')

        self.rotationLayout.addWidget(self.rotateXCheckBox)
        self.rotationLayout.addWidget(self.rotateYCheckBox)
        self.rotationLayout.addWidget(self.rotateZCheckBox)

        self.layout().addWidget(self.rotationGroupBox)

        # Create the scale group box
        #
        self.scaleLayout = QtWidgets.QHBoxLayout()

        self.scaleGroupBox = QtWidgets.QGroupBox('Match Scale:')
        self.scaleGroupBox.setLayout(self.scaleLayout)

        self.scaleXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.scaleYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.scaleZCheckBox = QtWidgets.QCheckBox('Z-Axis')

        self.scaleLayout.addWidget(self.scaleXCheckBox)
        self.scaleLayout.addWidget(self.scaleYCheckBox)
        self.scaleLayout.addWidget(self.scaleZCheckBox)

        self.layout().addWidget(self.scaleGroupBox)

        # Set startup defaults
        #
        self.sourcePivotRadioButton.setChecked(True)
        self.targetPivotRadioButton.setChecked(True)

        self.translateXCheckBox.setChecked(True)
        self.translateYCheckBox.setChecked(True)
        self.translateZCheckBox.setChecked(True)

        self.rotateXCheckBox.setChecked(True)
        self.rotateYCheckBox.setChecked(True)
        self.rotateZCheckBox.setChecked(True)

    @property
    def skipTranslateX(self):
        """
        Getter method used to check if translateX should be skipped.

        :rtype: bool
        """

        return not self.translateXCheckBox.isChecked()

    @property
    def skipTranslateY(self):
        """
        Getter method used to check if translateY should be skipped.

        :rtype: bool
        """

        return not self.translateYCheckBox.isChecked()

    @property
    def skipTranslateZ(self):
        """
        Getter method used to check if translateZ should be skipped.

        :rtype: bool
        """

        return not self.translateZCheckBox.isChecked()

    @property
    def skipRotateX(self):
        """
        Getter method used to check if rotateX should be skipped.

        :rtype: bool
        """

        return not self.rotateXCheckBox.isChecked()

    @property
    def skipRotateY(self):
        """
        Getter method used to check if rotateY should be skipped.

        :rtype: bool
        """

        return not self.rotateYCheckBox.isChecked()

    @property
    def skipRotateZ(self):
        """
        Getter method used to check if rotateZ should be skipped.

        :rtype: bool
        """

        return not self.rotateZCheckBox.isChecked()

    @property
    def skipScaleX(self):
        """
        Getter method used to check if the scaleX value should be skipped.

        :rtype: bool
        """

        return not self.scaleXCheckBox.isChecked()

    @property
    def skipScaleY(self):
        """
        Getter method used to check if the scaleY value should be skipped.

        :rtype: bool
        """

        return not self.scaleYCheckBox.isChecked()

    @property
    def skipScaleZ(self):
        """
        Getter method used to check if the scaleZ value should be skipped.

        :rtype: bool
        """

        return not self.scaleZCheckBox.isChecked()

    def getSourceType(self):
        """
        Returns the selected source type.

        :rtype: int
        """

        return [x.isChecked() for x in self.sourceRadioButtons].index(True)

    def getSourceObject(self):
        """
        Evaluates the active selection to return the data related to the source object.
        This includes a dag path, and offset matrix.
        Please note that bounding boxes are returned in world space!

        :rtype: fntransform.FnTransform, om.MMatrix
        """

        # Get selection list
        #
        fnTransform = fntransform.FnTransform()

        selection = fnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('getSourceObject() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        source = selection[0]
        success = fnTransform.trySetObject(source)

        if not success:

            raise TypeError('getSourceObject() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = fnTransform.worldMatrix()
        offsetMatrix = matrixmath.IDENTITY_MATRIX

        sourceType = self.getSourceType()

        if sourceType == 0:  # Minimum

            boundingBox = fnTransform.boundingBox()
            minPoint = numpy.array([boundingBox[0], boundingBox[2], boundingBox[4]])
            boundingMatrix = matrixmath.createTranslateMatrix(minPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        elif sourceType == 1:  # Center

            boundingBox = fnTransform.boundingBox()
            centerPoint = (numpy.array([boundingBox[0], boundingBox[2], boundingBox[4]]) * 0.5) + (numpy.array([boundingBox[1], boundingBox[3], boundingBox[5]]) * 0.5)
            boundingMatrix = matrixmath.createTranslateMatrix(centerPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        elif sourceType == 2:  # Pivot Point

            pass

        elif sourceType == 3:  # Maximum

            boundingBox = fnTransform.boundingBox()
            maxPoint = numpy.array([boundingBox[1], boundingBox[3], boundingBox[5]])
            boundingMatrix = matrixmath.createTranslateMatrix(maxPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        else:

            pass

        # Return results
        #
        return source, offsetMatrix

    def getTargetType(self):
        """
        Returns the selected target type.

        :rtype: int
        """

        return [x.isChecked() for x in self.targetRadioButtons].index(True)

    def getTargetObject(self):
        """
        Evaluates the active selection to return the data related to the target object.
        This includes a dag path and offset matrix.
        Please note that bounding boxes are returned in world space!

        :rtype: fntransform.FnTransform, om.MMatrix
        """

        # Get selection list
        #
        fnTransform = fntransform.FnTransform()

        selection = fnTransform.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('getTargetObject() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        target = selection[1]
        success = fnTransform.trySetObject(target)

        if not success:

            raise TypeError('getTargetObject() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = fnTransform.worldMatrix()
        offsetMatrix = matrixmath.IDENTITY_MATRIX

        sourceType = self.getTargetType()

        if sourceType == 0:  # Minimum

            boundingBox = fnTransform.boundingBox()
            minPoint = numpy.array([boundingBox[0], boundingBox[2], boundingBox[4]])
            boundingMatrix = matrixmath.createTranslateMatrix(minPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        elif sourceType == 1:  # Center

            boundingBox = fnTransform.boundingBox()
            centerPoint = (numpy.array([boundingBox[0], boundingBox[2], boundingBox[4]]) * 0.5) + (numpy.array([boundingBox[1], boundingBox[3], boundingBox[5]]) * 0.5)
            boundingMatrix = matrixmath.createTranslateMatrix(centerPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        elif sourceType == 2:  # Pivot Point

            pass

        elif sourceType == 3:  # Maximum

            boundingBox = fnTransform.boundingBox()
            maxPoint = numpy.array([boundingBox[1], boundingBox[3], boundingBox[5]])
            boundingMatrix = matrixmath.createTranslateMatrix(maxPoint)

            offsetMatrix = (matrixmath.decomposeMatrix(worldMatrix)[1] * boundingMatrix) * worldMatrix.I

        else:

            pass

        # Return results
        #
        return target, offsetMatrix

    def apply(self, preserveChildren=False):
        """
        Aligns the active selection.
        The expected selection order consists of two nodes:
            [0] Source - The transform to copy from.
            [1] Target - The transform to copy to.

        :type preserveChildren: bool
        :rtype: None
        """

        # Try and evaluate selection
        #
        try:

            # Get source and target objects
            #
            fnSource, sourceOffsetMatrix = self.getSourceObject()
            fnTarget, targetOffsetMatrix = self.getTargetObject()

            # Calculate source transform in target parent space
            # Don't forget to include the offset matrices!
            #
            sourceWorldMatrix = fnSource.worldMatrix()
            targetParentInverseMatrix = fnTarget.parentInverseMatrix()

            targetMatrix = targetOffsetMatrix.I * ((sourceOffsetMatrix * sourceWorldMatrix) * targetParentInverseMatrix)

            # Copy transform matrix
            #
            fnTarget.setMatrix(
                targetMatrix,
                skipTranslateX=self.skipTranslateX, skipTranslateY=self.skipTranslateY, skipTranslateZ=self.skipTranslateZ,
                skipRotateX=self.skipRotateX, skipRotateY=self.skipRotateY, skipRotateZ=self.skipRotateZ,
                skipScaleX=self.skipScaleX, skipScaleY=self.skipScaleY, skipScaleZ=self.skipScaleZ,
                preserveChildren=preserveChildren
            )

        except TypeError as exception:

            log.warning(exception)
            return

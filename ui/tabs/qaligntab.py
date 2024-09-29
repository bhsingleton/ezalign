import json

from Qt import QtCore, QtWidgets, QtGui
from dcc import fntransform
from dcc.dataclasses import transformationmatrix
from . import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAlignTab(qabstracttab.QAbstractTab):
    """
    Overload of `QAbstractTab` that implements copy transform logic.
    """

    # region Dunderscores
    def __setup_ui__(self, *args, **kwargs):
        """
        Private method that initializes the user interface.

        :rtype: None
        """

        # Initialize widget
        #
        self.setWhatsThis('Select the node to paste onto then the node to copy from.')

        # Initialize central layout
        #
        centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(centralLayout)

        # Initialize translation group-box
        #
        self.translationLayout = QtWidgets.QHBoxLayout()
        self.translationLayout.setObjectName('translationLayout')

        self.translationGroupBox = QtWidgets.QGroupBox('Align Translation:')
        self.translationGroupBox.setObjectName('translationGroupBox')
        self.translationGroupBox.setLayout(self.translationLayout)
        self.translationGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.translationGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.translateXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.translateXCheckBox.setObjectName('translationGroupBox')
        self.translateXCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.translateXCheckBox.setFixedHeight(24)
        self.translateXCheckBox.setChecked(True)
        self.translateXCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.translateYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.translateYCheckBox.setObjectName('translateYCheckBox')
        self.translateYCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.translateYCheckBox.setFixedHeight(24)
        self.translateYCheckBox.setChecked(True)
        self.translateYCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.translateZCheckBox = QtWidgets.QCheckBox('Z-Axis')
        self.translateZCheckBox.setObjectName('translateZCheckBox')
        self.translateZCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.translateZCheckBox.setFixedHeight(24)
        self.translateZCheckBox.setChecked(True)
        self.translateZCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.translateCheckBoxGroup = QtWidgets.QButtonGroup(self.translationGroupBox)
        self.translateCheckBoxGroup.setExclusive(False)
        self.translateCheckBoxGroup.addButton(self.translateXCheckBox, id=0)
        self.translateCheckBoxGroup.addButton(self.translateYCheckBox, id=1)
        self.translateCheckBoxGroup.addButton(self.translateZCheckBox, id=2)

        self.translationLayout.addWidget(self.translateXCheckBox)
        self.translationLayout.addWidget(self.translateYCheckBox)
        self.translationLayout.addWidget(self.translateZCheckBox)

        centralLayout.addWidget(self.translationGroupBox)

        # Initialize source object group-box
        #
        self.sourceLayout = QtWidgets.QVBoxLayout()
        self.sourceLayout.setObjectName('sourceLayout')

        self.sourceGroupBox = QtWidgets.QGroupBox('Source Object:')
        self.sourceGroupBox.setObjectName('sourceGroupBox')
        self.sourceGroupBox.setLayout(self.sourceLayout)
        self.sourceGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.sourceGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.sourceMinRadioButton = QtWidgets.QRadioButton('Minimum')
        self.sourceMinRadioButton.setObjectName('sourceMinRadioButton')
        self.sourceMinRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.sourceMinRadioButton.setFixedHeight(24)
        self.sourceMinRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sourceMinRadioButton.setToolTip("Aligns the point on the object's bounding box with the lowest X, Y, and Z values with the chosen point on the other object.")

        self.sourceCenterRadioButton = QtWidgets.QRadioButton('Center')
        self.sourceCenterRadioButton.setObjectName('sourceCenterRadioButton')
        self.sourceCenterRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.sourceCenterRadioButton.setFixedHeight(24)
        self.sourceCenterRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sourceCenterRadioButton.setToolTip("Aligns the center of the object's bounding box with the chosen point on the other object.")

        self.sourcePivotRadioButton = QtWidgets.QRadioButton('Pivot')
        self.sourcePivotRadioButton.setObjectName('sourcePivotRadioButton')
        self.sourcePivotRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.sourcePivotRadioButton.setFixedHeight(24)
        self.sourcePivotRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sourcePivotRadioButton.setChecked(True)
        self.sourcePivotRadioButton.setToolTip("Aligns the object's pivot point with the chosen point on the other object.")

        self.sourceMaxRadioButton = QtWidgets.QRadioButton('Maximum')
        self.sourceMaxRadioButton.setObjectName('sourceMaxRadioButton')
        self.sourceMaxRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.sourceMaxRadioButton.setFixedHeight(24)
        self.sourceMaxRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sourceMaxRadioButton.setToolTip("Aligns the point on the object's bounding box with the highest X, Y, and Z values with the chosen point on the other object.")

        self.sourceRadioButtonGroup = QtWidgets.QButtonGroup(self.sourceGroupBox)
        self.sourceRadioButtonGroup.setObjectName('sourceRadioButtonGroup')
        self.sourceRadioButtonGroup.setExclusive(True)
        self.sourceRadioButtonGroup.addButton(self.sourceMinRadioButton, id=0)
        self.sourceRadioButtonGroup.addButton(self.sourceCenterRadioButton, id=1)
        self.sourceRadioButtonGroup.addButton(self.sourcePivotRadioButton, id=2)
        self.sourceRadioButtonGroup.addButton(self.sourceMaxRadioButton, id=3)

        self.sourceLayout.addWidget(self.sourceMinRadioButton)
        self.sourceLayout.addWidget(self.sourceCenterRadioButton)
        self.sourceLayout.addWidget(self.sourcePivotRadioButton)
        self.sourceLayout.addWidget(self.sourceMaxRadioButton)

        # Initialize target object group-box
        #
        self.targetLayout = QtWidgets.QVBoxLayout()
        self.targetLayout.setObjectName('targetLayout')

        self.targetGroupBox = QtWidgets.QGroupBox('Target Object:')
        self.targetGroupBox.setObjectName('targetGroupBox')
        self.targetGroupBox.setLayout(self.targetLayout)
        self.targetGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.targetGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.targetMinRadioButton = QtWidgets.QRadioButton('Minimum')
        self.targetMinRadioButton.setObjectName('targetMinRadioButton')
        self.targetMinRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.targetMinRadioButton.setFixedHeight(24)
        self.targetMinRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.targetMinRadioButton.setToolTip("Aligns the point on the object's bounding box with the lowest X, Y, and Z values with the chosen point on the other object.")

        self.targetCenterRadioButton = QtWidgets.QRadioButton('Center')
        self.targetCenterRadioButton.setObjectName('targetCenterRadioButton')
        self.targetCenterRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.targetCenterRadioButton.setFixedHeight(24)
        self.targetCenterRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.targetCenterRadioButton.setToolTip("Aligns the center of the object's bounding box with the chosen point on the other object.")

        self.targetPivotRadioButton = QtWidgets.QRadioButton('Pivot')
        self.targetPivotRadioButton.setObjectName('targetPivotRadioButton')
        self.targetPivotRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.targetPivotRadioButton.setFixedHeight(24)
        self.targetPivotRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.targetPivotRadioButton.setChecked(True)
        self.targetPivotRadioButton.setToolTip("Aligns the object's pivot point with the chosen point on the other object.")

        self.targetMaxRadioButton = QtWidgets.QRadioButton('Maximum')
        self.targetMaxRadioButton.setObjectName('targetMaxRadioButton')
        self.targetMaxRadioButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.targetMaxRadioButton.setFixedHeight(24)
        self.targetMaxRadioButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.targetMaxRadioButton.setToolTip("Aligns the point on the object's bounding box with the highest X, Y, and Z values with the chosen point on the other object.")

        self.targetRadioButtonGroup = QtWidgets.QButtonGroup(self.targetGroupBox)
        self.targetRadioButtonGroup.setObjectName('targetRadioButtonGroup')
        self.targetRadioButtonGroup.setExclusive(True)
        self.targetRadioButtonGroup.addButton(self.targetMinRadioButton, id=0)
        self.targetRadioButtonGroup.addButton(self.targetCenterRadioButton, id=1)
        self.targetRadioButtonGroup.addButton(self.targetPivotRadioButton, id=2)
        self.targetRadioButtonGroup.addButton(self.targetMaxRadioButton, id=3)

        self.targetLayout.addWidget(self.targetMinRadioButton)
        self.targetLayout.addWidget(self.targetCenterRadioButton)
        self.targetLayout.addWidget(self.targetPivotRadioButton)
        self.targetLayout.addWidget(self.targetMaxRadioButton)

        # Initialize source/target object layout
        #
        self.objectLayout = QtWidgets.QHBoxLayout()
        self.objectLayout.setObjectName('objectLayout')
        self.objectLayout.setContentsMargins(0, 0, 0, 0)
        self.objectLayout.addWidget(self.sourceGroupBox)
        self.objectLayout.addWidget(self.targetGroupBox)

        centralLayout.addLayout(self.objectLayout)

        # Initialize rotation group-box
        #
        self.rotationLayout = QtWidgets.QHBoxLayout()
        self.rotationLayout.setObjectName('rotationLayout')

        self.rotationGroupBox = QtWidgets.QGroupBox('Align Rotation:')
        self.rotationGroupBox.setObjectName('rotationGroupBox')
        self.rotationGroupBox.setLayout(self.rotationLayout)
        self.rotationGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.rotationGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.rotateXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.rotateXCheckBox.setObjectName('rotationGroupBox')
        self.rotateXCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.rotateXCheckBox.setFixedHeight(24)
        self.rotateXCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotateXCheckBox.setChecked(True)

        self.rotateYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.rotateYCheckBox.setObjectName('rotateYCheckBox')
        self.rotateYCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.rotateYCheckBox.setFixedHeight(24)
        self.rotateYCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotateYCheckBox.setChecked(True)

        self.rotateZCheckBox = QtWidgets.QCheckBox('Z-Axis')
        self.rotateZCheckBox.setObjectName('rotateZCheckBox')
        self.rotateZCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.rotateZCheckBox.setFixedHeight(24)
        self.rotateZCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotateZCheckBox.setChecked(True)

        self.rotateCheckBoxGroup = QtWidgets.QButtonGroup(self.rotationGroupBox)
        self.rotateCheckBoxGroup.setExclusive(False)
        self.rotateCheckBoxGroup.addButton(self.rotateXCheckBox, id=0)
        self.rotateCheckBoxGroup.addButton(self.rotateYCheckBox, id=1)
        self.rotateCheckBoxGroup.addButton(self.rotateZCheckBox, id=2)

        self.rotationLayout.addWidget(self.rotateXCheckBox)
        self.rotationLayout.addWidget(self.rotateYCheckBox)
        self.rotationLayout.addWidget(self.rotateZCheckBox)

        centralLayout.addWidget(self.rotationGroupBox)

        # Initialize scale group-box
        #
        self.scaleLayout = QtWidgets.QHBoxLayout()
        self.scaleLayout.setObjectName('scaleLayout')

        self.scaleGroupBox = QtWidgets.QGroupBox('Align Scale:')
        self.scaleGroupBox.setObjectName('scaleGroupBox')
        self.scaleGroupBox.setLayout(self.scaleLayout)
        self.scaleGroupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.scaleGroupBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.scaleXCheckBox = QtWidgets.QCheckBox('X-Axis')
        self.scaleXCheckBox.setObjectName('scaleGroupBox')
        self.scaleXCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.scaleXCheckBox.setFixedHeight(24)
        self.scaleXCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.scaleYCheckBox = QtWidgets.QCheckBox('Y-Axis')
        self.scaleYCheckBox.setObjectName('scaleYCheckBox')
        self.scaleYCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.scaleYCheckBox.setFixedHeight(24)
        self.scaleYCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.scaleZCheckBox = QtWidgets.QCheckBox('Z-Axis')
        self.scaleZCheckBox.setObjectName('scaleZCheckBox')
        self.scaleZCheckBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))
        self.scaleZCheckBox.setFixedHeight(24)
        self.scaleZCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.scaleCheckBoxGroup = QtWidgets.QButtonGroup(self.scaleGroupBox)
        self.scaleCheckBoxGroup.setExclusive(False)
        self.scaleCheckBoxGroup.addButton(self.scaleXCheckBox, id=0)
        self.scaleCheckBoxGroup.addButton(self.scaleYCheckBox, id=1)
        self.scaleCheckBoxGroup.addButton(self.scaleZCheckBox, id=2)

        self.scaleLayout.addWidget(self.scaleXCheckBox)
        self.scaleLayout.addWidget(self.scaleYCheckBox)
        self.scaleLayout.addWidget(self.scaleZCheckBox)

        centralLayout.addWidget(self.scaleGroupBox)
    # endregion

    # region Properties
    @property
    def sourceType(self):
        """
        Getter methods that returns the source type.

        :rtype: int
        """

        return self.sourceRadioButtonGroup.checkedId()

    @sourceType.setter
    def sourceType(self, sourceType):
        """
        Setter method that updates the source type.

        :type sourceType: int
        :rtype: None
        """

        if isinstance(sourceType, int):

            self.sourceRadioButtonGroup.buttons()[sourceType].setChecked(True)

    @property
    def targetType(self):
        """
        Getter methods that returns the target type.

        :rtype: int
        """

        return self.targetRadioButtonGroup.checkedId()

    @targetType.setter
    def targetType(self, targetType):
        """
        Setter method that updates the target type.

        :type targetType: int
        :rtype: None
        """

        if isinstance(targetType, int):

            self.targetRadioButtonGroup.buttons()[targetType].setChecked(True)
    # endregion

    # region Methods
    def loadSettings(self, settings):
        """
        Loads the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        self.sourceType = settings.value('tabs/align/sourceType', defaultValue=2, type=int)
        self.targetType = settings.value('tabs/align/targetType', defaultValue=2, type=int)

        self.setMatchTranslate(json.loads(settings.value('tabs/align/matchTranslate', defaultValue='[true, true, true]', type=str)))
        self.setMatchRotate(json.loads(settings.value('tabs/align/matchRotate', defaultValue='[true, true, true]', type=str)))
        self.setMatchScale(json.loads(settings.value('tabs/align/matchScale', defaultValue='[false, false, false]', type=str)))

    def saveSettings(self, settings):
        """
        Saves the user settings.

        :type settings: QtCore.QSettings
        :rtype: None
        """

        settings.setValue('tabs/align/sourceType', self.sourceType)
        settings.setValue('tabs/align/targetType', self.targetType)

        settings.setValue('tabs/align/matchTranslate', json.dumps(self.matchTranslate()))
        settings.setValue('tabs/align/matchRotate', json.dumps(self.matchRotate()))
        settings.setValue('tabs/align/matchScale', json.dumps(self.matchScale()))

    def matchTranslate(self):
        """
        Returns the `matchTranslate` flags.

        :rtype: List[bool, bool, bool]
        """

        return [x.isChecked() for x in self.translateCheckBoxGroup.buttons()]

    def setMatchTranslate(self, matchTranslate):
        """
        Updates the `matchTranslate` flags.

        :type matchTranslate: List[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchTranslate):

            self.translateCheckBoxGroup.button(index).setChecked(match)

    def matchRotate(self):
        """
        Returns the `matchRotate` flags.

        :rtype: List[bool, bool, bool]
        """

        return [x.isChecked() for x in self.rotateCheckBoxGroup.buttons()]

    def setMatchRotate(self, matchRotate):
        """
        Updates the `matchRotate` flags.

        :type matchRotate: List[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchRotate):

            self.rotateCheckBoxGroup.button(index).setChecked(match)

    def matchScale(self):
        """
        Returns the `matchScale` flags.

        :rtype: List[bool, bool, bool]
        """

        return [x.isChecked() for x in self.scaleCheckBoxGroup.buttons()]

    def setMatchScale(self, matchScale):
        """
        Updates the `matchScale` flags.

        :type matchScale: List[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchScale):

            self.scaleCheckBoxGroup.button(index).setChecked(match)

    def getSourceInput(self):
        """
        Evaluates the active selection to return the source input.
        Please be aware that bounding boxes are returned in world space!

        :rtype: Tuple[fntransform.FnTransform, transformationmatrix.TransformationMatrix]
        """

        # Get selection list
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('getSourceInput() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        sourceNode = fntransform.FnTransform()
        success = sourceNode.trySetObject(selection[1])

        if not success:

            raise TypeError('getSourceInput() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = sourceNode.worldMatrix()
        offsetMatrix = transformationmatrix.TransformationMatrix()

        if self.sourceType == 0:  # Minimum

            boundingBox = sourceNode.boundingBox()
            translateMatrix = transformationmatrix.TransformationMatrix(row4=boundingBox.min)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        elif self.sourceType == 1:  # Center

            boundingBox = sourceNode.boundingBox()
            centerPoint = (boundingBox.min * 0.5) + (boundingBox.max * 0.5)
            translateMatrix = transformationmatrix.TransformationMatrix(row4=centerPoint)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        elif self.sourceType == 2:  # Pivot Point

            pass

        elif self.sourceType == 3:  # Maximum

            boundingBox = sourceNode.boundingBox()
            translateMatrix = transformationmatrix.TransformationMatrix(row4=boundingBox.max)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        else:

            pass

        # Return results
        #
        return sourceNode, offsetMatrix

    def getTargetInput(self):
        """
        Evaluates the active selection to return the target input.
        Please be aware that bounding boxes are returned in world space!

        :rtype: Tuple[fntransform.FnTransform, transformationmatrix.TransformationMatrix]
        """

        # Get selection list
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('getTargetInput() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        targetNode = fntransform.FnTransform()
        success = targetNode.trySetObject(selection[0])

        if not success:

            raise TypeError('getTargetInput() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = targetNode.worldMatrix()
        offsetMatrix = transformationmatrix.TransformationMatrix()

        if self.targetType == 0:  # Minimum

            boundingBox = targetNode.boundingBox()
            translateMatrix = transformationmatrix.TransformationMatrix(row4=boundingBox.min)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        elif self.targetType == 1:  # Center

            boundingBox = targetNode.boundingBox()
            centerPoint = (boundingBox.min * 0.5) + (boundingBox.max * 0.5)
            translateMatrix = transformationmatrix.TransformationMatrix(row4=centerPoint)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        elif self.targetType == 2:  # Pivot Point

            pass

        elif self.targetType == 3:  # Maximum

            boundingBox = targetNode.boundingBox()
            translateMatrix = transformationmatrix.TransformationMatrix(row4=boundingBox.max)

            offsetMatrix = (translateMatrix * worldMatrix.inverse()).translationPart()

        else:

            pass

        # Return results
        #
        return targetNode, offsetMatrix

    def apply(self, preserveChildren=False, freezeTransform=False):
        """
        Aligns the active selection.
        The selection order consisting of the source to copy from followed by the target to copy to.

        :type preserveChildren: bool
        :type freezeTransform: bool
        :rtype: None
        """

        # Try and evaluate selection
        #
        try:

            # Get source and target objects
            #
            sourceNode, sourceOffsetMatrix = self.getSourceInput()
            targetNode, targetOffsetMatrix = self.getTargetInput()

            log.info(f'Copying from: {sourceNode.name()}, pasting to {targetNode.name()}')

            # Calculate source transform in target parent space
            # Don't forget to include the offset matrices!
            #
            sourceWorldMatrix = sourceNode.worldMatrix()
            targetParentInverseMatrix = targetNode.parentInverseMatrix()

            targetMatrix = (targetOffsetMatrix * (sourceOffsetMatrix * sourceWorldMatrix) * targetParentInverseMatrix)

            # Copy transform matrix
            #
            skipTranslateX, skipTranslateY, skipTranslateZ = (not x for x in self.matchTranslate())
            skipRotateX, skipRotateY, skipRotateZ = (not x for x in self.matchRotate())
            skipScaleX, skipScaleY, skipScaleZ = (not x for x in self.matchScale())

            targetNode.snapshot()
            targetNode.setMatrix(
                targetMatrix,
                skipTranslateX=skipTranslateX, skipTranslateY=skipTranslateY, skipTranslateZ=skipTranslateZ,
                skipRotateX=skipRotateX, skipRotateY=skipRotateY, skipRotateZ=skipRotateZ,
                skipScaleX=skipScaleX, skipScaleY=skipScaleY, skipScaleZ=skipScaleZ
            )

            # Check if transform should be frozen
            #
            if freezeTransform:

                targetNode.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                targetNode.assumeSnapshot()

        except TypeError as exception:

            log.warning(exception)
            return
    # endregion

import numpy
import json

from PySide2 import QtCore, QtWidgets, QtGui
from copy import deepcopy
from dcc import fntransform
from dcc.math import matrixmath
from ezalign.abstract import qabstracttab

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QAlignTab(qabstracttab.QAbstractTab):
    """
    Overload of QAbstractTab used to align two transforms.
    """

    # region Dunderscores
    def __init__(self, *args, **kwargs):
        """
        Private method called after a new instance has been created.

        :type parent: QtWidgets.QWidget
        :type f: QtCore.Qt.WindowFlags
        :rtype: None
        """

        # Call parent method
        #
        super(QAlignTab, self).__init__(*args, **kwargs)
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

        self.targetRadioButtonGroup.buttons()[targetType].setChecked(True)
    # endregion

    # region Methods
    def postLoad(self):
        """
        Called after the user interface has been loaded.

        :rtype: None
        """

        self.translateCheckBoxGroup.setId(self.translateXCheckBox, 0)
        self.translateCheckBoxGroup.setId(self.translateYCheckBox, 1)
        self.translateCheckBoxGroup.setId(self.translateZCheckBox, 2)

        self.sourceRadioButtonGroup.setId(self.sourceMinRadioButton, 0)
        self.sourceRadioButtonGroup.setId(self.sourceCenterRadioButton, 1)
        self.sourceRadioButtonGroup.setId(self.sourcePivotRadioButton, 2)
        self.sourceRadioButtonGroup.setId(self.sourceMaxRadioButton, 3)

        self.targetRadioButtonGroup.setId(self.targetMinRadioButton, 0)
        self.targetRadioButtonGroup.setId(self.targetCenterRadioButton, 1)
        self.targetRadioButtonGroup.setId(self.targetPivotRadioButton, 2)
        self.targetRadioButtonGroup.setId(self.targetMaxRadioButton, 3)

        self.rotateCheckBoxGroup.setId(self.rotateXCheckBox, 0)
        self.rotateCheckBoxGroup.setId(self.rotateYCheckBox, 1)
        self.rotateCheckBoxGroup.setId(self.rotateZCheckBox, 2)

        self.scaleCheckBoxGroup.setId(self.scaleXCheckBox, 0)
        self.scaleCheckBoxGroup.setId(self.scaleYCheckBox, 1)
        self.scaleCheckBoxGroup.setId(self.scaleZCheckBox, 2)

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
        Returns the match translation flags.

        :rtype: list[bool, bool, bool]
        """

        return [x.isChecked() for x in self.translateCheckBoxGroup.buttons()]

    def setMatchTranslate(self, matchTranslate):
        """
        Updates the match translation flags.

        :type matchTranslate: list[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchTranslate):

            self.translateCheckBoxGroup.button(index).setChecked(match)

    def matchRotate(self):
        """
        Returns the match rotation flags.

        :rtype: list[bool, bool, bool]
        """

        return [x.isChecked() for x in self.rotateCheckBoxGroup.buttons()]

    def setMatchRotate(self, matchRotate):
        """
        Updates the match rotation flags.

        :type matchRotate: list[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchRotate):

            self.rotateCheckBoxGroup.button(index).setChecked(match)

    def matchScale(self):
        """
        Returns the match scale flags.

        :rtype: list[bool, bool, bool]
        """

        return [x.isChecked() for x in self.scaleCheckBoxGroup.buttons()]

    def setMatchScale(self, matchScale):
        """
        Updates the match scale flags.

        :type matchScale: list[bool, bool, bool]
        :rtype: None
        """

        for (index, match) in enumerate(matchScale):

            self.scaleCheckBoxGroup.button(index).setChecked(match)

    def evaluateSource(self):
        """
        Evaluates the active selection to return the source input.
        Please be aware that bounding boxes are returned in world space!

        :rtype: fntransform.FnTransform, numpy.matrix
        """

        # Get selection list
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('evaluateSource() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        source = selection[0]

        fnTransform = fntransform.FnTransform()
        success = fnTransform.trySetObject(source)

        if not success:

            raise TypeError('evaluateSource() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = fnTransform.worldMatrix()
        offsetMatrix = deepcopy(matrixmath.IDENTITY_MATRIX)

        if self.sourceType == 0:  # Minimum

            boundingBox = fnTransform.boundingBox()
            minPoint = numpy.array(boundingBox[0])
            translateMatrix = matrixmath.createTranslateMatrix(minPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        elif self.sourceType == 1:  # Center

            boundingBox = fnTransform.boundingBox()
            centerPoint = (numpy.array(boundingBox[0]) * 0.5) + (numpy.array(boundingBox[1]) * 0.5)
            translateMatrix = matrixmath.createTranslateMatrix(centerPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        elif self.sourceType == 2:  # Pivot Point

            pass

        elif self.sourceType == 3:  # Maximum

            boundingBox = fnTransform.boundingBox()
            maxPoint = numpy.array(boundingBox[1])
            translateMatrix = matrixmath.createTranslateMatrix(maxPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        else:

            pass

        # Return results
        #
        return fnTransform, offsetMatrix

    def evaluateTarget(self):
        """
        Evaluates the active selection to return the target input.
        Please be aware that bounding boxes are returned in world space!

        :rtype: fntransform.FnTransform, numpy.matrix
        """

        # Get selection list
        #
        selection = self.scene.getActiveSelection()
        selectionCount = len(selection)

        if selectionCount != 2:

            raise TypeError('evaluateTarget() expects to 2 selected nodes!')

        # Attach source object to function set
        #
        target = selection[1]

        fnTransform = fntransform.FnTransform()
        success = fnTransform.trySetObject(target)

        if not success:

            raise TypeError('evaluateTarget() expects a transform node!')

        # Evaluate source type for offset matrix
        #
        worldMatrix = fnTransform.worldMatrix()
        offsetMatrix = deepcopy(matrixmath.IDENTITY_MATRIX)

        if self.targetType == 0:  # Minimum

            boundingBox = fnTransform.boundingBox()
            minPoint = numpy.array(boundingBox[0])
            translateMatrix = matrixmath.createTranslateMatrix(minPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        elif self.targetType == 1:  # Center

            boundingBox = fnTransform.boundingBox()
            centerPoint = (numpy.array(boundingBox[0]) * 0.5) + (numpy.array(boundingBox[1]) * 0.5)
            translateMatrix = matrixmath.createTranslateMatrix(centerPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        elif self.targetType == 2:  # Pivot Point

            pass

        elif self.targetType == 3:  # Maximum

            boundingBox = fnTransform.boundingBox()
            maxPoint = numpy.array(boundingBox[1])
            translateMatrix = matrixmath.createTranslateMatrix(maxPoint)

            offsetMatrix = matrixmath.decomposeMatrix((translateMatrix * worldMatrix.I))[0]

        else:

            pass

        # Return results
        #
        return fnTransform, offsetMatrix

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
            fnSource, sourceOffsetMatrix = self.evaluateSource()
            fnTarget, targetOffsetMatrix = self.evaluateTarget()

            log.info('Copying from: %s, pasting to %s' % (fnSource.name(), fnTarget.name()))

            # Calculate source transform in target parent space
            # Don't forget to include the offset matrices!
            #
            sourceWorldMatrix = fnSource.worldMatrix()
            targetParentInverseMatrix = fnTarget.parentInverseMatrix()

            targetMatrix = targetOffsetMatrix * ((sourceOffsetMatrix * sourceWorldMatrix) * targetParentInverseMatrix)

            # Copy transform matrix
            #
            skipTranslateX, skipTranslateY, skipTranslateZ = (not x for x in self.matchTranslate())
            skipRotateX, skipRotateY, skipRotateZ = (not x for x in self.matchRotate())
            skipScaleX, skipScaleY, skipScaleZ = (not x for x in self.matchScale())

            fnTarget.snapshot()
            fnTarget.setMatrix(
                targetMatrix,
                skipTranslateX=skipTranslateX, skipTranslateY=skipTranslateY, skipTranslateZ=skipTranslateZ,
                skipRotateX=skipRotateX, skipRotateY=skipRotateY, skipRotateZ=skipRotateZ,
                skipScaleX=skipScaleX, skipScaleY=skipScaleY, skipScaleZ=skipScaleZ
            )

            # Check if transform should be frozen
            #
            if freezeTransform:

                fnTarget.freezeTransform()

            # Check if children should be preserved
            #
            if preserveChildren:

                fnTarget.assumeSnapshot()

        except TypeError as exception:

            log.warning(exception)
            return
    # endregion

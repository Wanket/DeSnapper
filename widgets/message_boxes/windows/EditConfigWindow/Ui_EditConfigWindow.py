# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/windows/EditConfigWindow/EditConfigWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditConfigWindow(object):
    def setupUi(self, EditConfigWindow):
        EditConfigWindow.setObjectName("EditConfigWindow")
        EditConfigWindow.resize(194, 88)
        self.gridLayout = QtWidgets.QGridLayout(EditConfigWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.configSettingsWidget = ConfigSettingsWidget(EditConfigWindow)
        self.configSettingsWidget.setObjectName("configSettingsWidget")
        self.gridLayout.addWidget(self.configSettingsWidget, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editPushButton = QtWidgets.QPushButton(EditConfigWindow)
        self.editPushButton.setObjectName("editPushButton")
        self.horizontalLayout.addWidget(self.editPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(EditConfigWindow)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.baseInfoLabel = QtWidgets.QLabel(EditConfigWindow)
        self.baseInfoLabel.setObjectName("baseInfoLabel")
        self.gridLayout.addWidget(self.baseInfoLabel, 0, 0, 1, 2)

        self.retranslateUi(EditConfigWindow)
        self.cancelPushButton.clicked.connect(EditConfigWindow.close)
        QtCore.QMetaObject.connectSlotsByName(EditConfigWindow)

    def retranslateUi(self, EditConfigWindow):
        _translate = QtCore.QCoreApplication.translate
        EditConfigWindow.setWindowTitle(_translate("EditConfigWindow", "Edit config"))
        self.editPushButton.setText(_translate("EditConfigWindow", "Edit"))
        self.cancelPushButton.setText(_translate("EditConfigWindow", "Cancel"))
        self.baseInfoLabel.setText(_translate("EditConfigWindow", "Editing config "))
from widgets.ConfigSettingsWidget.ConfigSettingsWidget import ConfigSettingsWidget

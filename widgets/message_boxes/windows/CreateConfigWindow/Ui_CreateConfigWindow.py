# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/windows/CreateConfigWindow/CreateConfigWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateConfigWindow(object):
    def setupUi(self, CreateConfigWindow):
        CreateConfigWindow.setObjectName("CreateConfigWindow")
        CreateConfigWindow.resize(303, 146)
        self.gridLayout = QtWidgets.QGridLayout(CreateConfigWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(CreateConfigWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.volumeComboBox = QtWidgets.QComboBox(CreateConfigWindow)
        self.volumeComboBox.setObjectName("volumeComboBox")
        self.gridLayout.addWidget(self.volumeComboBox, 0, 1, 1, 1)
        self.configSettingsWidget = ConfigSettingsWidget(CreateConfigWindow)
        self.configSettingsWidget.setObjectName("configSettingsWidget")
        self.gridLayout.addWidget(self.configSettingsWidget, 3, 0, 1, 4)
        self.templateGroupBox = QtWidgets.QGroupBox(CreateConfigWindow)
        self.templateGroupBox.setCheckable(True)
        self.templateGroupBox.setChecked(False)
        self.templateGroupBox.setObjectName("templateGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.templateGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.templateComboBox = QtWidgets.QComboBox(self.templateGroupBox)
        self.templateComboBox.setObjectName("templateComboBox")
        self.verticalLayout.addWidget(self.templateComboBox)
        self.gridLayout.addWidget(self.templateGroupBox, 0, 3, 2, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.createPushButton = QtWidgets.QPushButton(CreateConfigWindow)
        icon = QtGui.QIcon.fromTheme("dialog-ok")
        self.createPushButton.setIcon(icon)
        self.createPushButton.setObjectName("createPushButton")
        self.horizontalLayout.addWidget(self.createPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(CreateConfigWindow)
        icon = QtGui.QIcon.fromTheme("dialog-cancel")
        self.cancelPushButton.setIcon(icon)
        self.cancelPushButton.setDefault(True)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(13, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.configNameLineEdit = QtWidgets.QLineEdit(CreateConfigWindow)
        self.configNameLineEdit.setObjectName("configNameLineEdit")
        self.gridLayout.addWidget(self.configNameLineEdit, 1, 0, 1, 3)

        self.retranslateUi(CreateConfigWindow)
        self.cancelPushButton.clicked.connect(CreateConfigWindow.close)
        self.templateGroupBox.clicked['bool'].connect(self.configSettingsWidget.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(CreateConfigWindow)

    def retranslateUi(self, CreateConfigWindow):
        _translate = QtCore.QCoreApplication.translate
        CreateConfigWindow.setWindowTitle(_translate("CreateConfigWindow", "Create config"))
        self.label.setText(_translate("CreateConfigWindow", "Volume"))
        self.templateGroupBox.setTitle(_translate("CreateConfigWindow", "Use template"))
        self.createPushButton.setText(_translate("CreateConfigWindow", "Create"))
        self.cancelPushButton.setText(_translate("CreateConfigWindow", "Cancel"))
        self.configNameLineEdit.setPlaceholderText(_translate("CreateConfigWindow", "Config name"))
from widgets.ConfigSettingsWidget.ConfigSettingsWidget import ConfigSettingsWidget

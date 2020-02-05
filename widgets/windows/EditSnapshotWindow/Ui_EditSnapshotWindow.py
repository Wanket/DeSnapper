# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/windows/EditSnapshotWindow/EditSnapshotWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditSnapshotWindow(object):
    def setupUi(self, EditSnapshotWindow):
        EditSnapshotWindow.setObjectName("EditSnapshotWindow")
        EditSnapshotWindow.resize(442, 340)
        self.gridLayout = QtWidgets.QGridLayout(EditSnapshotWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(EditSnapshotWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cleanupTypeComboBox = QtWidgets.QComboBox(EditSnapshotWindow)
        self.cleanupTypeComboBox.setObjectName("cleanupTypeComboBox")
        self.cleanupTypeComboBox.addItem("")
        self.cleanupTypeComboBox.addItem("")
        self.cleanupTypeComboBox.addItem("")
        self.cleanupTypeComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.cleanupTypeComboBox)
        spacerItem = QtWidgets.QSpacerItem(288, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.descriptionLineEdit = QtWidgets.QLineEdit(EditSnapshotWindow)
        self.descriptionLineEdit.setObjectName("descriptionLineEdit")
        self.gridLayout.addWidget(self.descriptionLineEdit, 2, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(EditSnapshotWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.userDataTableWidget = QtWidgets.QTableWidget(EditSnapshotWindow)
        self.userDataTableWidget.setObjectName("userDataTableWidget")
        self.userDataTableWidget.setColumnCount(2)
        self.userDataTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.userDataTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.userDataTableWidget.setHorizontalHeaderItem(1, item)
        self.userDataTableWidget.horizontalHeader().setMinimumSectionSize(200)
        self.userDataTableWidget.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.userDataTableWidget, 4, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(248, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.editPushButton = QtWidgets.QPushButton(EditSnapshotWindow)
        icon = QtGui.QIcon.fromTheme("dialog-ok")
        self.editPushButton.setIcon(icon)
        self.editPushButton.setObjectName("editPushButton")
        self.horizontalLayout.addWidget(self.editPushButton)
        self.pushButton_2 = QtWidgets.QPushButton(EditSnapshotWindow)
        icon = QtGui.QIcon.fromTheme("dialog-cancel")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 2)

        self.retranslateUi(EditSnapshotWindow)
        self.pushButton_2.clicked.connect(EditSnapshotWindow.close)
        QtCore.QMetaObject.connectSlotsByName(EditSnapshotWindow)

    def retranslateUi(self, EditSnapshotWindow):
        _translate = QtCore.QCoreApplication.translate
        EditSnapshotWindow.setWindowTitle(_translate("EditSnapshotWindow", "Edit snapshot"))
        self.label_3.setText(_translate("EditSnapshotWindow", "Cleanup type"))
        self.cleanupTypeComboBox.setItemText(0, _translate("EditSnapshotWindow", "None"))
        self.cleanupTypeComboBox.setItemText(1, _translate("EditSnapshotWindow", "Number"))
        self.cleanupTypeComboBox.setItemText(2, _translate("EditSnapshotWindow", "Timeline"))
        self.cleanupTypeComboBox.setItemText(3, _translate("EditSnapshotWindow", "Empty pre post"))
        self.descriptionLineEdit.setPlaceholderText(_translate("EditSnapshotWindow", "Description"))
        self.label_4.setText(_translate("EditSnapshotWindow", "User data"))
        item = self.userDataTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("EditSnapshotWindow", "Key"))
        item = self.userDataTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("EditSnapshotWindow", "Value"))
        self.editPushButton.setText(_translate("EditSnapshotWindow", "Edit"))
        self.pushButton_2.setText(_translate("EditSnapshotWindow", "Cancel"))

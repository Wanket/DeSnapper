# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/windows/MainWindow/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.snapshotsTreeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.snapshotsTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.snapshotsTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.snapshotsTreeWidget.setRootIsDecorated(False)
        self.snapshotsTreeWidget.setItemsExpandable(False)
        self.snapshotsTreeWidget.setObjectName("snapshotsTreeWidget")
        self.verticalLayout_3.addWidget(self.snapshotsTreeWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.configsListWidget = QtWidgets.QListWidget(self.dockWidgetContents)
        self.configsListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.configsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.configsListWidget.setObjectName("configsListWidget")
        self.verticalLayout.addWidget(self.configsListWidget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.userDataDockWidget = QtWidgets.QDockWidget(MainWindow)
        self.userDataDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.userDataDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.userDataDockWidget.setObjectName("userDataDockWidget")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.userDataTableWidget = QtWidgets.QTableWidget(self.dockWidgetContents_2)
        self.userDataTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.userDataTableWidget.setObjectName("userDataTableWidget")
        self.userDataTableWidget.setColumnCount(2)
        self.userDataTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.userDataTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.userDataTableWidget.setHorizontalHeaderItem(1, item)
        self.userDataTableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.userDataTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.userDataTableWidget)
        self.userDataDockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.userDataDockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.configsListWidget, self.snapshotsTreeWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DeSnapper"))
        self.snapshotsTreeWidget.headerItem().setText(0, _translate("MainWindow", "Type"))
        self.snapshotsTreeWidget.headerItem().setText(1, _translate("MainWindow", "Number"))
        self.snapshotsTreeWidget.headerItem().setText(2, _translate("MainWindow", "Pre snapshot number"))
        self.snapshotsTreeWidget.headerItem().setText(3, _translate("MainWindow", "Date"))
        self.snapshotsTreeWidget.headerItem().setText(4, _translate("MainWindow", "User"))
        self.snapshotsTreeWidget.headerItem().setText(5, _translate("MainWindow", "Cleanup"))
        self.snapshotsTreeWidget.headerItem().setText(6, _translate("MainWindow", "Description"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Configs"))
        self.userDataDockWidget.setWindowTitle(_translate("MainWindow", "User data"))
        item = self.userDataTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Key"))
        item = self.userDataTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))

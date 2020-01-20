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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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

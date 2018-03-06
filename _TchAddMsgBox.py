# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_TchAddMsgBox.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TchAddMsgBox(object):
    def setupUi(self, TchAddMsgBox):
        TchAddMsgBox.setObjectName("TchAddMsgBox")
        TchAddMsgBox.resize(422, 210)
        TchAddMsgBox.setToolTip("")
        self.layoutWidget = QtWidgets.QWidget(TchAddMsgBox)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 341, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.TchAddMsgBoxAssilineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.TchAddMsgBoxAssilineEdit.setObjectName("TchAddMsgBoxAssilineEdit")
        self.horizontalLayout_2.addWidget(self.TchAddMsgBoxAssilineEdit)
        self.layoutWidget_2 = QtWidgets.QWidget(TchAddMsgBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(40, 110, 341, 23))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.TchAddMsgBoxMajorlineEdit = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.TchAddMsgBoxMajorlineEdit.setObjectName("TchAddMsgBoxMajorlineEdit")
        self.horizontalLayout_3.addWidget(self.TchAddMsgBoxMajorlineEdit)
        self.TchAddAddButton = QtWidgets.QPushButton(TchAddMsgBox)
        self.TchAddAddButton.setGeometry(QtCore.QRect(230, 160, 71, 28))
        self.TchAddAddButton.setObjectName("TchAddAddButton")
        self.TchAddCloseButton = QtWidgets.QPushButton(TchAddMsgBox)
        self.TchAddCloseButton.setGeometry(QtCore.QRect(310, 160, 71, 28))
        self.TchAddCloseButton.setObjectName("TchAddCloseButton")
        self.layoutWidget_3 = QtWidgets.QWidget(TchAddMsgBox)
        self.layoutWidget_3.setGeometry(QtCore.QRect(40, 70, 341, 23))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.TchAddMsgBoxTNumlineEdit = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.TchAddMsgBoxTNumlineEdit.setObjectName("TchAddMsgBoxTNumlineEdit")
        self.horizontalLayout_4.addWidget(self.TchAddMsgBoxTNumlineEdit)

        self.retranslateUi(TchAddMsgBox)
        QtCore.QMetaObject.connectSlotsByName(TchAddMsgBox)

    def retranslateUi(self, TchAddMsgBox):
        _translate = QtCore.QCoreApplication.translate
        TchAddMsgBox.setWindowTitle(_translate("TchAddMsgBox", "Dialog"))
        self.label.setText(_translate("TchAddMsgBox", "添加题目"))
        self.TchAddMsgBoxAssilineEdit.setToolTip(_translate("TchAddMsgBox", "<html><head/><body><p>添加题目，如果为空则不添加题目！</p></body></html>"))
        self.TchAddMsgBoxAssilineEdit.setStatusTip(_translate("TchAddMsgBox", "添加题目，为空则不添加"))
        self.label_2.setText(_translate("TchAddMsgBox", "添加专业"))
        self.TchAddMsgBoxMajorlineEdit.setToolTip(_translate("TchAddMsgBox", "<html><head/><body><p>为空则不添加专业名称！</p></body></html>"))
        self.TchAddMsgBoxMajorlineEdit.setStatusTip(_translate("TchAddMsgBox", "为空则不添加专业名称！"))
        self.TchAddAddButton.setText(_translate("TchAddMsgBox", "添加"))
        self.TchAddCloseButton.setText(_translate("TchAddMsgBox", "取消"))
        self.label_3.setText(_translate("TchAddMsgBox", "该题最大可容纳小组数量"))
        self.TchAddMsgBoxTNumlineEdit.setToolTip(_translate("TchAddMsgBox", "<html><head/><body><p align=\"justify\">在未输入题目之前该框被锁定，输入范围为0-255</p></body></html>"))
        self.TchAddMsgBoxTNumlineEdit.setStatusTip(_translate("TchAddMsgBox", "可为空，但是在没有输入题目的情况下，该输入框输入无效"))


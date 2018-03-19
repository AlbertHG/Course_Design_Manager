from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox

import MySQLite3Util
from Models import *
from _StuAddMsgBox import Ui_StuAddMsgBox
from _TchAddMsgBox import Ui_TchAddMsgBox


class TchAddMsgBox(object):
    """教师添加信息窗口封装类，"""

    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        window = Ui_TchAddMsgBox()
        window.setupUi(self.dialog)

        # 只显示关闭按钮，也就是右上角只有一个×
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 设置窗口的标题
        self.dialog.setWindowTitle('添加课程的题目或者专业名')
        # 禁止调整窗口大小
        self.dialog.setFixedSize(self.dialog.width(), self.dialog.height())

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('iconLibrary/icon1.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        # 定义界面得各种输入框，从_TchAddMsgBox复制过来
        self.TchAddMsgBoxAssilineEdit = window.TchAddMsgBoxAssilineEdit
        self.TchAddMsgBoxTNumlineEdit = window.TchAddMsgBoxTNumlineEdit
        self.TchAddMsgBoxMajorlineEdit = window.TchAddMsgBoxMajorlineEdit

        self.TchAddAddButton = window.TchAddAddButton
        self.TchAddCloseButton = window.TchAddCloseButton
        # 给按钮绑定监听器
        self.TchAddAddButton.clicked.connect(self.tchAddAddButtonClicked)
        self.TchAddCloseButton.clicked.connect(self.dialog.close)

        # 设置该输入框只能输入0-255范围数字
        self.TchAddMsgBoxTNumlineEdit.setValidator(
            QRegExpValidator(QRegExp('^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$')))
        # 初始化“该题最大可容纳小组数量”输入框无法输入
        self.TchAddMsgBoxTNumlineEdit.setReadOnly(True)
        self.TchAddMsgBoxAssilineEdit.editingFinished.connect(self.onFun)

    def onFun(self):
        """
        实现功能：“该题最大可容纳小组数量”输入框受到“添加题目”输入框限制
            1、若“添加题目”输入框里边没有内容，则设置“该题最大可容纳小组数量”输入框为只读，即无法在该框输入内容
            2、否则设置“该题最大可容纳小组数量”输入框为读写，即可以在该框输入内容
        :return:
        """
        if self.TchAddMsgBoxAssilineEdit.text().strip() == '':
            print('1')
            self.TchAddMsgBoxTNumlineEdit.setReadOnly(True)
            # self.TchAddMsgBoxTNumlineEdit.setEnabled(False)
        else:
            print('2')
            self.TchAddMsgBoxTNumlineEdit.setReadOnly(False)
            # self.TchAddMsgBoxTNumlineEdit.setEnabled(True)

    # 点击“确定添加”按钮时要完成的逻辑
    def tchAddAddButtonClicked(self):
        """这个动作，应该是这样的：点击确认，并进行输入框的文字获取：
            1、题目有输入：
                i、人数限制有输入。
                ii、人数限制无输入，不限制每个课设题目的小组数目限制
            2、题目无输入：
                i、人数限制无输入
                ii、人数限制有输入，则弹出警告窗，提示：题目为空请先键入题目内容
            3、专业有输入
            4、专业无输入,则忽略该输入框
            5、若全部输入框都为空，则点击添加按钮弹出警告窗
        """
        ass = self.TchAddMsgBoxAssilineEdit.text()
        max_num = self.TchAddMsgBoxTNumlineEdit.text()
        maj = self.TchAddMsgBoxMajorlineEdit.text()
        msg = ''
        if ass.strip() == '' and maj.strip() == '':
            QMessageBox.warning(self.dialog, "禁止访问", "无输入内容，提交被终止！", QMessageBox.Yes)
        elif MySQLite3Util.query_some_by_condition(Assignments, 'AssName', ass.strip()):
            QMessageBox.warning(self.dialog, "禁止访问", "数据库已存在改题目，请重新输入！", QMessageBox.Yes)
        else:
            msg = '课设题目：{}\n'.format(ass) + '可允许最大小组数：{}\n'.format(max_num) + '添加专业名为：{}'.format(maj)
            reply = QMessageBox.question(self.dialog, '请确认信息', msg, QMessageBox.Yes | QMessageBox.No)
            if QMessageBox.Yes == reply:
                if ass.strip():
                    assi = Assignments()
                    assi.AssName = ass
                    if max_num.strip():
                        assi.MaxCount = max_num
                    MySQLite3Util.add_one_msg(assi)
                if maj.strip():
                    major = Majors()
                    major.MajorName = maj
                    MySQLite3Util.add_one_msg(major)
                self.clear_1()

    def show(self):
        self.dialog.show()

    def clear_1(self):
        """
        清空数据
        :return:
        """
        self.TchAddMsgBoxTNumlineEdit.setText('')
        self.TchAddMsgBoxMajorlineEdit.setText('')
        self.TchAddMsgBoxAssilineEdit.setText('')


class StuAddMsgBox(object):
    """学生添加信息窗口封装类，"""
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        window = Ui_StuAddMsgBox()
        window.setupUi(self.dialog)

        # 只显示关闭按钮，也就是右上角只有一个×
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 设置窗口的标题
        self.dialog.setWindowTitle('添加小组')
        # 禁止调整窗口大小
        self.dialog.setFixedSize(self.dialog.width(), self.dialog.height())

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('iconLibrary/icon2.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        # 定义界面得各种输入框，从_StuAddMsgBox复制过来
        self.AssicomboBox = window.AssicomboBox
        self.MsgBoxTeamNamelineEdit = window.MsgBoxTeamNamelineEdit

        self.MajorcomboBox_1 = window.MajorcomboBox_1
        self.MajorcomboBox_2 = window.MajorcomboBox_2
        self.MajorcomboBox_3 = window.MajorcomboBox_3
        self.MajorcomboBox_4 = window.MajorcomboBox_4
        self.MajorcomboBox_5 = window.MajorcomboBox_5
        self.MajorcomboBox_6 = window.MajorcomboBox_6

        self.MsgBoxNamelineEdit_1 = window.MsgBoxNamelineEdit_1
        self.MsgBoxNamelineEdit_2 = window.MsgBoxNamelineEdit_2
        self.MsgBoxNamelineEdit_3 = window.MsgBoxNamelineEdit_3
        self.MsgBoxNamelineEdit_4 = window.MsgBoxNamelineEdit_4
        self.MsgBoxNamelineEdit_5 = window.MsgBoxNamelineEdit_5
        self.MsgBoxNamelineEdit_6 = window.MsgBoxNamelineEdit_6

        self.MsgBoxNumlineEdit_1 = window.MsgBoxNumlineEdit_1
        self.MsgBoxNumlineEdit_2 = window.MsgBoxNumlineEdit_2
        self.MsgBoxNumlineEdit_3 = window.MsgBoxNumlineEdit_3
        self.MsgBoxNumlineEdit_4 = window.MsgBoxNumlineEdit_4
        self.MsgBoxNumlineEdit_5 = window.MsgBoxNumlineEdit_5
        self.MsgBoxNumlineEdit_6 = window.MsgBoxNumlineEdit_6

        self.StuAddOkButton = window.StuAddOkButton
        self.StuAddCloseButton = window.StuAddCloseButton
        # 给按钮绑定监听器
        self.StuAddOkButton.clicked.connect(self.onStuAddOk)
        self.StuAddCloseButton.clicked.connect(self.dialog.close)

        assi_lists = MySQLite3Util.query_all(Assignments)
        for assi_list in assi_lists:
            self.AssicomboBox.addItem(assi_list.AssName)
        # currentIndexChanged方法实现当当前列表的索引发生改变的时候，返回一个信号
        self.AssicomboBox.currentIndexChanged.connect(self.AssiBoxhasTest)

        self.MsgBoxTeamNamelineEdit.setEnabled(False)

        maj_lists = MySQLite3Util.query_all(Majors)
        for maj_list in maj_lists:
            self.MajorcomboBox_1.addItem(maj_list.MajorName)
            self.MajorcomboBox_2.addItem(maj_list.MajorName)
            self.MajorcomboBox_3.addItem(maj_list.MajorName)
            self.MajorcomboBox_4.addItem(maj_list.MajorName)
            self.MajorcomboBox_5.addItem(maj_list.MajorName)
            self.MajorcomboBox_6.addItem(maj_list.MajorName)
        self.MajorcomboBox_1.setEnabled(False)
        self.MajorcomboBox_2.setEnabled(False)
        self.MajorcomboBox_3.setEnabled(False)
        self.MajorcomboBox_4.setEnabled(False)
        self.MajorcomboBox_5.setEnabled(False)
        self.MajorcomboBox_6.setEnabled(False)

        self.MsgBoxNamelineEdit_1.setEnabled(False)
        self.MsgBoxNamelineEdit_2.setEnabled(False)
        self.MsgBoxNamelineEdit_3.setEnabled(False)
        self.MsgBoxNamelineEdit_4.setEnabled(False)
        self.MsgBoxNamelineEdit_5.setEnabled(False)
        self.MsgBoxNamelineEdit_6.setEnabled(False)

        self.MsgBoxNumlineEdit_1.setEnabled(False)
        self.MsgBoxNumlineEdit_2.setEnabled(False)
        self.MsgBoxNumlineEdit_3.setEnabled(False)
        self.MsgBoxNumlineEdit_4.setEnabled(False)
        self.MsgBoxNumlineEdit_5.setEnabled(False)
        self.MsgBoxNumlineEdit_6.setEnabled(False)

    def onStuAddOk(self):
        """
        该按钮的逻辑应该是这样的：
            1、首先从下拉菜单中选择数据库中已经存在的题目，（先得获取数据库表信息）
            2、输入老师给定的唯一的小组编号
            3、默认一个小组最多6个人
                i、通过下拉菜单选择数据库中已经存在的专业
                ii、键入姓名，学号
                iii、如果输入信息完整，也就是同时编辑好（专业，学号，姓名）三条，则认为添加成员，若让同一行中任一个框为孔
                    输入框为空，则该行的全部信息会被忽略掉，认为不添加成员
                iiii、点击‘添加’按钮，弹出对话框，对话框文本内容为小组选题，小组成员等信息，目的是让输入者确认信息
                    j、信息无误，点击对话框确认按钮，将信息持久化进数据库
                    jj、信息有误，点击对话框取消按钮，回到上一级窗口修改信息
        :return:
        """
        select_assi = self.AssicomboBox.currentText()

        # 检测到所选题目不为空
        if select_assi.strip():
            # 先根据用户所选的题目去数据库查找改题目是否达到上限也就是判断‘MaxCount=CurrentCount？’
            get_assi = MySQLite3Util.query_one_by_condition(Assignments, 'AssName', select_assi)

            if get_assi.CurrentCount is None:
                current_count = 0
            else:
                current_count = get_assi.CurrentCount

            # 判断该课设题目是否设置了小组数目限制，和判断当前小组数量是否达到上限
            if get_assi.MaxCount is None or get_assi.MaxCount != get_assi.CurrentCount:

                lists = []
                stu_1 = {'maj': self.MajorcomboBox_1.currentText(), 'stu_name': self.MsgBoxNamelineEdit_1.text(),
                         'num': self.MsgBoxNumlineEdit_1.text()}
                lists.append(stu_1)

                stu_2 = {'maj': self.MajorcomboBox_2.currentText(), 'stu_name': self.MsgBoxNamelineEdit_2.text(),
                         'num': self.MsgBoxNumlineEdit_2.text()}
                lists.append(stu_2)

                stu_3 = {'maj': self.MajorcomboBox_3.currentText(), 'stu_name': self.MsgBoxNamelineEdit_3.text(),
                         'num': self.MsgBoxNumlineEdit_3.text()}
                lists.append(stu_3)

                stu_4 = {'maj': self.MajorcomboBox_4.currentText(), 'stu_name': self.MsgBoxNamelineEdit_4.text(),
                         'num': self.MsgBoxNumlineEdit_4.text()}
                lists.append(stu_4)

                stu_5 = {'maj': self.MajorcomboBox_5.currentText(), 'stu_name': self.MsgBoxNamelineEdit_5.text(),
                         'num': self.MsgBoxNumlineEdit_5.text()}
                lists.append(stu_5)

                stu_6 = {'maj': self.MajorcomboBox_6.currentText(), 'stu_name': self.MsgBoxNamelineEdit_6.text(),
                         'num': self.MsgBoxNumlineEdit_6.text()}
                lists.append(stu_6)

                team_name = self.MsgBoxTeamNamelineEdit.text()

                msg = '选定的课设题目是：{}\n老师分配的小组名称是：{}\n小组成员信息：\n'.format(select_assi, team_name)

                # 对该列表倒序迭代，实现“在迭代中删除特定数据”的功能
                for i in range(len(lists) - 1, -1, -1):
                    # 如果监测到该条记录不完整也就是isNull方法返回True,则把该条记录删除
                    if self.isNull(lists[i]):
                        lists.pop(i)
                    else:
                        dict_1 = lists[i]
                        msg += '\t<专业：{}>--<姓名：{}>--<学号：{}>\n'.format(dict_1['maj'], dict_1['stu_name'],
                                                                      dict_1['num'])

                reply = QMessageBox.question(self.dialog, '请确认信息', msg, QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 新建一个team（小组）模型对象
                    team_model = Teams()
                    team_model.TeamName = team_name
                    team_model.AssID = get_assi.ID
                    # 这里应该是插入小组信息，返回小组ID
                    team_id = MySQLite3Util.add_one_msg(team_model)

                    for j in range(len(lists)):
                        # 这个地方负责对学生信息的插入
                        # 新建一个Student(学生）模型对象
                        stu_model = Students()
                        stu_model.StuName = lists[j]['stu_name']
                        stu_model.StuNum = lists[j]['num']
                        stu_model.MajorID = MySQLite3Util.query_one_by_condition(Majors, 'MajorName',
                                                                                 lists[j]['maj'])['ID']
                        stu_model.TeamID = team_id

                        MySQLite3Util.add_one_msg(stu_model)
                    # 这里完成了小组全部人数的插入，应该更新课设题目的当前是小组数量的那个值也就是CurrentCount
                    current_count += 1
                    MySQLite3Util.update_AssiCurrentCount(current_count, select_assi)

                    self.dialog.close()

            else:
                QMessageBox.warning(self.dialog, '', '该课设题目已达到最大数量限制：' +
                                    '{}人\n请选择其他题目！'.format(get_assi.MaxCount),
                                    QMessageBox.Yes)
        else:
            # 若检测到没有选择题目就点击了“添加按钮”
            QMessageBox.warning(self.dialog, '', '未选择任何课设题目，添加操作被终止！', QMessageBox.Yes)

    def AssiBoxhasTest(self):
        """
        实现功能：“题目”下拉框控制窗口其他控件
            1、“题目”下拉框没有获取到内容，则设置窗口其他控件为只读，即无法输入内容
            2、否则设置窗口其他控件为读写，即可以输入内容
        :return:str_1
        """
        str_1 = self.AssicomboBox.currentText()
        if str_1.strip():
            flag = True
        else:
            flag = False

        self.MsgBoxTeamNamelineEdit.setEnabled(flag)

        self.MajorcomboBox_1.setEnabled(flag)
        self.MajorcomboBox_2.setEnabled(flag)
        self.MajorcomboBox_3.setEnabled(flag)
        self.MajorcomboBox_4.setEnabled(flag)
        self.MajorcomboBox_5.setEnabled(flag)
        self.MajorcomboBox_6.setEnabled(flag)

        self.MsgBoxNamelineEdit_1.setEnabled(flag)
        self.MsgBoxNamelineEdit_2.setEnabled(flag)
        self.MsgBoxNamelineEdit_3.setEnabled(flag)
        self.MsgBoxNamelineEdit_4.setEnabled(flag)
        self.MsgBoxNamelineEdit_5.setEnabled(flag)
        self.MsgBoxNamelineEdit_6.setEnabled(flag)

        self.MsgBoxNumlineEdit_1.setEnabled(flag)
        self.MsgBoxNumlineEdit_2.setEnabled(flag)
        self.MsgBoxNumlineEdit_3.setEnabled(flag)
        self.MsgBoxNumlineEdit_4.setEnabled(flag)
        self.MsgBoxNumlineEdit_5.setEnabled(flag)
        self.MsgBoxNumlineEdit_6.setEnabled(flag)

    def isNull(self, my_dict):
        """
        该方法将用于检测学生信息的完整性
            1、一个学生的信息包括专业，姓名和学号
            2、只要有一个为空，则忽略该学生的信息
            3、默认返回False，即不为空，也就是学生信息完整
        :param my_dict:
        :return:
        """
        flag = False
        for each_key in my_dict.keys():
            if str(my_dict[each_key]).strip() == '':
                flag = True
                break
        return flag

    def show(self):
        self.dialog.show()


# 没有机会使用，先写在这里以防以后有用
class MyComboBox(QtWidgets.QComboBox):

    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)

    """
    重载ComboBox的下拉列表点击方法showPopup()
    效果是点击一下下拉框就发出一个信号
    """
    # 这是一个信号

    popup_about_to_be_show = QtCore.pyqtSignal(str)

    def showPopup(self):
        # 将信号发射出去
        self.popup_about_to_be_show.emit()

        QtWidgets.QComboBox.showPopup(self)

    # 使用方法是：self.AssicomboBox.popup_about_to_be_show.connect(self.fun1)
    # AssicomboBox是你自己定义好的ComboBox组件对象，fun1是相应函数（自定义）

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import MySQLite3Util
from AddMsgUI import TchAddMsgBox, StuAddMsgBox
from Models import *
from _mainUI import Ui_MainWindow
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


class MainWindow(object):
    """
    主窗口封装类
    """

    def __init__(self):
        self.dialog = QtWidgets.QMainWindow()
        self.window = Ui_MainWindow()
        self.window.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # 禁止调整窗口大小
        self.dialog.setFixedSize(self.dialog.width(), self.dialog.height())
        self.dialog.setWindowTitle('欢迎使用')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('iconLibrary/icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)

        self.SearchlineEdit = self.window.SearchlineEdit
        # 为搜索输入框绑定快速显示结果监听器,效果是：每次敲入内容都会进行一次响应
        self.SearchlineEdit.textChanged['QString'].connect(self.on_quick_search)
        self.SearchcomboBox = self.window.SearchcomboBox
        self.SearchpushButton = self.window.SearchpushButton
        # 绑定‘搜索’按键监听器
        self.SearchpushButton.clicked.connect(self.on_search)

        # 刷新数据按钮
        self.refreshData = self.window.refresh_data
        self.refreshData.clicked.connect(self.on_refrech_data)

        # “树状图信息展示”框
        self.AllMsgtreeWidget = self.window.AllMsgtreeWidget
        self.AllMsgtreeWidget.clicked.connect(self.get_selected_data)
        self.load_tree_data()

        # 搜索结果展示框
        self.tableWidget = self.window.tableWidget
        # 设置为只读
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 禁止被选中
        self.tableWidget.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        # 隐藏网格线
        self.tableWidget.setShowGrid(False)
        # 隐藏行名
        self.tableWidget.verticalHeader().setVisible(False)

        self.StuName = self.window.StuName
        self.StuNum = self.window.StuNum
        self.StuMajor = self.window.StuMajor

        self.DelStuMsgpushButton = self.window.DelStuMsgpushButton
        # 绑定学生信息框里边的“删除”按钮的按键监听器
        self.DelStuMsgpushButton.clicked.connect(self.on_delete_stu_msg)

        self.TeamName = self.window.TeamName
        self.TeamAssi = self.window.TeamAssi
        self.TeamMember = self.window.TeamMember
        self.TeamVote = self.window.TeamVote
        # 设置该输入框只能输入0-100范围数字
        self.TeamScore = self.window.TeamScore
        self.TeamScore.setValidator(QRegExpValidator(QRegExp('^(?:[1-9]?\d|100)$')))
        self.TeamScore.setEnabled(False)
        # self.set_team_box_enabled(False)

        self.inputScorepushButton = self.window.inputScorepushButton
        # 绑定小组信息框里边的“修改...”按钮的按键监听器
        self.inputScorepushButton.clicked.connect(self.on_input_score)
        self.VoteTeampushButton = self.window.VoteTeampushButton
        # 绑定小组信息框里边的“为他打Call”按钮的按键监听器
        self.VoteTeampushButton.clicked.connect(self.on_vote_team)
        self.DelTeamMsgpushButton = self.window.DelTeamMsgpushButton
        # 绑定小组信息框里边的“删除”按钮的按键监听器
        self.DelTeamMsgpushButton.clicked.connect(self.on_delete_team_msg)

        self.TchAddpushButton = self.window.TchAddpushButton
        # 绑定“老师添加课程信息”按钮的按键监听器
        self.TchAddpushButton.clicked.connect(self.on_tch_add_msg)
        self.StuAddpushButton = self.window.StuAddpushButton
        # 绑定“学生添加分组信息”按钮的按键监听器
        self.StuAddpushButton.clicked.connect(self.on_stu_add_msg)

        self.deleteDBButton = self.window.deleteDBButton
        # 绑定清空数据库按钮的按键监听器
        self.deleteDBButton.clicked.connect(self.on_delete_db)

        self.pre_score = ''

    def get_selected_data(self):
        """
        获取到单击树形图某一属性的值,并显示在主界面上
        :return:
        """
        self.clear_stu_box_msg()
        self.clear_team_box_msg()

        for col in range(3):
            col_text = self.AllMsgtreeWidget.currentItem().text(col)
            if str(col_text).strip() != '':
                table_lists = []
                if col == 0:
                    # 当col等于0时，表示当前选择的是选题列
                    assi, sess = MySQLite3Util.get_first_data(col, col_text)

                    for team in assi.teams:
                        stus = MySQLite3Util.query_some_by_condition(Students, 'TeamID', team.ID)
                        for stu in stus:
                            table_map = {'AssName': assi.AssName, 'TeamName': team.TeamName,
                                         'TeamScore': team.TeamScore,
                                         'VoteNum': team.VoteNum, 'StuName': stu.StuName}
                            table_lists.append(table_map)
                    self.load_table_msg(table_lists)
                    MySQLite3Util.lazy_close(sess)

                elif col == 1:
                    # 当col等于1时，表示当前选择的是小组列
                    # assi_name是该小组所属题目的题目名
                    assi_name = self.AllMsgtreeWidget.currentItem().parent().text(col - 1)
                    teams_1, sess = MySQLite3Util.get_data(col, col_text)
                    for team_1 in teams_1:
                        if assi_name == team_1.assignment.AssName:
                            stus = MySQLite3Util.query_some_by_condition(Students, 'TeamID', team_1.ID)
                            for stu in stus:
                                table_map = {'AssName': assi_name, 'TeamName': team_1.TeamName,
                                             'TeamScore': team_1.TeamScore,
                                             'VoteNum': team_1.VoteNum, 'StuName': stu.StuName}
                                table_lists.append(table_map)
                            self.load_team_box_msg(team_1)
                    self.load_table_msg(table_lists)
                    MySQLite3Util.lazy_close(sess)

                elif col == 2:
                    # 当col等于1时，表示当前选择的是学生信息列
                    team_name = self.AllMsgtreeWidget.currentItem().parent().text(col - 1)
                    assi_name = self.AllMsgtreeWidget.currentItem().parent().parent().text(col - 2)

                    stus, sess = MySQLite3Util.get_data(col, col_text)
                    # 发现同名同姓的人
                    for stu in stus:
                        if team_name == stu.team.TeamName:
                            table_map = {'AssName': assi_name, 'TeamName': team_name,
                                         'TeamScore': stu.team.TeamScore,
                                         'VoteNum': stu.team.VoteNum, 'StuName': stu.StuName}
                            table_lists.append(table_map)
                            self.load_team_box_msg(stu.team)
                            self.load_stu_box_msg(stu)
                    self.load_table_msg(table_lists)
                    MySQLite3Util.lazy_close(sess)

    def on_quick_search(self):
        """
        定义了“搜索输入框”键入文字时的即使相应动作逻辑
        :return:
        """
        print('我是搜索输入框')
        key = self.SearchcomboBox.currentText()
        value = self.SearchlineEdit.text()
        table_lists = []
        if key == '课设题目':
            assi, sess = MySQLite3Util.get_first_data(0, value)
            if assi is not None:
                for team in assi.teams:
                    stus = MySQLite3Util.query_some_by_condition(Students, 'TeamID', team.ID)
                    for stu in stus:
                        table_map = {'AssName': assi.AssName, 'TeamName': team.TeamName,
                                     'TeamScore': team.TeamScore,
                                     'VoteNum': team.VoteNum, 'StuName': stu.StuName}
                        table_lists.append(table_map)
                self.load_table_msg(table_lists)
                MySQLite3Util.lazy_close(sess)
            else:
                self.clear_table_msg()

        elif key == '学生姓名':
            stus, sess = MySQLite3Util.get_data(2, value)
            for stu in stus:
                assi_id = MySQLite3Util.query_one_by_condition(Teams, 'ID', stu.TeamID).AssID
                assi_name = MySQLite3Util.query_one_by_condition(Assignments, 'ID', assi_id).AssName
                table_map = {'AssName': assi_name, 'TeamName': stu.team.TeamName,
                             'TeamScore': stu.team.TeamScore,
                             'VoteNum': stu.team.VoteNum, 'StuName': stu.StuName}
                table_lists.append(table_map)
            self.load_table_msg(table_lists)
            MySQLite3Util.lazy_close(sess)

        elif key == '专业':
            majors, sess = MySQLite3Util.get_data(3, value)
            for major in majors:
                stus = major.students
                for stu in stus:
                    assi_id = MySQLite3Util.query_one_by_condition(Teams, 'ID', stu.TeamID).AssID
                    assi_name = MySQLite3Util.query_one_by_condition(Assignments, 'ID', assi_id).AssName
                    team = MySQLite3Util.query_one_by_condition(Teams, 'ID', stu.TeamID)

                    table_map = {'AssName': assi_name, 'TeamName': team.TeamName,
                                 'TeamScore': team.TeamScore,
                                 'VoteNum': team.VoteNum, 'StuName': stu.StuName}
                    table_lists.append(table_map)
            self.load_table_msg(table_lists)
            MySQLite3Util.lazy_close(sess)

    def on_search(self):
        """
        该方法定义了点击“搜素...”按钮时的响应逻辑
        :return:
        """
        self.on_quick_search()
        print('搜素...')

    def on_delete_stu_msg(self):
        """
        该方法定义了学生信息框里边的点击“删除”按钮时的响应逻辑
        :return:
        """
        print('学生信息框里边的“删除”')
        stu_name = self.StuName.text()
        stu_major = self.StuMajor.text()
        stu_num = self.StuNum.text()
        if stu_num.strip('') and stu_name.strip(''):
            stu = MySQLite3Util.query_one_by_condition(Students, 'StuNum', stu_num)
            if stu is not None:
                msg = '请确认信息：\n\t' + '姓名：' + stu_name + '，学号：' + stu_num + '，专业：' + stu_major
                reply = QMessageBox.question(self.dialog, '该学生信息将被删除', msg, QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    MySQLite3Util.delete_by_id(Students, stu.ID)
                    self.clear_stu_box_msg()
                    self.load_tree_data()
                    self.clear_table_msg()
                    self.clear_team_box_msg()

    def on_input_score(self):
        """
        该方法定义了小组信息框里边的点击“录入成绩”按钮时的响应逻辑
        :return:
        """
        print('组信息框里边的“修改...”')

        button_text = self.inputScorepushButton.text()
        if button_text == '录入成绩':
            self.pre_score = self.TeamScore.text().strip('')
            self.TeamScore.setEnabled(True)
            self.inputScorepushButton.setText('确认？')
        elif button_text == '确认？':
            now_score = self.TeamScore.text()
            self.inputScorepushButton.setText('录入成绩')
            if now_score.strip('') != self.pre_score:
                # 将成绩更新进去
                team_name = self.TeamName.text()
                if team_name.strip(''):
                    assi_name = self.TeamAssi.text()
                    teams, sess = MySQLite3Util.get_data(1, team_name)
                    for team in teams:
                        if team.assignment.AssName == assi_name:
                            MySQLite3Util.update_team_score(team.ID, now_score)
                    MySQLite3Util.lazy_close(sess)
                else:
                    self.TeamScore.setText('')
            self.TeamScore.setEnabled(False)

    def on_vote_team(self):
        """
        该方法定义了小组信息框里边的点击“为他打call”按钮时的响应逻辑
        :return:
        """
        print('为他打call')
        team_name = self.TeamName.text().strip('')
        if team_name:
            msg = '确定为小组：<' + team_name + '> 投票？'
            reply = QMessageBox.question(self.dialog, '投票确认', msg, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                assi_name = self.TeamAssi.text()
                team_vote = self.TeamVote.text()
                teams, sess = MySQLite3Util.get_data(1, team_name)
                for team in teams:
                    if team.assignment.AssName == assi_name:
                        vote = team.VoteNum
                        if vote is not None:
                            vote += 1
                        else:
                            vote = 1
                        MySQLite3Util.update_team_vote(team.ID, vote)
                        team_vote = str(vote)
                self.TeamVote.setText(team_vote)

                MySQLite3Util.lazy_close(sess)

    def on_refrech_data(self):
        """
        刷新数据按钮的事件响应
        :return:
        """
        self.load_tree_data()
        self.clear_table_msg()
        self.clear_team_box_msg()
        self.clear_stu_box_msg()

        self.TeamScore.setEnabled(False)
        self.inputScorepushButton.setText('录入成绩')

    def on_delete_team_msg(self):
        """
        该方法定义了小组信息框里边的点击“删除”按钮时的响应逻辑
        :return:
        """
        print('小组信息框里边的“删除”')
        team_name = self.TeamName.text()
        assi_name = self.TeamAssi.text()
        team_member = self.TeamMember.text()
        if team_name.strip(''):
            teams, sess = MySQLite3Util.get_data(1, team_name)
            for team in teams:
                if team.assignment.AssName == assi_name:
                    msg = '请确认信息：\n\t' + '小组名称：' + team_name + '\n\t小组成员：' + team_member
                    reply = QMessageBox.question(self.dialog, '该小组信息将被删除', msg, QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        MySQLite3Util.delete_by_id(Teams, team.ID)
                        self.clear_team_box_msg()
                        self.clear_table_msg()
                        self.load_tree_data()
            MySQLite3Util.lazy_close(sess)

    def on_tch_add_msg(self):
        """
        该方法定义了“老师添加课程信息”按钮时的响应逻辑
        :return:
        """
        print('老师添加课程信息')
        self._newTchAddMsgBox = TchAddMsgBox()
        self._newTchAddMsgBox.show()

        pass

    def on_stu_add_msg(self):
        """
        该方法定义了“学生添加分组信息”按钮时的响应逻辑
        :return:
        """
        print('学生添加分组信息')

        self._newStuAddMsgBox = StuAddMsgBox()
        self._newStuAddMsgBox.show()

    def on_delete_db(self):
        """
        该方法定义了清空数据库按钮的响应逻辑
        :return:
        """
        print('重构数据库')
        reply = QMessageBox.warning(self.dialog, '警告！', '所有数据将被清空！', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            MySQLite3Util.delete_all_table()
            MySQLite3Util.create_db_table()

    def load_tree_data(self):
        """
        将数据库的全部数据以树形图形式加载出来
        :return:
        """
        assi_dir = MySQLite3Util.query_all_for_tree()
        self.AllMsgtreeWidget.setColumnCount(3)
        self.AllMsgtreeWidget.setHeaderLabels(['课设题目', '小组名称', '成员姓名'])
        self.AllMsgtreeWidget.clear()
        if assi_dir is not None:
            for assi_name in assi_dir.keys():

                root_1 = QtWidgets.QTreeWidgetItem(self.AllMsgtreeWidget)
                root_1.setText(0, assi_name)  # 设置根节点名称

                if len(assi_dir[assi_name]) != 0:
                    team_lists = assi_dir[assi_name]
                    for i in range(len(team_lists)):
                        team_dir = team_lists[i]
                        for team_name in team_dir.keys():

                            root_2 = QtWidgets.QTreeWidgetItem(root_1)  # 将root_1作为root_2的父节点
                            root_2.setText(1, team_name)

                            stu_lists = team_dir[team_name]
                            if len(stu_lists) != 0:
                                for j in range(len(stu_lists)):
                                    root_3 = QtWidgets.QTreeWidgetItem(root_2)  # 将root_2作为root_3的父节点
                                    root_3.setText(2, stu_lists[j])

                self.AllMsgtreeWidget.addTopLevelItem(root_1)

    def load_table_msg(self, msg_lists):
        """
        将信息加载到table里边
        :param msg_lists:
        :return:
        """
        self.clear_table_msg()
        col = 0
        if len(msg_lists):
            for msg in msg_lists:
                if msg['TeamScore'] is None:
                    msg['TeamScore'] = ''
                if msg['VoteNum'] is None:
                    msg['VoteNum'] = ''
                self.tableWidget.insertRow(col)
                self.tableWidget.setItem(col, 0, QtWidgets.QTableWidgetItem(str(msg['AssName'])))
                self.tableWidget.setItem(col, 1, QtWidgets.QTableWidgetItem(str(msg['TeamName'])))
                self.tableWidget.setItem(col, 2, QtWidgets.QTableWidgetItem(str(msg['StuName'])))
                self.tableWidget.setItem(col, 3, QtWidgets.QTableWidgetItem(str(msg['TeamScore'])))
                self.tableWidget.setItem(col, 4, QtWidgets.QTableWidgetItem(str(msg['VoteNum'])))
                col += 1

    def load_team_box_msg(self, team):
        """
        将数据库获取到小组信息加载到界面指定位置
        :param team:
        :return:
        """
        if team.VoteNum is None:
            team.VoteNum = ''
        if team.TeamScore is None:
            team.TeamScore = ''
        self.TeamName.setText(str(team.TeamName))
        self.TeamVote.setText(str(team.VoteNum))
        self.TeamScore.setText(str(team.TeamScore))
        assi = MySQLite3Util.query_one_by_condition(Assignments, 'ID', team.AssID).AssName
        self.TeamAssi.setText(str(assi))
        students = team.students
        stu_str = ''
        for student in students:
            stu_str += student.StuName + '、'
        self.TeamMember.setText(str(stu_str))

    def load_stu_box_msg(self, student):
        """
        将数据库获取到学生信息加载到界面指定位置
        :param student:
        :return:
        """
        self.StuName.setText(str(student.StuName))
        self.StuNum.setText(str(student.StuNum))
        stu_major = MySQLite3Util.query_one_by_condition(Majors, 'ID', student.MajorID).MajorName
        self.StuMajor.setText(str(stu_major))

    def clear_table_msg(self):
        """
        清空主界面题目信息展示表中所有内容
        :return:
        """
        row_count = self.tableWidget.rowCount()
        for i in range(row_count - 1, -1, -1):
            self.tableWidget.removeRow(i)

    def clear_team_box_msg(self):
        """
        清空主界面小组信息展示框的内容
        :return:
        """
        self.TeamName.setText('')
        self.TeamAssi.setText('')
        self.TeamVote.setText('')
        self.TeamScore.setText('')
        self.TeamMember.setText('')

    def clear_stu_box_msg(self):
        """
        清空学生信息展示框的内容
        :return:
        """
        self.StuName.setText('')
        self.StuNum.setText('')
        self.StuMajor.setText('')

    def show(self):
        self.dialog.show()

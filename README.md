<h1 align="center">简易课程作业管理工具</h1>

# 目录

* [目录](#目录)
* [1 成员分组和任务分工](#1-成员分组和任务分工)
* [2 设计实现详细说明](#2-设计实现详细说明)
    * [2.1 选题任务详细说明](#21-选题任务详细说明)
    * [设计思路详细描述](#设计思路详细描述)
        * [数据库E-R图](#数据库er图)
        * [数据库字段定义](#数据库字段定义)
        * [逻辑实现和使用](#逻辑实现和使用)
            * [init.pyw运行文件启动程序](#initpyw运行文件启动程序)
            * [调用MainWindow类生成主界面](#调用mainwindow类生成主界面)
            * [老师录入课程相关信息](#老师录入课程相关信息)
            * [学生录入选题和分组](#学生录入选题和分组)
            * [信息检索操作](#信息检索操作)
            * [全局信息展示](#全局信息展示)
            * [分类信息展示](#分类信息展示)
            * [刷新系统](#刷新系统)
            * [删除课程档案](#删除课程档案)
    * [涵盖的知识点](#涵盖的知识点)
    * [代码展示](#代码展示)
        * [mainUI.py](#mainui-py)
        * [AddMsgUI.py](#addmsgui-py)
        * [Models.py](#models-py)
        * [MySQLite3Util.py](#mysqlite3util-py)
        * [其他py文件](#其他py文件)
* [总结](#总结)
* [备注](#备注)
    * [程序文件](#程序文件)
    * [Qt Designer文件](#qt-designer文件)
    * [其余文件](#其余文件)
    * [平台和依赖](#平台和依赖)



# 1 成员分组和任务分工

组员 |任务分工
---------|---------
张三|界面设计
李四|数据库设计
王五|业务逻辑拆分
赵六|业务实现

# 2 设计实现详细说明
## 2.1 选题任务详细说明

设计一个简易课程作业管理系统，使用PyQt编写，将数据存储到数据库吗，提供增删改查操作。
- 管理员可以添加课程内学生和专业信息
- 管理员同时可以添加课程设计题目及其相关信息
- 学生使用系统进行题目选择和组队操作
- 系统提供必要的检索功能
- 系统提供打分和投票功能

## 2.2 设计思路详细描述

### 2.2.1 数据库E-R图
![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/01.png)

### 2.2.2 数据库字段定义

依据上述数据库结构图，其基表的字段定义如下:

*Assignments表*

列名 |类型|允许NULL|备注
---------|---------|---------|---------
ID|INTEGER|False|主键，题目编号
AssName|TEXT|False|题目名称
MaxCount|INTEGER|True|题目的小组容量
CurrentCount|INTEGER|True|当前题目的小组数

*Majors表*

列名 |类型|允许NULL|备注
---------|---------|---------|---------
ID|INTEGER|False|主键，专业编号
MajorName|TEXT|False|专业名称

*Students表*

列名 |类型|允许NULL|备注
---------|---------|---------|---------
ID|INTEGER|False|主键，学生编号
StuName|TEXT|False|学生姓名
StuSex|TEXT|True|学生性别
StuNum|TEXT|False|学生学号
MajorID|INTEGER|True|外键，专业编号
TeamID|INTEGER|True|外键，小组编号

*Teams表*

列名 |类型|允许NULL|备注
---------|---------|---------|---------
ID|INTEGER|False|主键，小组编号
TeamName|TEXT|False|小组名称
TeamScore|INTEGER|True|小组成绩
VoteNum|INTEGER|True|得票数
AssID|INTEGER|True|外键，题目编号

### 2.2.3 逻辑实现和使用

#### 2.2.3.1 init.pyw运行文件启动程序

```python
"""程序启动器"""
if __name__ == '__main__':
    argv = sys.argv
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
```

调用MainWindow类生成主界面

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/02.png)

#### 2.2.3.2 老师录入课程相关信息

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/03.png)

可供输入的类别有三个，分别是：课程题目、该题容量和课程专业。
- 其中题目容量文本框必须在课程题目文本框有内容的情况下才被激活
- 课程专业文本框和其他框互相独立

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/04.png)

#### 2.2.3.3 学生录入选题和分组

1. “题目”下拉框获取数据库关于题目的相关内容
2. 小组名称作为区分同一题目下的不同小组的关键信息
3. 每组小队人数不得超过6人
4. 只有完成填写了专业、姓名和学号的成员信息才会被系统录入

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/05.png)

#### 2.2.3.4 信息检索操作

- 提供快速检索操作：在信息检索框输入内容，被匹配的信息即时呈现在主界面上。
- 信息检索操作提供三类信息检索：课设题目检索，专业检索和学生姓名检索。
- 同时提供搜索按钮，该动作会立即激活检索操作

#### 2.2.3.5 全局信息展示

- 全局信息展示以树的形式展示数据库所有内容

#### 2.2.3.6 分类信息展示

- 题目信息将以表格的形式呈现
- 小组和成员信息将以信息组合框的形式展示
    - 小组和成员信息提供删除操作
    - 小组信息展示框提供成绩录入和投票操作响应

#### 2.2.3.7 刷新系统

即时重置主界面，重新获取数据库数据

#### 2.2.3.8 删除课程档案

档案一旦删除不可恢复。

## 2.3 涵盖的知识点

1. 判断语句的使用
2. 列表，字典等语句的使用
3. 循环结构的应用
4. 自定义函数的应用
5. PyQt界面编程
6. Python数据库操作，ORM应用

## 2.4 代码展示

### 2.4.1 *mainUI.py*:
```python
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
        """
        构造方法
        """
        pass

    def get_selected_data(self):
        """
        获取到单击树形图某一属性的值,并显示在主界面上
        :return:
        """
        pass

    def on_quick_search(self):
        """
        定义了“搜索输入框”键入文字时的即使相应动作逻辑
        :return:
        """
        pass

    def on_search(self):
        """
        该方法定义了点击“搜素...”按钮时的响应逻辑
        :return:
        """
        pass

    def on_delete_stu_msg(self):
        """
        该方法定义了学生信息框里边的点击“删除”按钮时的响应逻辑
        :return:
        """
        pass

    def on_input_score(self):
        """
        该方法定义了小组信息框里边的点击“录入成绩”按钮时的响应逻辑
        :return:
        """
        pass

    def on_vote_team(self):
        """
        该方法定义了小组信息框里边的点击“为他打call”按钮时的响应逻辑
        :return:
        """
        pass

    def on_refrech_data(self):
        """
        刷新数据按钮的事件响应
        :return:
        """
        pass

    def on_delete_team_msg(self):
        """
        该方法定义了小组信息框里边的点击“删除”按钮时的响应逻辑
        :return:
        """
        pass

    def on_tch_add_msg(self):
        """
        该方法定义了“老师添加课程信息”按钮时的响应逻辑
        :return:
        """
        pass

    def on_stu_add_msg(self):
        """
        该方法定义了“学生添加分组信息”按钮时的响应逻辑
        :return:
        """
        pass

    def on_delete_db(self):
        """
        该方法定义了清空数据库按钮的响应逻辑
        :return:
        """
        pass

    def load_tree_data(self):
        """
        将数据库的全部数据以树形图形式加载出来
        :return:
        """
        pass

    def load_table_msg(self, msg_lists):
        """
        将信息加载到table里边
        :param msg_lists:
        :return:
        """
        pass

    def load_team_box_msg(self, team):
        """
        将数据库获取到小组信息加载到界面指定位置
        :param team:
        :return:
        """
        pass

    def load_stu_box_msg(self, student):
        """
        将数据库获取到学生信息加载到界面指定位置
        :param student:
        :return:
        """
        pass

    def clear_table_msg(self):
        """
        清空主界面题目信息展示表中所有内容
        :return:
        """
        pass

    def clear_team_box_msg(self):
        """
        清空主界面小组信息展示框的内容
        :return:
        """
        pass

    def clear_stu_box_msg(self):
        """
        清空学生信息展示框的内容
        :return:
        """
        pass

    def show(self):
        self.dialog.show()
```

### 2.4.2 *AddMsgUI.py*:

```Python
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
        """构造方法"""
        pass

    def onFun(self):
        """
        实现功能：“该题最大可容纳小组数量”输入框受到“添加题目”输入框限制
            1、若“添加题目”输入框里边没有内容，则设置“该题最大可容纳小组数量”输入框为只读，即无法在该框输入内容
            2、否则设置“该题最大可容纳小组数量”输入框为读写，即可以在该框输入内容
        :return:
        """
        pass

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
        pass

    def show(self):
        self.dialog.show()

    def clear_1(self):
        """
        清空数据
        :return:
        """
        pass

class StuAddMsgBox(object):
    """学生添加信息窗口封装类，"""
    def __init__(self):
        """构造方法"""
        pass

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
        pass

    def AssiBoxhasTest(self):
        """
        实现功能：“题目”下拉框控制窗口其他控件
            1、“题目”下拉框没有获取到内容，则设置窗口其他控件为只读，即无法输入内容
            2、否则设置窗口其他控件为读写，即可以输入内容
        :return:str_1
        """
        pass

    def isNull(self, my_dict):
        """
        该方法将用于检测学生信息的完整性
            1、一个学生的信息包括专业，姓名和学号
            2、只要有一个为空，则忽略该学生的信息
            3、默认返回False，即不为空，也就是学生信息完整
        :param my_dict:
        :return:
        """
        pass

    def show(self):
        self.dialog.show()

```

### 2.4.3 *Models.py*:

```python
from sqlalchemy import Column, Integer, TEXT
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()  # <-元类

# ************下列所有类都是基于Base = declarative_base()而存在的，如果使用sqlalchemy的反射机制automap_base()，可以不用定义模型层
# 定义Assignments对象
class Assignments(Base):
    # 表的名字
    __tablename__ = 'Assignments'
    __table_args__ = {'sqlite_autoincrement': True}

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    AssName = Column(TEXT, nullable=False)
    MaxCount = Column(Integer)
    CurrentCount = Column(Integer)

    # 添加关系属性
    # teams变量装载了查询到的属于该Assignment的所有小组（使用AssID外键遍历Teams表，返回teams列表）
    # 加上backref字段的话，则实现在Teams对象上，通过teams1.assignment语句输出查询到的该teams1所属的Assignment集合
    teams = relationship('Teams', backref='assignment')


# 定义Teams对象
class Teams(Base):
    # 表的名字
    __tablename__ = 'Teams'
    __table_args__ = {'sqlite_autoincrement': True}

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    TeamName = Column(TEXT, nullable=False)
    TeamScore = Column(Integer)
    VoteNum = Column(Integer)
    AssID = Column(Integer, ForeignKey('Assignments.ID'))

    students = relationship('Students', backref='team')


# 定义Students对象，该表其实是Teams表和Majors表解除多对多关系的一个关联表
class Students(Base):
    # 表的名字
    __tablename__ = 'Students'
    __table_args__ = {'sqlite_autoincrement': True}

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    StuName = Column(TEXT, nullable=False)
    StuSex = Column(TEXT)
    StuNum = Column(TEXT, nullable=False)

    TeamID = Column(Integer, ForeignKey('Teams.ID'))
    MajorID = Column(Integer, ForeignKey('Majors.ID'))


# 定义Majors对象
class Majors(Base):
    # 表的名字
    __tablename__ = 'Majors'
    __table_args__ = {'sqlite_autoincrement': True}

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    MajorName = Column(TEXT, nullable=False)

    students = relationship('Students', backref='major')

```

### 2.4.4 *MySQLite3Util.py*

```Python
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from Models import *

# 用来初始化数据库连接，创建数据库引擎,echo为True,会打印所有的sql语句，方便调试
engine = create_engine('sqlite:///./Stu.db', echo=False)
# 创建DBSession会话类
DBSession = sessionmaker(bind=engine)

Base_ref = automap_base()
Base_ref.prepare(engine, reflect=True)


def create_db_table():
    """
    创建数据表
    :return:
    """
    pass


def delete_all_table():
    """
    一次性删除全部表
    :return:
    """
    pass


def get_ref_table():
    """
    返回通过sqlalchemy的反射机制获取的数据库表结构
    :return:
    """
    pass


def get_session():
    """
    获取session对象
    :return:
    """
    pass


def add_one_msg(model):
    """
    为数据库添加一条记录
    :param model: 实例对象
    :return:
    """
    pass


def add_some_msg(model):
    """
    一次性添加若干条记录
    :param model:
    :return:
    """
    pass


def query_all(model):
    """
    传入要查询的表名，返回表的所有数据
    :param model: 表名
    :return:
    """
    pass


def query_all_for_tree():
    """
    为构建树状图专门服务的方法
    一次查询所有的课设题目，小组，学生,
    :return:
    """
    pass


def query_some_by_condition(model, column, condition):
    """
    传入表对应的实体类的类名，列名和条件，返回符合的记录
    :param model:表对应的实体类的类名
    :param column:列名
    :param condition:条件
    :return: list
    """
    pass


def query_one_by_condition(model, column, condition):
    """
    传入表对应的实体类的类名，列名和条件，返回符合的第一条记录
    :param model:表对应的实体类的类名
    :param column:列名
    :param condition:条件
    :return:
    """
    pass


def update_team_vote(team_id, vote):
    """
    为指定ID的小组投票
    :param team_id:
    :param vote:
    :return:
    """
    pass


def update_team_score(team_id, score):
    """
    为指定ID的小组修改成绩
    :param team_id:
    :param score:
    :return:
    """
    pass

def update_AssiCurrentCount(new_current_count, assi_name):
    """
    根据条件更新指定表的指定列
    :param new_current_count:
    :param assi_name:
    :return:
    """
    pass


def add_get_generated_key(model):
    """
    新增一条记录并返回主键
    :param model:
    :return:
    """
    pass


def get_first_data(index, value):
    """
    根据树状图双击的获得属性，去数据库找符合条件的第一条记录
    :param index:
    :param name:
    :return:
    """
    pass


def get_data(index, name):
    """
    根据树状图双击的获得属性，去数据库找相关详细信息
    :param index:
    :param name:
    :return:
    """
    pass


def delete_by_id(model, value):
    """
    根据条件删除记录
    :param model:
    :param value:
    :return:
    """
    pass


def lazy_close(session, flag=True):
    """
    延迟关闭会话
    :param session:
    :param flag:
    :return:
    """
    pass

```
### 2.4.5 其他py文件

\_main.py、\_StuAddMsgBox.py、\_TchAddMsgBox为窗口和空间布局模块，此处不做详细说明。

# 3 总结

略

# 4 备注
## 4.1 程序文件

文件名 |注释
---------|---------|
init.pyw|程序入口
_mainUI.py|主窗口界面UI
mainUI.py|主窗口封装类, 实现功能
_StuAddMsgBox.py|学生添加信息界面UI
_TchAddMsgBox.py|教师添加信息界面UI
AddMagUI.py|教师和学生添加信息窗口封装包，实现教师和学生添加信息的逻辑
MySQLite3Util.py|SQLite3数据库操作封装类，实现数据库的操作
Models.py|ORM对象关系映射类
Stu.db|数据库文件

## 4.2 Qt Designer文件
文件名|注释
---------|---------|
_mainUI.ui|主窗口界面UI设计文件
_StuAddMsgBox.ui|学生添加信息界面UI设计文件
_TchAddMsgBox.ui|教师添加信息界面UI设计文件

## 4.3 其余文件

文件名 |注释
---------|---------|
iconLibrary|系统图标库
md_images|README.md文件图片库

## 4.4 平台和依赖

环境 |注释
---------|---------
Python|3.6 x64
PyQt5|Qt界面库 x64
sqlalchemy|数据库操作模块

<h1 align="center">简易课程作业管理工具</h1>

## 成员分组和任务分工


组员 |任务分工
---------|---------
张三|界面设计
李四|数据库设计
王五|业务逻辑拆分
赵六|业务实现

## 设计实现详细说明
### 选题任务详细说明

设计一个简易课程作业管理系统，使用PyQt编写，将数据存储到数据库吗，提供增删改查操作。
- 管理员可以添加课程内学生和专业信息
- 管理员同时可以添加课程设计题目及其相关信息
- 学生使用系统进行题目选择和组队操作
- 系统提供必要的检索功能
- 系统提供打分和投票功能

### 设计思路详细描述

#### 数据库E-R图
![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/01.png)

#### 数据库字段定义

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

#### 逻辑实现和使用

##### init.pyw运行文件启动程序

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

##### 老师录入课程相关信息

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/03.png)

可供输入的类别有三个，分别是：课程题目、该题容量和课程专业。
- 其中题目容量文本框必须在课程题目文本框有内容的情况下才被激活
- 课程专业文本框和其他框互相独立

![](https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/04.png)

##### 学生录入选题和分组

1. “题目”下拉框获取数据库关于题目的相关内容
2. 小组名称作为区分同一题目下的不同小组的关键信息
3. 每组小队人数不得超过6人
4. 只有完成填写了专业、姓名和学号的成员信息才会被系统录入

![](05https://raw.githubusercontent.com/AlbertHG/Course_Design_Manager/master/md_images/05.png)

##### 信息检索操作

- 提供快速检索操作：在信息检索框输入内容，被匹配的信息即时呈现在主界面上。
- 信息检索操作提供三类信息检索：课设题目检索，专业检索和学生姓名检索。
- 同时提供搜索按钮，该动作会立即激活检索操作

##### 全局信息展示

- 全局信息展示以树的形式展示数据库所有内容

##### 分类信息展示

- 题目信息将以表格的形式呈现
- 小组和成员信息将以信息组合框的形式展示
    - 小组和成员信息提供删除操作
    - 小组信息展示框提供成绩录入和投票操作响应

##### 刷新系统

即时重置主界面，重新获取数据库数据

##### 删除课程档案

档案一旦删除不可恢复。


### 涵盖的知识点

1. 判断语句的使用
2. 列表，字典等语句的使用
3. 循环结构的应用
4. 自定义函数的应用
5. PyQt界面编程
6. Python数据库操作，ORM应用

### 代码展示

详见工程项目

### 总结

略

### 备注
#### 程序文件

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

#### Qt Designer文件
文件名|注释
---------|---------|
_mainUI.ui|主窗口界面UI设计文件
_StuAddMsgBox.ui|学生添加信息界面UI设计文件
_TchAddMsgBox.ui|教师添加信息界面UI设计文件

#### 其余文件

文件名 |注释
---------|---------|
iconLibrary|系统图标库
md_images|README.md文件图片库

#### 平台和依赖

环境 |注释
---------|---------
Python|3.6 x64
PyQt5|Qt界面库 x64
sqlalchemy|数据库操作模块



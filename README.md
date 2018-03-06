# Course_Design_Manager
Course design engineering code.
# 配置
### 文件

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

### Qt Designer文件
文件名|注释
---------|---------|
_mainUI.i|主窗口界面UI设计文件
_StuAddMsgBox.ui|学生添加信息界面UI设计文件
_TchAddMsgBox.ui|教师添加信息界面UI设计文件

###平台和依赖

环境 |信息     
---------|---------
Python|3.6 x64
PyQt5|Qt界面库 x64
sqlalchemy|数据库操作模块

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
    # assignment = None


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

    # major = None
    # team = None


# 定义Majors对象
class Majors(Base):
    # 表的名字
    __tablename__ = 'Majors'
    __table_args__ = {'sqlite_autoincrement': True}

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    MajorName = Column(TEXT, nullable=False)

    students = relationship('Students', backref='major')

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
    db_conn = engine.connect()
    db_conn.execute(r'''CREATE TABLE Assignments (
    ID           INTEGER PRIMARY KEY AUTOINCREMENT
                         NOT NULL,
    AssName      TEXT    NOT NULL,
    MaxCount     INTEGER,
    CurrentCount INTEGER
);
''')
    db_conn.execute(r'''CREATE TABLE Majors (
    ID        INTEGER PRIMARY KEY AUTOINCREMENT
                      NOT NULL,
    MajorName TEXT    NOT NULL
);''')
    db_conn.execute(r'''CREATE TABLE Teams (
    ID        INTEGER PRIMARY KEY AUTOINCREMENT
                      NOT NULL,
    TeamName  TEXT    NOT NULL,
    TeamScore INTEGER,
    VoteNum   INTEGER,
    AssID     INTEGER REFERENCES Assignments (ID) ON DELETE CASCADE
);''')
    db_conn.execute(r'''CREATE TABLE Students (
    ID      INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL,
    StuName TEXT    NOT NULL,
    StuSex  TEXT,
    StuNum  TEXT    NOT NULL,
    MajorID INTEGER REFERENCES Majors (ID) ON DELETE CASCADE,
    TeamID  INTEGER REFERENCES Teams (ID) ON DELETE CASCADE
);
''')
    db_conn.close()


def delete_all_table():
    """
    一次性删除全部表
    :return:
    """
    Base.metadata.drop_all(engine)


def get_ref_table():
    """
    返回通过sqlalchemy的反射机制获取的数据库表结构
    :return:
    """
    # 使用反射，加载数据库的表,具体需要访问数据库的哪一张表只需要‘table.表名’即可
    table = Base_ref.classes
    return table


def get_session():
    """
    获取session对象
    :return:
    """
    return DBSession()


def add_one_msg(model):
    """
    为数据库添加一条记录
    :param model: 实例对象
    :return:
    """
    # 获取session对象:
    session = get_session()
    session.add(model)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    result_id = model.ID
    session.close()
    return result_id


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
    session = get_session()
    lists = session.query(model).all()
    # print(lists)
    session.close()
    return lists


def query_all_for_tree():
    """
    为构建树状图专门服务的方法
    一次查询所有的课设题目，小组，学生,
    :return:
    """
    session = get_session()
    assig_lists = session.query(Assignments).all()
    assig_dir = dict()
    for assig_list in assig_lists:
        team_lists = []
        for team_list in assig_list.teams:
            team_dir = {}
            stu_lists = []
            for stu_list in team_list.students:
                stu_lists.append(stu_list.StuName)
            team_dir[team_list.TeamName] = stu_lists
            team_lists.append(team_dir)
        assig_dir[assig_list.AssName] = team_lists

    session.close()
    return assig_dir


def query_some_by_condition(model, column, condition):
    """
    传入表对应的实体类的类名，列名和条件，返回符合的记录
    :param model:表对应的实体类的类名
    :param column:列名
    :param condition:条件
    :return: list
    """
    model_name = model.__name__
    sql_str = 'select * from {} WHERE {} = "{}"'.format(model_name, column, condition)
    session = get_session()
    result = session.execute(sql_str).fetchall()
    session.close()
    return result


def query_one_by_condition(model, column, condition):
    """
    传入表对应的实体类的类名，列名和条件，返回符合的第一条记录
    :param model:表对应的实体类的类名
    :param column:列名
    :param condition:条件
    :return:
    """
    return query_some_by_condition(model, column, condition)[0]


def update_team_vote(team_id, vote):
    """
    为指定ID的小组投票
    :param team_id:
    :param vote:
    :return:
    """
    session = get_session()
    session.query(Teams).filter(Teams.ID == team_id).update(
        {Teams.VoteNum: vote})
    session.commit()
    session.close()


def update_team_score(team_id, score):
    """
    为指定ID的小组修改成绩
    :param team_id:
    :param score:
    :return:
    """
    session = get_session()
    session.query(Teams).filter(Teams.ID == team_id).update(
        {Teams.TeamScore: score})
    session.commit()
    session.close()


def update_AssiCurrentCount(new_current_count, assi_name):
    """
    根据条件更新指定表的指定列
    :param new_current_count:
    :param assi_name:
    :return:
    """
    session = get_session()
    session.query(Assignments).filter(Assignments.AssName == assi_name).update(
        {Assignments.CurrentCount: new_current_count})
    session.commit()
    session.close()


def add_get_generated_key(model):
    """
    新增一条记录并返回主键
    :param model:
    :return:
    """
    # 获取session对象:
    session = get_session()
    session.add(model)
    # 提交即保存到数据库:
    session.commit()
    session.flush()
    # 关闭session:
    session.close()
    return model.ID


def get_first_data(index, value):
    result, session = get_data(index, value)
    if len(result):
        return result[0], session
    else:
        result = None
        return result, session


def get_data(index, name):
    """
    根据树状图双击的获得属性，去数据库找相关详细信息
    :param index:
    :param name:
    :return:
    """
    session = get_session()

    if index == 0:
        # 查询 题目信息
        result = session.query(Assignments).filter(Assignments.AssName == name).all()
    elif index == 1:
        # 查询小组信息
        result = session.query(Teams).filter(Teams.TeamName == name).all()
    elif index == 2:
        # 查询学生讯息
        result = session.query(Students).filter(Students.StuName == name).all()
    elif index == 3:
        # 查询专业信息
        result = session.query(Majors).filter(Majors.MajorName == name).all()
    return result, session


def delete_by_id(model, value):
    """
    根据条件删除记录
    :param model:
    :param value:
    :return:
    """
    session = get_session()
    session.delete(session.query(model).filter_by(ID=value).first())
    session.commit()
    session.close()
    pass


def lazy_close(session, flag=True):
    if flag:
        session.close()
    else:
        print('会话未关闭')

import sqlite3
from flask import flash
from frozen_dir import app_path


def sql(position, type, date, keyword):
    if position == "before":
        sqlcmd = "select * from news where ({}<'{}%' and title like '%{}%')".format(type, date, keyword)
    elif position == "at":
        sqlcmd = "select * from news where ({} like '{}%' and title like '%{}%')".format(type, date, keyword)
    elif position == "after":
        sqlcmd = "select * from news where ({}>'{}%' and title like '%{}%')".format(type, date, keyword)
    try:
        dir = app_path()
        db = sqlite3.connect(dir + r'\RssNews.db')
        cursor = db.cursor()
        process = cursor.execute(sqlcmd)
        result = cursor.fetchall()
        return result
    except sqlite3.OperationalError as e:
        flash('发生错误:{}。第一次查询请先进行信息收集。'.format(e))

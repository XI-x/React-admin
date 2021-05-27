#创建学生单场考试文理总分 #StudentGrade
from flask_csv import send_csv
from pymongo import MongoClient
import cpca
import pandas as pd
import numpy as np
from pandas import DataFrame
from bson.json_util import dumps
#对所有学生信息表excel进行处理并建立数据集合
# 创建连接MongoDB数据库函数
def connection():
    # 1:连接本地MongoDB数据库服务
    conn=MongoClient("localhost")
    # 2:连接本地数据库(bysj)。没有时会自动创建
    db=conn.bysj
    # 3:创建集合
    #set1=db.student_grade
    # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    #第一种直接remove
    # set1.remove(None)
    #第二种remove不好用的时候
    #set1.delete_many({})
    return db
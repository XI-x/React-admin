from operator import ne
from re import sub
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from flask import Flask, request, jsonify, session
import requests
from flask import Blueprint
from bson.json_util import dumps
from operator import itemgetter
from itertools import groupby
from collections import Counter

test_api = Blueprint('test_api', __name__)
one_id = [926,927,928,929,930,934,935,936,937,938]
two_id = [901,902,903,904,905,906,907,908,909,910]
three_id = [916,917,918,919,920,921,922,923,924,925]
# 连接mongodb数据库
client = pymongo.MongoClient("localhost")
# 连接数据库
db = client["bysj"]
# 数据表
demo = db["StudentExamRecord"]
# 将mongodb中的数据读出
#for each in two_id:
@test_api.route("/test",methods=["POST"])
def test():
    demolist2 = []
    for each in two_id:
        user = demo.find({"cla_id":each})
        demolist1 = []
        for each in user:
            demolist1.append(each)
        new_list = sorted(demolist1, key=lambda test:(test["stu_id"],test["exam_sub_id"]),reverse=True) #依据考试时间/考试科目排序
    
        for date, items in groupby(new_list, key=itemgetter('stu_id',"exam_sub_id")):
            demolist3=[]
            demolist4=[]
            sub_id=0
            cla_id= 0
            stu_id =0.0
            for user in list(items):
                sub_id=int(user["exam_sub_id"])
                cla_id= int(user["cla_id"])
                stu_id =user["stu_id"]
                demolist4.append(user["exam_score"])
            demolist3.append(cla_id)
            demolist3.append(stu_id)
            demolist3.append(sub_id)
            for each in demolist4:
                demolist3.append(each)
            demolist2.append(demolist3)
    data1 = pd.DataFrame(demolist2)
    data1.to_csv('data1.csv')
    return jsonify({"data":demolist2})
# data = pd.DataFrame(list(demo.find()))
# data.head()
# # 保存为csv格式
# data.to_csv('szHousePrice.csv',encoding='utf-8')
# # 读取csv数据
# df = pd.read_csv('szHousePrice.csv',low_memory=False,index_col=0)
# # 查看数据大小(行列)
# data.shape
# # 查看数据行号
# data.columns
# # 找出所有满足字段的行
# df1 = data.loc[:,["成交时间","成交均价"]]
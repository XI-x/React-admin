# 班级成绩分析
from flask import Flask, request, jsonify, session
import requests
from flask import Blueprint
import pymongo
from bson.json_util import dumps
from operator import itemgetter
from itertools import groupby
from collections import Counter

class_grade_api = Blueprint('classgrade_api', __name__)
client = pymongo.MongoClient(host="localhost", port=27017) #连接到数据库
db = client.bysj


@class_grade_api.route("/classgrade",methods=["POST"])
def get_class_grade():
    one_id = [926,927,928,929,930,934,935,936,937,938]
    two_id = [901,902,903,904,905,906,907,908,909,910]
    three_id = [916,917,918,919,920,921,922,923,924,925]
    subjectid = [1,2,3,4,5,6,7,8,17] #语文 数学 英语 物理 化学 生物 历史 地理   政治
    get_data = request.get_json()
    key_id = int(get_data.get("key_id"))
    print(key_id)
    data= getone(key_id)

    
    return jsonify(data)

def getone(value):

    classgrade = []
    user = db.StudentExamRecord.find({"cla_id":value })
    demoname = [] #存储考试名称
    demograde = [] #粗存考试分数
    demo = {} #临时存储分数
    for each in user:
        if each["exam_number"] not in [301,302]:
            if each["exam_name"] == "\t2017学年度第一学期期末考试":
                each["exam_name"] = "2017学年度第一学期期末考试"
            classgrade.append(each)
    new_list = sorted(classgrade, key=lambda test:(test["exam_number"],test["exam_sub_id"]),reverse=True) #依据考试时间/考试科目排序
    #return {"newlist":new_list}
    for date, items in groupby(new_list, key=itemgetter('exam_number',"exam_sub_id")):
        demosubgrade = []
        demowenli1 =[]
        exam_name = ""
        for each in list(items):
            demosubgrade.append(each["exam_score"])
            exam_name = each["exam_name"]
        demoname.append(exam_name)
        condition = lambda t: t != 0.0
        filter_list = list(filter(condition, demosubgrade))
        demograde.append(filter_list)

    list2 = list(set(demoname))
    list2.sort(key=demoname.index)
    cla_grade = []
    demo2 = []
    for i in range(len(demograde)):        
        if i%9 ==0 and i!=0:
            cla_grade.append(demo2)

            if i != len(demograde)-1: 
                demo2 = []
        demo2.append(demograde[i])
    cla_grade.append(demo2)
    bargrade = []
    for item in cla_grade:
        demo_bargrade = []
        for each in item:
            demo_bargrade.append(getbar(each))
        bargrade.append(demo_bargrade)
    totalgrade = []  #班级总分
    totaluser = db.StudentTotalGrade.find({"cla_id":value })
    for each in totaluser:
        if each["exam_name"] == "\t2017学年度第一学期期末考试":
                each["exam_name"] = "2017学年度第一学期期末考试"
        totalgrade.append(each)
    new_list1 = sorted(totalgrade, key=lambda test:(test["exam_number"]),reverse=True) #总分依据考试时间/考试科目从小到大排序
    demototalgrade=[]#总分表
    for date, items in groupby(new_list1, key=itemgetter('exam_number')):
        list3=[]
        for each in items:
            list3.append(each["total_grade"])
        demototalgrade.append(getbar(list3))
    return {"demoname" : list2,"demograde":cla_grade,"bargrade":bargrade,"totalgrade":demototalgrade}

def getbar(list1):
    counter= Counter(list1)
    k = counter.most_common(len(counter))  # 找出全部元素从大到小的元素频率以及对应的次数。
    # 转化成列表形式，列表每一项又是元祖。

    print(counter)
    print(k)
    demo = []
    demo1 = []
    for i in k:
        print(str(i[0]) + " " + str(i[1]))
        demo1.append(i[0])
        demo1.append(i[1])
        demo.append(demo1)
        demo1= []
    return demo

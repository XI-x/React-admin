#创建学生单条考试记录表 StudentExamRecord 
from flask_csv import send_csv
from pymongo import MongoClient
import csv
import cpca
import pandas as pd
import numpy as np
from pandas import DataFrame
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


def insertToMongoDB(db):
    fid = [14497,14495,14477,14480,14456,14482,14464,14487,14512,14460,14050,13685,13599,13564]
    cla_id =[901,902,903,904,905,906,907,908,909,910,
    916,917,918,919,920,921,922,923,924,925,
    926,927,928,929,930,934,935,936,937,938]
    one_id = [926,927,928,929,930,934,935,936,937,938]
    two_id = [901,902,903,904,905,906,907,908,909,910]
    three_id = [916,917,918,919,920,921,922,923,924,925]
    idcount = 0
    db.StudentExamRecord.delete_many({})
    for key_id in cla_id:
        user = db.studentinfo_demo.find({"cla_id":key_id })
        stu_id = [] #该班级学生id集合
        for each in user:
            stu_id.append(each["stu_id"])
        print(stu_id)
        #db.StudentExamRecord.delete_many({})
        #循环改班级所有学生id，查询相关成绩信息
        demo = [] #所有该考生考试记录
        for each in stu_id:
            if each in fid:
                continue
            studentinfo = db.student_grade.find({"stu_id":int(each) })  
            for item in studentinfo:
                exam={} # 一条考生考试记录
                if key_id in one_id:
                    if item["test_term"] == '2018-2019-1':
                        exam["exam_name"]=item["test_name"]
                        exam["exam_number"] =item["test_number"]
                        exam["exam_term"] =item["test_term"]
                        exam["exam_sub"] = item["sub_name"]
                        exam["exam_sub_id"] =item["sub_id"]
                        exam["stu_id"] =item["stu_id"]
                        exam["exam_score"] = item["test_score"]
                        demo.append(exam)
                elif key_id in two_id:
                    if item["test_term"] == '2018-2019-1' or item["test_term"] == '2017-2018-1' or item["test_term"] == '2017-2018-2':
                        exam["exam_name"]=item["test_name"]
                        exam["exam_number"] =item["test_number"]
                        exam["exam_term"] =item["test_term"]
                        exam["exam_sub"] = item["sub_name"]
                        exam["exam_sub_id"] =item["sub_id"]
                        exam["stu_id"] =item["stu_id"]
                        exam["exam_score"] = item["test_score"]
                        demo.append(exam)
                else:
                    if item["test_term"] == '2018-2019-1' or item["test_term"] == '2017-2018-1' or item["test_term"] == '2017-2018-2' or item["test_term"] == '2016-2017-1' or item["test_term"] == '2016-2017-2':
                        exam["exam_name"]=item["test_name"]
                        exam["exam_number"] =item["test_number"]
                        exam["exam_term"] =item["test_term"]
                        exam["exam_sub"] = item["sub_name"]
                        exam["exam_sub_id"] =item["sub_id"]
                        exam["stu_id"] =item["stu_id"]
                        exam["exam_score"] = item["test_score"]
                        demo.append(exam) 
            #新建一个临时表用以存储改班级所有学生的考试集合
            # eaxm = {"eaxm_name":"","exam_number":0,"exam_class":[
            #     {"exam_sub":"","exam_sub_id":0,"stu_id":0,"exam_score":0.0}
            # ]}
        new_list = sorted(demo, key=lambda test:(test["exam_number"],test["exam_sub_id"],test["exam_score"]),reverse=True) #依据考试时间/考试科目、考试分数从小到大排序
        #判断学生单学科排名
        sub_id=[]
        exam_num=[]
        demo1 = {}
        counts = 1

        for item in new_list:
            idcount+=1
            if item["exam_number"] in exam_num:
                if item["exam_sub_id"] in sub_id:
                    counts+=1
                else:
                    sub_id.append(item["exam_sub_id"])
                    counts = 1
            else:
                del exam_num[:]
                del sub_id[:]
                exam_num.append(item["exam_number"])
                sub_id.append(item["exam_sub_id"])
                counts = 1
                    
            demo1["exam_name"] = item["exam_name"]
            demo1["exam_number"] = int(item["exam_number"])
            demo1["exam_score"] = item["exam_score"]
            demo1["exam_sub"] = item["exam_sub"]
            demo1["exam_sub_id"] = int(item["exam_sub_id"])
            demo1["exam_term"] = item["exam_term"]
            demo1["stu_id"] = int(item["stu_id"])
            demo1["stu_rank"] = counts
            demo1["_id"] = idcount
            demo1["cla_id"] = key_id
            db.StudentExamRecord.insert_one(demo1)
            print(counts)
            print('成功添加了'+str(idcount)+'条数据 ')
    



        

        
            
           
                


# 创建主函数
def main():
    db=connection()
    insertToMongoDB(db)
# 判断是不是调用的main函数。这样以后调用的时候就可以防止不会多次调用 或者函数调用错误
if __name__=='__main__':
    main()
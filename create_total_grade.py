#创建学生个人单场考试总分 #StudentTotalGrade
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

def insertToMongoDB(db):
    fid = [14497,14495,14477,14480,14456,14482,14464,14487,14512,14460,14050,13685,13599,13564]
    cla_id =[
    901,902,903,904,905,906,907,908,909,910,
    916,917,918,919,920,921,922,923,924,905,
    926,927,928,929,930,934,935,936,937,938]
    counts= 0

    db.StudentTotalGrade.delete_many({})
    for key_id in cla_id:
        user = db.studentinfo_demo.find({"cla_id":key_id })
        stu_id = [] #该班级学生id集合
        for each in user:
            stu_id.append(each["stu_id"])
        print(stu_id)
        for item in stu_id:
            if item in fid:
                continue
            stu_grade = db.StudentExamRecord.find({"stu_id":item})
        #stu_grade = dumps(db.StudentExamRecord.find({"stu_id":stu_id[0]}),ensure_ascii=False)
            col_grade = []#学生个人成绩集合
            sub_number = [ ] #学科number集合
            demo = {} #单条学生总分数据用于插入数据库
            total_grade = 0.0
            examcount=0
            for item in stu_grade:
                if item["exam_number"] in sub_number:
                    total_grade = total_grade+item["exam_score"]
                else:
                    if total_grade != 0.0:
                        examcount+=1
                        demo["total_grade"]=total_grade
                        counts+=1
                        demo["_id"] = counts
                        db.StudentTotalGrade.insert_one(demo)
                         
                        print('成功添加了'+str(counts)+'条数据 ')
                    
                    total_grade = 0.0
                    sub_number.append(item["exam_number"])
                    total_grade = total_grade+item["exam_score"]
                    demo["exam_name"] = item["exam_name"]
                    demo["exam_number"] =int(item["exam_number"])
                    demo["exam_term"] = item["exam_term"] 
                    demo["cla_id"]  = item["cla_id"]
                    demo["stu_id"] = item["stu_id"]
            if examcount != len(sub_number):
                demo["total_grade"]=total_grade
                counts+=1
                demo["_id"] = counts
                db.StudentTotalGrade.insert_one(demo)
                print('成功添加了'+str(counts)+'条数据 ')

    return "nice"


# 创建主函数
def main():
    db=connection()
    insertToMongoDB(db)
# 判断是不是调用的main函数。这样以后调用的时候就可以防止不会多次调用 或者函数调用错误
if __name__=='__main__':
    main()
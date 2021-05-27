#学生单场单学科考试表未排名 student_grade
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
    set1=db.student_grade
    # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    #第一种直接remove
    # set1.remove(None)
    #第二种remove不好用的时候
    set1.delete_many({})
    return set1

def insertToMongoDB(set1):
    # 打开文件teacher.csv
    with open('D:\\bysj-workspace\\education_data\\5_chengji.csv','r',encoding='utf-8')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader=csv.DictReader(csvfile)
        # 创建一个counts计数一下 查看一共添加了了多少条数据以验证是否正确无重复添加
        counts=0
        demo = {}
        exam_id = [2,3,6,7,9] #保留考试的id
        sub_id = [57,59,38,13] #删除学科的id
        for each in reader:
            # 将数据中需要转换类型的数据转换类型。
            #print(each['mes_TestID'])
            #demo['test_id']=int(each['mes_TestID'])
            if each['mes_sub_id'] == None or each['mes_sub_id']=='':
                continue
            elif int(each["exam_type"]) not in exam_id:
                continue
            elif int(each['mes_sub_id']) in sub_id:
                continue
            else:
                demo['test_number']=int(each['exam_number'])
                demo['test_name']=each['exam_numname']                
                demo['sub_id']=int(each['mes_sub_id'])
                demo['sub_name']=each['mes_sub_name']
                demo['test_type']=int(each['exam_type'])
                demo['test_term']=each['exam_term']
                demo['stu_id']=int(each['mes_StudentID'])
                if each['mes_Score'] =='-2' or each['mes_Score']=='-1' or each['mes_Score']=='-3' :
                    demo['test_score']=0.0
                else:
                    demo['test_score']=float(each['mes_Score'])
                # 每次使用同一个变量存储不同的数据，导致数据库认为每次存储的是同一条数据，最终生成同一个_id值
                # 手动添加_id值,当插入的数据带有_id的字段时,mongodb就不再自动生成_id
                demo['_id'] = counts+1 
                set1.insert_one(demo)
                counts+=1
                print('成功添加了'+str(counts)+'条数据 ')
            
           
                


# 创建主函数
def main():
    set1=connection()
    insertToMongoDB(set1)
# 判断是不是调用的main函数。这样以后调用的时候就可以防止不会多次调用 或者函数调用错误
if __name__=='__main__':
    main()
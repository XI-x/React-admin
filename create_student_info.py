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
    set1=db.studentinfo_demo
    # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    #第一种直接remove
    set1.remove(None)
    #第二种remove不好用的时候
    # set1.delete_many({})
    return set1

def insertToMongoDB(set1):
    # 打开文件teacher.csv
    with open('D:\\bysj-workspace\\education_data\\2_student_info.csv','r',encoding='gbk')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader=csv.DictReader(csvfile)
        # 创建一个counts计数一下 查看一共添加了了多少条数据以验证是否正确无重复添加
        counts=0
        demo = {}
        place = ['demo']
        for each in reader:
            # 将数据中需要转换类型的数据转换类型。
            demo['stu_id']=int(each['bf_StudentID'])
            demo['stu_name']=each['bf_Name']
            demo['stu_sex']=each['bf_sex']
            demo['stu_nation']=each['bf_nation']
            demo['stu_borndate']=int(each['bf_BornDate'])
            demo['cla_name']=each['cla_Name']
            # 判断住址是否登记
            if each['bf_NativePlace'].strip()=='':
                demo['stu_nativeplace']="未登记"
            else:
                place[0] = each['bf_NativePlace']
                df = cpca.transform(place)
                # 首先将pandas读取的数据转化为array
                data_array = np.array(df)
                # 然后转化为list形式
                data_list =data_array.tolist()
                #浙江省内细分到市，省外到省
                if data_list[0][0] == '浙江省':
                    demo['stu_nativeplace']=data_list[0][0]+data_list[0][1]
                else:
                    demo['stu_nativeplace']=data_list[0][0]
            demo['stu_residencetype']=each['Bf_ResidenceType']
            demo['stu_policy']=each['bf_policy']
            demo['cla_id']=int(each['cla_id'])
            demo['cla_term']=each['cla_term']
            #判断学生是否处于休学
            if each['bf_leaveSchool'].strip()=='':
                demo['stu_leaveschool']="否"
                if each['bf_zhusu'].strip()=='':
                    demo['stu_zhusu']="不住宿"
                    demo['stu_qinshihao']=0
                else:
                    demo['stu_zhusu']="住宿"
                    demo['stu_qinshihao']=int(each['bf_qinshihao'])
            else:
                demo['stu_leaveschool']="是"
                demo['stu_zhusu']="不住宿"
                demo['stu_qinshihao']=0
            # 每次使用同一个变量存储不同的数据，导致数据库认为每次存储的是同一条数据，最终生成同一个_id值
            # 手动添加_id值,当插入的数据带有_id的字段时,mongodb就不再自动生成_id
            demo['_id'] = int(each['bf_StudentID'])  
            print(demo)
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

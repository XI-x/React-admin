#创建高二学生个人单场考试总分 #ClassTwo
from pymongo import MongoClient
import csv

#对所有学生信息表excel进行处理并建立数据集合
# 创建连接MongoDB数据库函数
def connection():
    # 1:连接本地MongoDB数据库服务
    conn=MongoClient("localhost")
    # 2:连接本地数据库(bysj)。没有时会自动创建
    db=conn.bysj
    # 3:创建集合
    set1=db.classtwo
    # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    #第一种直接remove
    set1.remove(None)
    #第二种remove不好用的时候
    #set1.delete_many({})
    return set1

def insertToMongoDB(set1):
       # 打开文件guazi.csv
    with open('data_classtwo.csv','r',encoding='utf-8')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader=csv.DictReader(csvfile)
        # 创建一个counts计数一下 看自己一共添加了了多少条数据
        counts=0
        for each in reader:
            # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）。
            each['_id']=int(each['count'])
            each['cla_id']=int(each['cla_id'])
            each['stu_id']=int(each['stu_id'])
            each['sub_id']=int(each['sub_id'])
            each['pre_score']=float(each['pre_score'])
            set1.insert(each)
            counts+=1
            print('成功添加了'+str(counts)+'条数据 ')


    return "nice"


# 创建主函数
def main():
    set1=connection()
    insertToMongoDB(set1)
# 判断是不是调用的main函数。这样以后调用的时候就可以防止不会多次调用 或者函数调用错误
if __name__=='__main__':
    main()
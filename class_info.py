from flask_csv import send_csv
from pymongo import MongoClient
import csv
#对学生信息表进行处理
# 创建连接MongoDB数据库函数
def connection():
    # 1:连接本地MongoDB数据库服务
    conn=MongoClient("localhost")
    # 2:连接本地数据库(bysj)。没有时会自动创建
    db=conn.bysj
    # 3:创建集合
    set1=db.class_info
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
        class_admin ={}
        id_count = []
        for each in reader:
            #判断cla_id是否存在
            if int(each['cla_id']) not in id_count:
                id_count.append(int(each['cla_id']))
                # 将数据中需要转换类型的数据转换类型。
                class_admin['id']=int(each['cla_id'])
                class_admin['class_name']=each['cla_Name']
                # 每次使用同一个变量存储不同的数据，导致数据库认为每次存储的是同一条数据，最终生成同一个_id值
                # 手动添加_id值,当插入的数据带有_id的字段时,mongodb就不再自动生成_id
                class_admin['_id'] = int(each['cla_id'])  
                print(class_admin)
                set1.insert_one(class_admin)
                counts+=1
                print('成功添加了'+str(counts)+'条数据 ')


# 创建主函数
def main():
    set1=connection()
    insertToMongoDB(set1)
# 判断是不是调用的main函数。这样以后调用的时候就可以防止不会多次调用 或者函数调用错误
if __name__=='__main__':
    main()

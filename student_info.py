# 班级概括获取学生详细信息接口文件  901为例子
from flask import Flask, request, jsonify, session
import requests
from flask import Blueprint
import pymongo
from bson.json_util import dumps


student_info_api = Blueprint('studentinfo_api', __name__)
client = pymongo.MongoClient(host="localhost", port=27017) #连接到数据库
db = client.bysj

@student_info_api.route("/studentinfo",methods=["POST"])
def get_student_info():
    get_data = request.get_json()
    key_id = int(get_data.get("key_id"))
    #print(key_id)
    user = dumps(db.studentinfo_demo.find({"cla_id":key_id }),ensure_ascii=False) #返回的是cursor（find返回值）,将其转换为json对象
    return user

@student_info_api.route("/cardinfo",methods=["POST"])
def get_card_info():
    get_data = request.get_json()
    key_id = int(get_data.get("key_id"))
    #print(key_id)
    user = db.studentinfo_demo.find({"cla_id":key_id }) #返回的是cursor（find返回值）,将其转换为json对象
    man = 0 #男生人数
    total = 0 #班级学生总人数
    num_zhusu = 0 #住宿生人数
    num_policy =0 #共青团员人数
    num_type = 0 #城镇户口类型人数
    num_address = 0#省内住址人数
    num_leaveschool =0 #离校人数
    num_address_none = 0 #未登记住址人数
    for each in user:
        if each['stu_leaveschool'] == '是':
            num_leaveschool+=1
            continue
        #print(each)
        total+=1
        if each['stu_sex'] == '男':
            man+=1
        if each['stu_zhusu'] == '住宿':
            num_zhusu+=1
        
        if each['stu_policy'] == '共青团员':
            num_policy+=1
        if each['stu_residencetype'] == '城镇':
            num_type+=1
        if '浙江省' in each['stu_nativeplace']:
            num_address+=1
        if each['stu_nativeplace'] == '未登记':
            num_address_none+=1
        

    return jsonify({'total':total,'man':man,'num_zhusu':num_zhusu,'num_policy':num_policy,'num_type':num_type,'num_address':num_address,'num_address_none':num_address_none})

@student_info_api.route("/teacherinfo",methods=["POST"])
def get_teacher_info():
    get_data = request.get_json()
    key_id = int(get_data.get("key_id"))
    #print(key_id)
    user = db.teacher.find({"cla_id":key_id ,"cla_term":'2018-2019-1'}) #返回的是cursor（find返回值）
    teacher_info=[]
    for each in user:
        teacher_info.append({"sub_name":each["sub_name"],"tea_name":each["tea_name"]})
    return jsonify({'data':teacher_info})
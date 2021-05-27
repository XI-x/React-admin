# 学生画像
from flask import Flask, request, jsonify, session
import requests
from flask import Blueprint
import pymongo
from bson.json_util import dumps

student_pic_api = Blueprint('studentpic_api', __name__)
client = pymongo.MongoClient(host="localhost", port=27017) #连接到数据库
db = client.bysj
two_id = [901,902,903,904,905,906,907,908,909,910]

@student_pic_api.route("/studentpic",methods=["POST"])
def get_student_pic():
    get_data = request.get_json()
    key_id = int(get_data.get("key_id"))
    user = db.studentinfo_demo.find({"cla_id":key_id })
    stu_id = [] #该班级学生id集合
    for each in user:
        stu_id.append(each["stu_id"])
    print(stu_id[0])#第一个学生
    stu_pic = get_studentinfo(stu_id[0],key_id)

    return stu_pic

@student_pic_api.route("/studentpic_id",methods=["POST"])
def get_student_picid():
    get_data = request.get_json()
    key_id = int(get_data.get("stu_id"))
    cla_id = int(get_data.get("cla_id"))
    stu_pic = get_studentinfo(key_id,cla_id)
    return stu_pic

#判断该学科
def setdata(one,two):

    if len(one) == two :
        return one 
    else: 
        one.append(10)
        return one


def get_studentinfo(s_id,cla_id):
    subjectid = [1,2,3,4,5,6,7,8,9,17] #语文 数学 英语 物理 化学 生物 历史 地理  体育 政治
    stu_info = db.studentinfo_demo.find_one({"stu_id": s_id}) #查找学生的个人信息
    if stu_info == None:
        return  0 #表示无该学生信息
    else:
        sub_rank = db.StudentExamRecord.find({"stu_id":s_id })
        # total_rank =dumps( db.StudentTotalRank.find({"stu_id":s_id }),ensure_ascii=False)
        total_rank =db.StudentTotalRank.find({"stu_id":s_id })
        exam_name = []  #所有考试名称集合
        totalgrade_rank = [] #总分排名集合
        total_grade = [] #总分集合
        exam_number= []
        for each in total_rank:
            exam_name.append(each["exam_name"])
            totalgrade_rank.append(each["rank"])
            total_grade.append(each["total_grade"])
            exam_number.append(each["exam_number"])
        #从个人单场考试总分带排名 #StudentTotalRank查找该学生的总分及排名
       
        yw_rank = [] #存储学生单场考试单科成绩数据
        math_rank = []
        yy_rank=[]
        wl_rank = []
        hx_rank = []
        sw_rank = []        
        ls_rank = []
        dl_rank =[]
        zz_rank = []
        demo = [] #临时存储考试number用以判断该学科在本次考试是否设置考核
        subcounts = 0
        for each in sub_rank:
            if each["exam_number"] in exam_number: 
                if each["exam_number"] not in demo:
                    demo.append(each["exam_number"])
                    yw_rank= setdata(yw_rank,subcounts)
                    math_rank = setdata(math_rank,subcounts)
                    yy_rank = setdata(yy_rank,subcounts)
                    wl_rank = setdata(wl_rank,subcounts)
                    hx_rank = setdata(hx_rank,subcounts)
                    sw_rank = setdata(sw_rank,subcounts)
                    ls_rank = setdata(ls_rank,subcounts)
                    dl_rank = setdata(dl_rank,subcounts)
                    zz_rank =setdata(zz_rank,subcounts)
                    subcounts+=1
                    print(math_rank,dl_rank)
                if each["exam_sub_id"] == 1:
                    yw_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 2:
                    math_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 3:
                    yy_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 4:
                    wl_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 5:
                    hx_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 6:
                    sw_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 7:
                    ls_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 8:
                    dl_rank.append(each["stu_rank"])
                if each["exam_sub_id"] == 17:
                    zz_rank.append(each["stu_rank"])
        yw_rank= setdata(yw_rank,subcounts)
        math_rank = setdata(math_rank,subcounts)
        yy_rank = setdata(yy_rank,subcounts)
        wl_rank = setdata(wl_rank,subcounts)
        hx_rank = setdata(hx_rank,subcounts)
        sw_rank = setdata(sw_rank,subcounts)
        ls_rank = setdata(ls_rank,subcounts)
        dl_rank = setdata(dl_rank,subcounts)
        zz_rank =setdata(zz_rank,subcounts)
        presocre = []
        if cla_id in two_id:
            userpre =db.classtwo.find({"stu_id":s_id })
        for each in userpre:
            presocre.append(each["pre_score"])
        return jsonify({"stu_info":stu_info,"total_rank":totalgrade_rank,"exam_name":exam_name,"total_grade":total_grade,"yw_rank":yw_rank,"math_rank":math_rank,"yy_rank":yy_rank,"wl_rank":wl_rank,"hx_rank":hx_rank,"sw_rank":sw_rank,"ls_rank":ls_rank,"dl_rank":dl_rank,"zz_rank":zz_rank,"pre_score":presocre})
        



   
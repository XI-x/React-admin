from flask import Flask, request, jsonify, session
import pymongo
from flask import Blueprint
 
login_api = Blueprint('account_api', __name__)
client = pymongo.MongoClient(host="localhost", port=27017) #连接到数据库
db = client.bysj


@login_api.route("/login",methods=["POST"])
def login():
    get_data = request.get_json()
    username = int(get_data.get("password"))
    password = get_data.get("username")
    if not all([username,password]):
        return jsonify(msg = "登录参数不完整")

    user = db.class_info.find_one({"id":username }) #find_one 返回的是字典对象而不是cursor（find返回值）
    if user and user["class_name"] == password:
        session["class_id"] = username
        return jsonify({'status':0,'admin_data':user,'msg':'登陆成功！'})
    else:
        return jsonify({'status':1,'msg':'登录失败，请重新输入用户名或密码！'})

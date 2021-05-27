from flask import Flask, request, jsonify, session
from login import login_api
from student_info import student_info_api
from student_pic import student_pic_api
from class_grade import class_grade_api
from create_socre import test_api
app = Flask(__name__)

app.secret_key = 'adsafa'



# @app.route('/set',methods=["POST"])
# def setsession():
#     get_data = request.get_json()
#     print(get_data)
#     session[get_data.get("key_name")] = int(get_data.get("key_id")) # 设置“字典”键值对
#     print(session)
#     return 'success'
 

# @app.route('/get',methods=["POST"])
# def get():
#     # session['username']
#     get_data = request.get_json()
#     key_name = get_data.get("key_name")
#     print(key_name)
#     print(session)
#     print(session.get('class_id'))
#     print(session.get(key_name))
#     return "nice"
app.register_blueprint(login_api)
app.register_blueprint(student_info_api,url_prefix='/class_info')
app.register_blueprint(student_pic_api,url_prefix='/student')
app.register_blueprint(class_grade_api,url_prefix='/class')
app.register_blueprint(test_api,url_prefix='/test')

app.run(debug=True)
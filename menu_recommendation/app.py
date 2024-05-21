# -*- coding: cp949 -*-
from flask import Flask, request, jsonify
import json
from recommendation import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = extract_menu("����",24,["���̷�"])
    return data

@app.route('/menuRecommendation', methods=['POST'])
def recommend_menuList():
    # Spring ���κ��� ���޹��� JSON ��ü
    user_info = request.get_json()
    age = user_info.get('age')
    gender = user_info.get('gender')
    foodCategoryNameList = user_info.get('foodCategoryNameList')

    print(age, gender, foodCategoryNameList)

    recommendations = extract_menu(gender, age, foodCategoryNameList)
    return recommendations


if __name__ == "__main__":
    app.run(debug=True)
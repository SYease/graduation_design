from flask import Blueprint, jsonify, request
from app.models import Algorithm
from app import db

main_db=Blueprint('main',__name__)

@main_db.route('/')
def index():
    return '''
    <h1>欢迎来到算法学习推荐系统</h1>
    <p>这是我的毕业设计：）</p>
    '''

@main_db.route('/algorithms',methods=['GET'])
def get_algorithm():
    algorithms=Algorithm.query.all()
    return jsonify({
        'success': True,
        'algorithms':[algo.to_dict() for algo in algorithms]
    })


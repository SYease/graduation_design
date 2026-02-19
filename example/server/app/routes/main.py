"""
主页面路由蓝图
============================================================
思路说明：
main_bp 负责页面级别的路由，即用户在浏览器地址栏输入URL后
看到的HTML页面。使用Flask的 render_template 渲染Jinja2模板。

为什么用蓝图(Blueprint)：
1. Flask推荐用蓝图组织路由，类似Django的app概念
2. 不同功能的路由分开管理，代码更清晰
3. 蓝图可以有自己的模板、静态文件目录
4. 方便后续扩展（比如加一个归并排序页面，再建一个蓝图即可）
============================================================
"""
from flask import Blueprint, render_template, session
import uuid

# 创建蓝图实例
# 第一个参数 'main' 是蓝图名称，用于 url_for('main.index') 这样的反向路由
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首页路由
    渲染快速排序学习页面，同时为用户分配一个session_id
    用于后续追踪该用户的学习行为
    """
    # 如果用户还没有session_id，分配一个
    # session_id 存在Flask的session中（基于cookie），浏览器关闭前一直有效
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())[:8]

    return render_template('quicksort.html', session_id=session['session_id'])

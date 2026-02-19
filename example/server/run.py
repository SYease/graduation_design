"""
应用入口文件
============================================================
思路说明：
这是整个Flask应用的启动入口。
运行方式: python run.py
然后在浏览器打开 http://localhost:5000

使用应用工厂模式，通过 create_app() 创建应用实例。
============================================================
"""
from app import create_app

# 创建应用实例，使用开发环境配置
app = create_app('development')

if __name__ == '__main__':
    print('=' * 50)
    print('  快速排序算法学习推荐系统')
    print('  基于知识图谱的算法学习推荐系统')
    print('  打开浏览器访问: http://localhost:5000')
    print('=' * 50)
    app.run(debug=True, port=5000)

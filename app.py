from flask import Flask

app = Flask(__name__)

@app.route('/') #选择触发以下函数的url
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__': #如果这个模块被直接运行，
    app.run(debug=True)
import os
import pathlib

from flask import url_for, render_template, abort, request, session
from werkzeug.utils import redirect, secure_filename, escape

from .. import test
from ..services import TestService as testService


# Test1Controller.py里也有一个getT方法，启动时会报错
@test.route('/t', methods=['GET', ])
def getT():
    return "TestController: t"


@test.route('/<int:id>', methods=['GET', ])
def getById(id):
    return testService.getById(id)


@test.route('/getTest', methods=['GET', ])
def getTest():
    return testService.getTest()


# 重定向
@test.route('/index', methods=['GET', ])
def index():
    return redirect(url_for('test.username'))


# 重定向, 带参
@test.route('/hello')
def hello_world():
    # url_for('方法名') 获取 请求路径

    return redirect(url_for('test.helloParam', username='JohnDoe'))


# 文件上传
@test.route('/upload', methods=['POST'])
def upload_file():
    path = ""

    token = request.cookies.get('token')
    print(token)

    if request.method == 'POST':
        f = request.files['file']
        path = 'F:/aaa/bb/'

        # pathlib.Path(path).exist() 检查目录或文件是否存在
        # pathlib.Path(path).is_file() 检查path是否是一个文件,且存在
        if not pathlib.Path(path).exists():
            os.makedirs(path)
        path = path + secure_filename(f.filename)

        print(pathlib.Path(path).exists())
        print(pathlib.Path(path).is_file())

        f.save(path)

    return path


@test.route('/username')
def username():
    return '重定向========='


@test.route('/helloParam')
def helloParam():
    if request.method == 'POST':
        username = request.form['username']
    else:
        username = request.args.get("username")

    return 'username: %s' % username


# 返回400状态码
@test.route('/user400')
def user400():
    return '<p>Bad Request !</p>', 400


# redirect 到百度
@test.route('/baidu')
def baidu():
    return redirect('http://www.baidu.com')


# redirect 到百度
@test.route('/index.html')
def indexViews():
    return render_template('test/index.html', name="tom")


@test.route('/info')
@test.route('/info/<name>')
def info(name=None):
    # data = testService.getTest()

    return render_template('test/info.html', name=name)


# 设置响应文本和cookie
@test.route('/testCookie')
def testCookie():
    return testService.testCookie()


@test.route('/home')
def home():
    if 'username' in session:
        name = escape(session['username'])
        # 清空session, 重启服务发现username依然存于session中，好奇
        # session.clear()
        return 'Logged in as %s' % name
    return 'You are not logged in'


@test.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('test.home'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


# 404测试
@test.route('/get/<id>')
def getId(id):
    if id != '9':
        abort(404)
    return '<h1>Hello, %s!</h1>' % id

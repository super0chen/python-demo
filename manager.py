#!/usr/bin/python
from run import app_server, init_server
from flask_script import Manager, Server, Command

manager = Manager(app_server)

# 可以运行命令：python manage.py server 来运行整个项目, 默认是runserver
manager.add_command("server", Server(host='0.0.0.0', port=8000))
if __name__ == '__main__':
    init_server()
    manager.run()

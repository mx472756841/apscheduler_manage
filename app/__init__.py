import importlib
import os

from flask import Flask
from flask_admin import AdminIndexView, Admin
from flask_babelex import Babel

from app.common.flask_apscheduler import CustomAPScheduler
from config import config
from .models import db


def init_view():
    """
    动态导入本地view
    :param app:
    :return:
    """
    #: 基础view处理
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.walk(os.sep.join([curr_dir, "views"]))
    #: 获取views中多有定义的views信息
    root, paths, fs = files.send(None)
    fs.remove("__init__.py")
    for file_name in fs:
        module = importlib.import_module("app.views" + ".{}".format(file_name.split(".")[0]))
        views = getattr(module, 'views', [])
        admin.add_views(*views)


def init_middlewares():
    """
    处理中间件
    :return:
    """
    middlewares = []
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.walk(os.sep.join([curr_dir, "middlewares"]))
    root, paths, fs = files.send(None)
    fs.remove("__init__.py")
    for file_name in fs:
        module = importlib.import_module("app.middlewares" + ".{}".format(file_name.split(".")[0]))
        tmp_middlewares = getattr(module, 'middlewares', [])
        middlewares.extend(tmp_middlewares)

    return middlewares


admin = Admin(name="APScheduler管理平台", index_view=AdminIndexView(), template_mode="bootstrap3")
#: 国际化
babel = Babel(default_locale='zh_Hans_CN')

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)
# 初始化Sqlarchemy
db.app = app
db.init_app(app)
# 初始化Admin
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
init_view()
admin.init_app(app)
# 初始化国际化
babel.init_app(app)
# 初始化 flask_apscheduler，将scheduler嵌入到flask管理，本地在flask_apscheduler插件中增加add_listener监听所有的job生命周期
flask_apscheduler = CustomAPScheduler(db.session, app=app)
# 启动apscheduler
flask_apscheduler.start()
# 注册蓝图
# 增加中间件处理
for middleware in init_middlewares():
    app.before_request(middleware.process_request)

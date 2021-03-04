import datetime
import importlib
import os

from flask import Flask
from flask_admin import AdminIndexView, Admin
from flask_babelex import Babel

from app.common.flask_apscheduler import CustomAPScheduler, LOGGER
from config import config
from .models import db


# todo 此函数用于job生命周期监控测试，后续增加flask_apscheduler动态job变更
def test_apscheduler_interval():
    LOGGER.info(f"test_apscheduler_interval >>>>> {datetime.datetime.now()}")

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
# 测试生命周期使用，无实际意义，实际使用时可删除或改为自己需要的函数
if not flask_apscheduler.get_job('test_apscheduler_interval'):
    job = flask_apscheduler.add_job("test_apscheduler_interval", test_apscheduler_interval,
                                    name="测试interval触发器 30s执行一次",
                                    trigger='interval',
                                    seconds=30,
                                    misfire_grace_time=10)
# 注册蓝图
# 增加中间件处理
for middleware in init_middlewares():
    app.before_request(middleware.process_request)
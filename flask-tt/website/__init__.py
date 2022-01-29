from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # 初始化
    db.init_app(app)



    from .views import views
    from .auth import auth

    # url_prefix是前缀，如果蓝图定义的是route('hello')，prefix是'auth/'，那么url大概就是'auth/hello'
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    # import .models 也行 from .models import User,Note #(为什么要导入这些呢？因为确保这些定义的模型在我门正式创建数据库的之前运行，定义好。)
    from .models import User, Note
    create_database(app)

    # 下面的代码放到创建数据库后面
    login_manager = LoginManager()
    # 如果我门没有登陆，我门应该去哪里？应该redirect to 登陆页面
    login_manager.login_view = 'auth.login'
    # 告诉manager你用的哪个app
    login_manager.init_app(app)


    # 这是告诉flask 我们怎样加载一个user
    @login_manager.user_loader
    def load_user(id):
        # query.get is similar to filter_by,但是get是照着primary key来查询的。
        return  User.query.get(int(id))


    return app

def create_database(app):
    # 用os的path,就是查看数据库是否已经存在，不存在就创建一个
    if not path.exists('website/'+DB_NAME):
        # app=app，意思是为app这个对象创建数据库
        db.create_all(app=app)
        print('Created Database!')
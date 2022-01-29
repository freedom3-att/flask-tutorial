from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
# 对密码做限制的东西，更安全。比如不能用空密码。加密用的
from werkzeug.security import generate_password_hash, check_password_hash
# 这个地方要导入，db要用到的。
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)



@auth.route('/login',methods=['GET','POST'])
def login():
    # 传递变量，text也可以换名称，随便什么，在这个例子里面text就是一个变量了，然后再到login的html文件里面使用这个变量。
    # 可以加多个变量
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # 这是通过email查找，你也可以通过id查找
        user = User.query.filter_by(email=email).first()
        if user:
            # 也可以改成user.email。
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category='sucess')
                # remember差不多意思是，登陆之后网页记住你了，就不用再反复登陆，除非你退出了，或者删除了session。
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again!',category='error')
        else:
            flash("Email does not exist.",category='error')
    return render_template('login.html',user=current_user)

@auth.route('/logout')
# 这个意思其实就是，如果你不登陆你就不能推出，不登陆就不能看主页
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist!",category='error')
        elif len(email) < 12:
            flash('Email must be greater than 12 characters.',category='error')# category取决于你自己
        elif len(firstName)<2:
            flash('Name must be greater than 2 characters.',category='error')
        elif password1 != password2:
            flash('password must be equal.',category='error')
        elif len(password1) < 7:
            flash('password must be greater than 7 characters.',category='error')
        else:
            new_user = User(email=email,first_name=firstName,password=generate_password_hash(password1,method='sha1'))
            # add user to database
            db.session.add(new_user)
            db.session.commit()

            login_user(user, remember=True)
            flash('Account created!',category='success')

            return redirect(url_for('views.home'))

    return render_template('sign_up.html',user=current_user)
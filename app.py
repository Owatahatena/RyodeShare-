from flask import Flask, render_template, request, url_for, redirect, session #追加
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from collections import defaultdict
import mysql.connector
from DB import DB
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'owatahatena'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


app.config['SECERET_KEY'] = "owatahatena"


class User(UserMixin):
    pass

db = DB()
sql = ('SELECT boardernumber,password FROM boarders_table')
users = dict(db.all_select(sql))
print('++++++++++++++++++++++++++++++++')
print(users)
print('++++++++++++++++++++++++++++++++')

#LOGIN
@login_manager.user_loader
def load_user(boader_number):
    if int(boader_number) not in users.keys():
        return 

    user = User()
    user.id = int(boader_number)
    return user


@app.route('/login')
def login():
    return render_template('login2.html')


@app.route('/_login', methods=["POST"])
def _login():
    if(request.method == "POST"):
        db = DB()
        boader_number = request.form['number']
        boader_number = int(boader_number)

        password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
        
        #return ID and password
        #sql = ('SELECT password FROM boarders_table WHERE boardernumber=%s;')
        #data = db.select(sql,boa)
        if boader_number in users:
            if password == users[boader_number]:
                user = User()
                user.id = boader_number
                f = login_user(user)
                return redirect(url_for('home'))

            #bad login
            else:
                return render_template('login2.html')
        else:
            return 'error'


@app.route('/protected')
@login_required
def protected():
    return 'logged in as:' + str(current_user.id)


@app.route('/')
def index():
    return redirect(url_for('login'))
    #return render_template('index.html') #変更



@app.route('/test')
def test():
    return render_template('index3.html')


@app.route('/home')
@login_required
def home():
    db = DB()
    now_date = datetime.date.today()
    sql = 'select * from time_real_table where boardernumber = %s and answer_date = %s'
    data= db.select(sql,[current_user.id,now_date])
    seat_sql = 'select * from seat_table where boardernumber = %s'
    seat_data = db.select(seat_sql,[current_user.id])

    if data and seat_data:
        data = data[0]
        seat_data = seat_data[0]
        ID,boardernumber,breakfast_time,dinner_time,bath_time,date = data
        ID,boardernumber,breakfast_seat,dinner_seat = seat_data

        if breakfast_time == 5:
            breakfast_time = '8:30'

        if dinner_time == 4:
            dinner_time = '18:30'

        if bath_time == 3:
            bath_time = '19:00'


        return render_template('index3.html',breakfast_time = breakfast_time, dinner_time = dinner_time, bath_time = bath_time, breakfast_seat=breakfast_seat,dinner_seat=dinner_seat)
    else:
        return 'dataがないよ'
@app.route('/_request_bathtime', methods=['POST'])
@login_required
def _request_bathtime():
    if request.method == "POST":
        request_breakfast_time = request.form['breakfast']
        request_dinner_time = request.form['dinner']
        request_bath_time = request.form['bathing']

        print(request_breakfast_time)
        print(request_dinner_time)
        print(request_bath_time)
        db = DB()

        sql = "INSERT INTO time_request_table (boardernumber,bathtime_request,breakfasttime_request,dinnertime_request,answer_date) VALUES (%s,%s,%s,%s,%s)"
        import datetime
        data = [current_user.id,request_bath_time,request_breakfast_time,request_dinner_time,datetime.date.today()]
        db.insert_request(sql,data)

        return redirect(url_for('home'))

@app.route('/evalution',methods=['POST'])
@login_required
def evalution():
    if request.method == 'POST':
        pass
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logged out'


## おまじない
if __name__ == "__main__":
    app.run(debug=True)

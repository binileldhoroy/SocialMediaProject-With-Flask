from flask import Flask,render_template,redirect,request,session
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'sample_project'

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'flask_sample_project'

mysql.init_app(app)

def getData(sql,vals=0):
    con = mysql.connect()
    cur = con.cursor()
    res = ''
    if(vals == 0):
        cur.execute(sql)
    else:
        cur.execute(sql,vals)
    res = cur.fetchall()
    cur.close()
    con.close()
    return res

def setData(sql,vals=0):
    con = mysql.connect()
    cur = con.cursor()
    if(vals == 0):
        cur.execute(sql)
    else:
        cur.execute(sql,vals)
    con.commit()
    res = cur.rowcount
    return res


@app.route('/')
def home():
    if 'uid' in session and 'role' in session:
        return redirect('/'+session['role']+'/home')
    return render_template('public/home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if 'uid' in session and 'role' in session:
        return redirect('/'+session['role']+'/home')
    msg = ''
    if request.method == 'POST':
        data = request.form
        sql = "select log_id,role from login where username=%s and password=%s"
        vals = (data['uname'],data['pword'])
        res = getData(sql,vals)
        if len(res):
            session['uid'] = res[0][0]
            session['role'] = res[0][1]
            return redirect('/'+res[0][1]+'/home')
        else:
            msg = 'Invalid login details'
    return render_template('public/login.html',msg=msg)

@app.route('/register',methods=['POST','GET'])
def register():
    if 'uid' in session and 'role' in session:
        return redirect('/'+session['role']+'/home')
    msg = ""
    data = ''
    if request.method=='POST':
        data = request.form
        sql = "select count(*) from login where username='%s'" % data['email']
        res = getData(sql)[0][0]
        if res == 0:
            sql = "select count(*) from user_details where phone='%s'" % data['phone']
            res = getData(sql)[0][0]
            if res == 0:
                sql = "select ifnull(max(log_id),0)+1 from login"
                log_id = getData(sql)[0][0]
                sql = "insert into login values(%s,%s,%s,'user')"
                vals = (log_id,data['email'],data['pword'])
                setData(sql,vals)
                sql = "insert into user_details values(%s,%s,%s)"
                vals = (log_id,data['name'],data['phone'])
                setData(sql,vals)
            else:
                msg = "Phone number already exists"
        else:
            msg = "Email already exists"
        return redirect('/login')
    return render_template('public/register.html',msg=msg,form=data)


@app.route('/admin/home')
def adminHome():
    if 'uid' not in session or 'role' not in session:
        return redirect('/')
    return render_template('admin/home.html')

@app.route('/admin/users/view')
def viewUsers():
    if 'uid' not in session or 'role' not in session:
        return redirect('/')
    sql = "select name,phone,username from user_details u join login l on l.log_id=u.uid where l.role='user'"
    res = getData(sql)
    return render_template('admin/viewUsers.html',users=res)


@app.route('/user/home')
def userHome():
    sql = "select * from posts where uid!=%s" % session['uid']
    res = getData(sql)
    return render_template('user/home.html',posts=res)

@app.route('/user/post/new',methods=['POST','GET'])
def addPost():
    if request.method == 'POST':
        desc = request.form['desc']
        file = request.files['image']
        sql = "select ifnull(max(pid),0)+1 from posts"
        pid = getData(sql)[0][0]
        fname = file.filename.split('.')[-1]
        fname = '%s.%s' % (pid,fname)
        sql = "insert into posts values(%s,%s,%s,%s,current_date,current_time)"
        vals = (pid,session['uid'],desc,fname)
        setData(sql,vals)
        file.save('static/uploads/'+secure_filename(fname))
        return redirect('/user/post')
    return render_template('user/addPost.html')

@app.route('/user/post')
def userPosts():
    sql = "select * from posts where uid=%s" % session['uid']
    res = getData(sql)
    return render_template('user/myPosts.html',posts=res)

@app.route('/user/post/delete/<pid>')
def deletePost(pid):
    sql = "delete from posts where pid=%s" % pid
    setData(sql)
    return redirect('/user/post')

@app.route('/logout')
def logout():
    del session['uid']
    del session['role']
    return redirect('/')

app.run(debug=True)
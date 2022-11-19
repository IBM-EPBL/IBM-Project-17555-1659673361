import sqlite3 as sql

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for,flash)
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import ibm_db

app= Flask(__name__)
app.config['DEBUG']=True
app.secret_key="mgyftuiu"
connection=ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zpj04244;PWD=xB9fQaRJsweFh5pv","","")

@app.route('/home')
def hello():
     if 'loggedin' in session and 'name' in session:
        return render_template('home.html',msg="TRUE")
     return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hospital')
def hospital():
    return render_template('hospitalhome.html')

@app.route("/blog")
def blog():
    return "<h1>Hello World from blog page</h1>"

@app.route("/blog/<int:id>")
def blogId(id):
    return "<h1>Hello World from blog page" +str(id)+"</h1>"

@app.route('/about')
def about():
    if 'loggedin' in session and 'name' in session:
        return render_template('about.html')
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/profiles/<username>")
def user(username):
    return "<h2>Hello "+username+"</h2>"

@app.route('/adduser',methods= ['POST','GET'])
def adduser():
    message=""
    if request.method=='POST':
        try:
            name= request.form['username']
            mail= request.form['mail']
            mobile= request.form['mobile']
            password= request.form['password']

            # with sql.connect("database.db") as con:
            #     cur= con.cursor()
            #     cur.execute('insert into user values(?,?,?,?)',(name,mail,mobile,password))
            #     con.commit()
            #     message="User Registered"
            #     return redirect(url_for('login'))
            sql = "SELECT * FROM ACCOUNT WHERE USERNAME =?"
            stmt = ibm_db.prepare(connection, sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)

            if account:
                return render_template('list.html', msg="Account Already Exists")
            else:
                command="INSERT INTO ACCOUNT (USERNAME,EMAIL,PHONENO,PASSWORD) VALUES (?,?,?,?)"
                prep_stmt = ibm_db.prepare(connection, command)
                ibm_db.bind_param(prep_stmt, 1, name)
                ibm_db.bind_param(prep_stmt, 2, mail)
                ibm_db.bind_param(prep_stmt, 3, mobile)
                ibm_db.bind_param(prep_stmt, 4, password)
                ibm_db.execute(prep_stmt)
                return render_template('login.html', msg="TRUE")

        except:
            con.rollback()
            message="error"
            return render_template("signup.html",error="TRUE")
    # return jsonify({message})
    # return render_template('signup.html')

@app.route('/admin')
def admin():
    data=[]
    products=[]
    if 'loggedin' in session and 'name' in session:
        sql="SELECT * FROM CATEGORY"
        stmt = ibm_db.prepare(connection, sql)
        ibm_db.execute(stmt)
        resultSet = ibm_db.fetch_both(stmt)
        while resultSet !=False:
            data.append(resultSet)
            resultSet=ibm_db.fetch_both(stmt)
        command="SELECT * FROM PRODUCT"
        stmt1 = ibm_db.prepare(connection, command)
        ibm_db.execute(stmt1)
        results = ibm_db.fetch_both(stmt1)
        while results !=False:
            products.append(results)
            results=ibm_db.fetch_both(stmt1)
        return render_template('admin.html',category=data,prods=products)
    return render_template('login.html')

@app.route("/check", methods=['POST','GET'])
def check():
    msg=""
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        account=""
        # con=sql.connect("database.db")
        # con.row_factory=sql.Row

        # cur =con.cursor()
        # cur.execute("SELECT * FROM user")

        # # rows= cur.fetchall()
        # cur.execute('SELECT * FROM user where name=? and password=?', (username,password))
        # account = cur.fetchone()
        try:
            if username.lower()=='admin' and password.lower()=='admin@123':
                session['loggedin'] = True
                session['name'] = username.lower()
                return redirect(url_for('admin'))
                
            else:
                command= "SELECT * FROM ACCOUNT WHERE USERNAME =? AND PASSWORD =?"
                stmt=ibm_db.prepare(connection,command)
                ibm_db.bind_param(stmt, 1, username)
                ibm_db.bind_param(stmt, 2, password)
                ibm_db.execute(stmt)
                result = ibm_db.fetch_assoc(stmt)
                while result !=False:
                    account=result['USERNAME']
                    id=result['USERID']
                    result = ibm_db.fetch_assoc(stmt)
                if account:
                    session['loggedin'] = True
                    session['name'] = account
                    session['id']= id
                    return redirect(url_for('hello'))
                else:
                    msg = "Incorrect username/password!"
                    return render_template('login.html', msg=msg)
        except:
            return render_template('login.html', msg="Account not found")


        #return render_template("list.html",rows=rows)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('name', None)
   session.pop('id',None)
   session.clear()
   return redirect(url_for('login'))

@app.route('/addRecord/<tablename>',methods=['POST','GET'])
def addRecord(tablename):
    if request.method=='POST':
        print(tablename)
        if tablename=='CATEGORY':
            name=request.form['catname']
            sql=f"INSERT INTO CATEGORY (CATEGORYNAME) VALUES ('{escape(name)}')"
            stmt1 = ibm_db.prepare(connection, sql)
            ibm_db.execute(stmt1)
            return redirect(url_for('admin'))
        elif tablename=='PRODUCT':
            pname=request.form['prodname']
            catid=request.form['catid']
            unit=request.form['unit']
            price=request.form['price']
            sql=f"INSERT INTO PRODUCT (PRODUCTNAME,CATEGORYID,UNIT,PRICE) VALUES ('{escape(pname)}',{escape(catid)},{escape(unit)},{escape(price)})"
            stmt1 = ibm_db.prepare(connection, sql)
            ibm_db.execute(stmt1)
            return redirect(url_for('admin'))





@app.route('/delete/<tablename>/<int:Id>')
def delete(tablename,Id):
  if tablename=='CATEGORY':
    sql=f"SELECT * FROM {escape(tablename)} WHERE CATEGORYID = ?"
    stmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(stmt, 1, Id)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_row(stmt)
    print ("The table Name is : ",  result)
    if result:
        sql1 = f"DELETE FROM {escape(tablename)} WHERE CATEGORYID = {escape(Id)}"
        stmt = ibm_db.exec_immediate(connection, sql1)
        # data = []
        # sql = f"SELECT * FROM {escape(tablename)}"
        # stmt = ibm_db.exec_immediate(connection, sql)
        # dictionary = ibm_db.fetch_both(stmt)
        # while dictionary != False:
        #     data.append(dictionary)
        #     dictionary = ibm_db.fetch_both(stmt)
            # return render_template("admin.html", category = data, deletemsg="True")
        return redirect(url_for('admin'))
        # return "success..."
    else:
        sql=f"SELECT * FROM PRODUCT WHERE PRODUCTID = {escape(str(Id))}"
        print('hi')
        print(tablename)
        stmt = ibm_db.prepare(connection, sql)
        # ibm_db.bind_param(stmt, 1, Id)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_row(stmt)
        print ("The table Name is : ",  result)
        if result:
            sql1 = f"DELETE FROM {escape(tablename)} WHERE PRODUCTID = {escape(Id)}"
            print('hello')
            stmt = ibm_db.exec_immediate(connection, sql1)
            return redirect(url_for('admin'))
        else:
            print("no value")
            return redirect(url_for('admin'))

@app.route('/deleteRec/<int:id>')
def deleteRec(id):
    sql=f"SELECT * FROM PRODUCT WHERE PRODUCTID = ?"
    print("hi")
    stmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(stmt, 1, id)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_row(stmt)
    print ("The table Name is : ",  result)
    if result:
        print("hello")
        sql1 = f"DELETE FROM PRODUCT WHERE PRODUCTID = {escape(id)}"
        stmt = ibm_db.exec_immediate(connection, sql1)
        return redirect(url_for('admin'))

@app.route('/edit/<int:ID>')
def edit(ID):
    return "<h2>Hello "+str(ID)+"</h2>"

@app.route('/pants')
def pants():
    if 'loggedin' in session and 'name' in session:
        return render_template('Pants.html')
    return render_template('login.html')

@app.route('/watch')
def watch():
    if 'loggedin' in session and 'name' in session:
        return render_template('watch.html')    
    return render_template('login.html')
@app.route('/shoes')
def shoes():
    if 'loggedin' in session and 'name' in session:
        return render_template('Shoes.html')
    return render_template('login.html')
   

@app.route('/tshirts')
def tshirts():
    if 'loggedin' in session and 'name' in session:
        return render_template('tshirts.html')
    return render_template('login.html')

    
@app.route('/shirts')
def shirts():
    if 'loggedin' in session and 'name' in session:
        return render_template('Shirts.html')
    return render_template('login.html')


@app.route('/order',methods=['POST','GET'])
def order():
    if request.method=='POST':
        user=request.form['uname']
        quan=request.form['quan']
        amount=request.form['amount']

        total=int(amount)*int(quan)
        uid=session['id']
        sql=f"INSERT INTO ORDER (USERID,AMOUNT) VALUES ({escape(uid)},{escape(total)})"
        stmt=ibm_db.exec_immediate(connection,sql)
        return redirect(url_for('hello'))


if __name__=='__main__':
    app.run(host='0.0.0.0',port="5000")
    # app.run()
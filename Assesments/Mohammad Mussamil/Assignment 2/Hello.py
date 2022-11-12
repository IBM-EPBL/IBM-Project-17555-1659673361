import sqlite3 as sql

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)

app= Flask(__name__)
app.config['DEBUG']=True
app.secret_key="mgyftuiu"

@app.route('/home')
def hello():
     if 'loggedin' in session and 'name' in session:
        return render_template('home.html')
     return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/blog")
def blog():
    return "<h1>Hello World from blog page</h1>"

@app.route("/blog/<int:id>")
def blogId(id):
    return "<h1>Hello World from blog page" +str(id)+"</h1>"

@app.route('/about')
def about():
    return render_template('about.html')

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

            with sql.connect("database.db") as con:
                cur= con.cursor()
                cur.execute('insert into user values(?,?,?,?)',(name,mail,mobile,password))
                con.commit()
                message="User Registered"
                return redirect(url_for('login'))
        except:
            con.rollback()
            message="error"
            return render_template("signup.html",error=message)
    # return jsonify({message})
    # return render_template('signup.html')


@app.route("/check", methods=['POST','GET'])
def check():
    msg=""
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']


        con=sql.connect("database.db")
        con.row_factory=sql.Row

        cur =con.cursor()
        cur.execute("SELECT * FROM user")

        # rows= cur.fetchall()
        cur.execute('SELECT * FROM user where name=? and password=?', (username,password))
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['name'] = account['name']
            return redirect(url_for('hello'))
        else:
            msg = "Incorrect username/password!"
            return render_template('login.html', msg=msg)

        #return render_template("list.html",rows=rows)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('name', None)
   return redirect(url_for('login'))

if __name__=='__main__':
    app.run()
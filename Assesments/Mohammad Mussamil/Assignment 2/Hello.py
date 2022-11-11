from flask import Flask,render_template,url_for

app= Flask(__name__)
app.config['DEBUG']=True

@app.route('/')
def hello():
    return render_template('home.html')

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




if __name__=='__main__':
    app.run()
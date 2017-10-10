from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://bloguser:bloggyboy@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    blogtitle = db.Column(db.String(120))
    blogbody = db.Column(db.String(250))

    def __init__(self, blogtitle, blogbody):
        self.blogtitle = blogtitle
        self.blogbody = blogbody

@app.route('/', methods=['GET', 'POST'])
def index():   
    if request.method == 'POST':
        blog_title = request.form['blogtitle']
        blog_body = request.form['blogbody']

        new_post = Blog(blog_title, blog_body)

        db.session.add(new_post)
        db.session.commit()



@app.route('/blog', methods=['GET'])
def mainblog():

    return render_template('index.html')

@app.route('/newpost', methods='POST')
def newpost():
    blog_title = request.form['blogtitle']
    blog_body = request.form['blogbody']
    
    if blog_title == "" or blog_body == "":
        return render_template('newentry.html', error='Please fill out both fields.')
    
    new_post = Blog(blog_title, blog_body)

    db.session.add(new_post)
    db.session.commit()
    redirect('/blog')

if __name__ == '__main__':
    app.run()

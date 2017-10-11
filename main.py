from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bloguser:bloggyboy@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    blogtitle = db.Column(db.String(120))
    blogbody = db.Column(db.String(250))

    def __init__(self, blogtitle, blogbody):
        self.blogtitle = blogtitle
        self.blogbody = blogbody

@app.route('/', methods=['GET'])
def index():   
    posts = Blog.query.filter_by().all()
    return render_template('index.html', posts=posts)


@app.route('/blog', methods=['GET'])
def mainblog():
    posts = Blog.query.filter_by().all()
    return render_template('index.html', posts=posts)

@app.route('/newpost', methods=['GET'])
def newpost():
    return render_template('newentry.html')

posts = []
@app.route('/newpostlogic', methods=['POST'])
def newpostlogic():
    
    blogtitle = request.form['title']
    blogbody = request.form['body']
    
    if blogtitle == "" or blogbody == "":
        return render_template('newentry.html', error='Please fill out both fields.')
    elif len(blogbody) > 250:
        return render_template('newentry.html', error='Max 250 characters in post.')
   
    posts.append(Blog(blogtitle, blogbody))
    
    for post in posts:
        db.session.add(post)
    db.session.commit()
    newinfo = Blog.query.filter_by().all()
    return redirect("/")

@app.route('/postclicked/', methods=['GET'])
def postclicked():
    postid = request.args.get('id')
    post = Blog.query.filter_by(id=int(postid)).first()
    return render_template('entry.html', post=post)

if __name__ == '__main__':
    app.run()

from datetime import datetime
from app import db,login_manager
from . import main
from .forms import UserForm,NamerForm,LoginForm,PostForm
from ..models import Users,Posts
from flask import Flask, render_template,flash,request,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user




@main.route('/')
def index():
    return render_template("base_index.html")

@main.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)

#create a name page
@main.route('/name',methods=['GET','POST']) #post method needed for page containing forms
def name():
    name = None
    form = NamerForm()
    #validating form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data =''
        flash("Form submitted successfully!")
        
    return render_template("name.html",name=name,form=form)

@main.route('/login',methods=['GET','POST']) #post method needed for page containing forms
def login():
    form = LoginForm()
    #validating form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            # checking the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('main.dashboard'))
                
            else:
                flash("Wrong password -- Try again")
        else:
            flash("That user doesn't exist -- Try again")
    
    else:
        return render_template("login.html",form=form)

@main.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@main.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You are logged out!")
    return render_template("index.html")



@main.route('/add-post', methods = ['POST','GET'])
@login_required
def add_post():
    post = None
    content = None
    slug = None
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data,
        content = form.content.data,
        poster_id = poster,
        slug = form.slug.data,
        )
        form.title.data = ''
        form.content.data = ''
       # form.author.data = ''
        form.slug.data = ''
# Add Log post to database 
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Submitted Sucessfully")
        return render_template("add_post.html",form=form,post=post,content=content,slug=slug)
    else:
        return render_template("add_post.html",form=form,post=post,content=content,slug=slug)
        
   
@main.route('/posts')
@login_required
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html",posts=posts)

@main.route('/post/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Blog post was deleted")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)

        
        
        except:
            flash("There was a problem deleting post..try again")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)

    else:
         flash("Unauthorized Access")
         posts = Posts.query.order_by(Posts.date_posted)
         return render_template("posts.html",posts=posts)



@main.route('/post/edit/<int:id>', methods = ["GET","POST"])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
       # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('main.post',id=post.id))
    
    if current_user.id == post.poster_id:
        form.title.data = post.title
    # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)

    else:
        flash("Unauthorized Access")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)




@main.route('/user/add', methods =['GET','POST'])
def add_user(): 
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password first
            hash_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,email=form.email.data,password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Sucessfully")
    #To display user names on the page 
    our_users = Users.query.order_by(Users.date_added)   
    return render_template('add_user.html',form=form,name=name,our_users=our_users)

#update database
@main.route('/update/<int:id>', methods =['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    # Query the database to retrieve the existing user row
    user = Users.query.get(id)
    form.name.data = user.name
    form.email.data = user.email

    # If the form is being submitted
    if request.method == 'POST':

        # Modify the values of the retrieved user object
        user.name = request.form['name']
        user.email = request.form['email']

        # Hash the new password
        hashed_password = generate_password_hash(request.form['password_hash'], "sha256")
        user.password_hash = hashed_password

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the dashboard page
        return redirect(url_for('main.dashboard'))

    # If the form is being displayed
    else:
        # Render the update template
        return render_template('update.html', user=user, form=form)

@main.route('/delete/<int:id>', methods =['GET','POST'])
@login_required
def delete(id):
    user = db.session.query(Users).get(id)
    form = UserForm(request.form)
    if request.method == "GET":
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Sucessfully")
        return render_template("add_user.html",form=form,user=user)
    
    else:
        return render_template("add_user.html",form=form,user=user)


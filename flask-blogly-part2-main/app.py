"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tags, PostTag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']= 'shhSecret!'

toolbar = DebugToolbarExtension(app)

app.app_context().push()
app.run(debug=True)


connect_db(app)
db.create_all()

# @app.route('/')
# def redirect_page():
#     """redirects home page to user's page"""
#     return redirect('/users')

@app.route('/')
def root():
    """show recent activity of page"""
    
    posts= Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """page not found"""
    return render_template("404.html"), 404

@app.route('/users')
def user_homepage():
    """Show the page with all the users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/index.html', users=users)    

@app.route('/users/new', methods= ['GET'])
def new_user_form():
    """show a form to create a new user"""
    return render_template('users/new.html')

@app.route('/users/new', methods= ['POST'])
def handle_new_user():
    """handle form for new users"""
    
    new_user= User(
        first_name= request.form['first_name'],
        last_name= request.form['last_name'],
        image_url= request.form['image_url'] or None
    )
    
    db.session.add(new_user)
    db.session.commit()
    flash (f"User {new_user.full_name} added.")
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """Show info about the user"""
    
    user= User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user(user_id):
    """uses a form to edit current users"""
    
    user= User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """handle form to update current user"""
    
    user= User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """handles the form to delete current user"""
    
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} has been deleted.")
    
    return redirect('/users')
    
# ////////////////////////////////////////////////////////
# ///POSTS ROUTES
    
@app.route('/users/<int:user_id/posts/new')
def new_post_form():
        """show a new form for a user to make a new post"""
        
        user= User.query.get_or_404(user_id)
        tags= Tags.query.all()
        return render_template('posts/new.html', user=user, tags=tags)
    
@app.route('/users/<int:user_id/posts/new', methods=["POST"])
def new_post(user_id):
        """handle new post"""
        
        user= User.query.get_or_404(user_id)
        tag_ids= [int(num) for num in request.form.getlist('tags')]
        tags = Tags.query.filter(Tag.id.in_(tag_ids)). all()
        
        new_post = Post(title= request.form['title'], content= request.form['content'], user=user, tags=tags)
        
        db.session.add(new_post)
        db.session.commit()
        flash (f"Post '{new_post.title}' added.")
        
        return redirect(f"/users/{user_id}")
    
@app.route('/posts/<int:post_id>')
def show_post(post_id):
        """show a page with info from post"""
        
        post=post.query.get_or_404(post_id)
        return render_template('posts/edit.html', post=post) 
    
@app.route('/posts/<int:user_id/edit')
def edit_posts(post_id):
        """show a form to edit a current post"""
        
        post= Post.query.get_or_404(post_id)
        tags= Tag.query.all()
        return render_template('posts/show.html', post=post)
    
@app.route('/posts/<int:user_id/edit', methods=["POST"])
def update_posts(post_id):
        """handle submission to update a current post"""
        
        post= Post.query.get_or_404(post_id) 
        post.title= request.form['title']
        post.content= request.form['content']
        
        tags_ids= [int(num) for num in request.form.getlist('tags')]
        post.tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()
        
        db.session.add(post)
        db.session.commit()
        flash (f"Post '{post.title}' has been edited.") 
        
        return redirect(f"/users/{post.user_id}")
    
@app.route('/posts/<int:post_id>/delete', methods= ["POST"])
def delete_post(post_id):
        
            post= Post.query.get_or_404(post_id)
            
            db.session.delete(post)
            db.session.commit()
            flash(f"Post '{post.title}' has been deleted.")
            
            return redirect(f"/users/{post.user_id}")
            
#  //////////////////////////////////////////////
# ////TAGS ROUTES
    
@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tags.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tags(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tags.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tags.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tags.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tags.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
        
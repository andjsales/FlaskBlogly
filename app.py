from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# USER HANDELING #######################################


@app.route('/')
def homepage():
    return redirect("/users")


# @app.route('/users')
# def list_users():
#     """
#     Show all users
#     """
#     users = User.query.all()
#     current_user = User.query.get(1)

#     return render_template('users.html', users=users, user=current_user)


@app.route('/users')
def list_users():
    """
    Show all users
    """
    users = User.query.all()
    current_user = User.query.first()
    return render_template('users.html', users=users, user=current_user)


@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    """
    Create a new user profile
    """
    if request.method == "POST":
        first_name = request.form["first_name"].capitalize()
        last_name = request.form["last_name"].capitalize()
        image_url = request.form["image_url"]

        user_new = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
        db.session.add(user_new)
        db.session.commit()
        return redirect('/users')
    else:
        current_user = User.query.first()
        return render_template('user_new.html', user=current_user)


@app.route('/users/<int:user_id>', methods=['GET'])
def show_user(user_id):
    """
    Display user profile
    """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user_info.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """
    Edit user profile
    """
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect('/users')
    return render_template('user_edit.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """
    Delete a user profile
    """
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return render_template('user_delete.html', user=user)

# POST HANDELING ########################################


@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_user_post(user_id):
    """
    - Show display
    - Post submission
    """
    user = User.query.get_or_404(user_id)  # Fetch the user first

    if request.method == "POST":
        post_new = Post(
            title=request.form["title"], content=request.form["content"], user_id=user.id)  # Use user_id if it's a foreign key in Post model
        db.session.add(post_new)
        db.session.commit()
        return redirect(f"/users/{user_id}")

    return render_template('post_new.html', user=user)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_show_post(post_id):
    """
    - Show edit form  
    - Submit changes
    - Cancel button (back to user page)
    """
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(f'/users/{user.id}')

    return render_template('post_edit.html', user=user, post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


if __name__ == '__main__':
    app.debug = True
    app.run()

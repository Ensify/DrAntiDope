from flask import Blueprint,render_template,request,redirect,flash,url_for,abort
from flask_login import login_user, login_required, logout_user, current_user
from website.models import User,Post,Comment
from website.posts.forms import PostForm,CommentForm
from website import bcrypt,db

posts=Blueprint('posts',__name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post= Post(title=form.title.data,content=form.content.data,author=current_user,topic=form.topic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.forum'))
    return render_template("create_post.html",user=current_user,form=form,legend ="New Post")

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    form=CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please login to comment","info")
            return redirect(url_for('users.login'))
        comment= Comment(content=form.content.data,user_id=current_user.id,post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added to the post!')
        return redirect(request.url)
    
    comments= Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('post.html',post=post,user=current_user,form=form,comments=comments)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.topic = form.topic.data
        db.session.commit()
        flash("Post Updated!","success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method =='GET':
        form.title.data= post.title
        form.content.data = post.content
        form.topic.data = post.topic
    return render_template("create_post.html",user=current_user,form=form,legend="Update post")

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.forum'))


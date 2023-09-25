from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_uploads import UploadNotAllowed

from app import app, db
from forms.forms import ProductForm
from models.models import User, Product

login_manager = LoginManager(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )

        if form.image.data:
            try:
                filename = form.image.data.filename
                form.image.data.save('uploads/' + filename)
                product.image = filename
            except :
                flash('Invalid file format. Please upload an image.', 'danger')
                return redirect(url_for('products'))

        db.session.add(product)
        db.session.commit()
        flash('Product created successfully', 'success')
        return redirect(url_for('products'))

    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', form=form, products=products, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_password = request.form['new_password']
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
    return render_template('profile.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('register.html')
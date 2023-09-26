from flask import render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


from app import app, db
from forms.forms import ProductForm
from models.models import User, Product, Order

login_manager = LoginManager(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    product = Product.query.get(product_id)
    # Додати товар до кошика користувача у сесії
    cart = session.get('cart', {})
    cart_item = {
        'name': product.name,
        'description': product.description,
        'quantity': cart.get(product_id, 0) + quantity
    }
    cart[product_id] = cart_item
    session['cart'] = cart

    flash('Product added to cart', 'success')
    return redirect(url_for('products'))

@app.route('/cart')
@login_required
def view_cart():
    # Отримати кошик користувача з сесії та відобразити його
    cart = session.get('cart', {})
    return render_template('cart.html', cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if request.method == 'POST':
        cart = session.get('cart', {})
        for product_id, prod in cart.items():
            product = Product.query.get(product_id)
            if product:
                order = Order(user_id=current_user.id, product_id=product_id, quantity=prod["quantity"])
                db.session.add(order)
        db.session.commit()
        session['cart'] = {}
        flash('Order placed successfully', 'success')
        return redirect(url_for('view_orders'))
    return render_template('checkout.html', cart=cart)

@app.route('/my_orders')
@login_required
def view_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    cart = session.get('cart', {})
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
                form.image.data.save('static/uploads/' + filename)
                product.image = filename
            except :
                flash('Invalid file format. Please upload an image.', 'danger')
                return redirect(url_for('products'))

        db.session.add(product)
        db.session.commit()
        flash('Product created successfully', 'success')
        return redirect(url_for('products'))

    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', form=form, products=products, user=current_user, cart=cart)

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
    cart = session.get('cart', {})
    if request.method == 'POST':
        new_password = request.form['new_password']
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
    return render_template('profile.html', user=current_user, cart=cart)

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
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import PRODUCTS
from forms import LoginForm, RegisterForm
from wtforms.validators import DataRequired, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-me'  # Change in production

USERS = {
    "chandru@example.com": "mypassword",
    "admin@example.com": "admin123"
}

@app.route('/')
def index():
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_products = [
            p for p in PRODUCTS
            if query in p['title'].lower() or query in p['desc'].lower()
        ]
    else:
        filtered_products = PRODUCTS
    return render_template('index.html', products=filtered_products, search_query=query)

@app.route('/like/<int:pid>', methods=['POST'])
def like_product(pid):
    if 'user' not in session:
        flash('Please log in to like products', 'warning')
        return redirect(url_for('login'))
    flash(f'You liked product ID {pid}!', 'success')
    return redirect(url_for('index'))
@app.route('/product/<int:pid>')
def product_detail(pid):
    product = next((x for x in PRODUCTS if x['id'] == pid), None)
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for('index'))
    return render_template('product.html', product=product)
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        flash('Please log in to add items to cart', 'warning')
        return redirect(url_for('login'))

    pid = request.form.get('product_id', type=int)
    qty = request.form.get('quantity', type=int, default=1)

    if not pid:
        flash("Invalid product", "danger")
        return redirect(url_for('index'))

    cart = session.get('cart', {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash('Added to cart', 'success')
    return redirect(request.referrer or url_for('index'))
@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = next((x for x in PRODUCTS if str(x['id']) == pid), None)
        if product:
            subtotal = product['price'] * qty
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', items=items, total=total)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in USERS and USERS[email] == password:
            session['user'] = email
            flash(f'Welcome back, {email}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in USERS:
            flash('Email already registered', 'warning')
        else:
            USERS[email] = password
            session['user'] = email
            flash('Registered and logged in successfully', 'success')
            return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

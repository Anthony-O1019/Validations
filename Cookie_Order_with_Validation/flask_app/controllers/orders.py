from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.modules.order import Order

@app.route('/')
def home_page():
    orders = Order.get_all()
    return render_template('index.html', orders = orders)

@app.route('/addorder')
def add_order():
    return render_template('order.html')

@app.route('/create_order', methods=["POST"])
def process():
    if not Order.validate_order(request.form):
        return redirect('/addorder')
    data = {
        "name": request.form["name"],
        "cookie_type": request.form["cookie_type"],
        "number_of_boxes": request.form["number_of_boxes"]
    }
    print(data)
    Order.save_order(data)
    return redirect('/addorder')

@app.route('/update_order/<int:order_id>', methods=["POST"])
def update(order_id):
    if not Order.validate_order(request.form):
        return redirect(f'/editorder/{order_id}')
    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "cookie_type": request.form["cookie_type"],
        "number_of_boxes": request.form["number_of_boxes"]
    }
    print(data)
    Order.update_order(data)
    return redirect('/')

@app.route('/editorder/<int:order_id>')
def edit_order(order_id):
    order = Order.single_id(order_id)

    return render_template('change.html', order = order)
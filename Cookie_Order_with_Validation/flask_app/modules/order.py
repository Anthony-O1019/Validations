from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('girl_scouts').query_db(query)
        orders = []
        for order in results:

            orders.append( cls(order)) 
        return orders

    @classmethod
    def single_id(cls, order_id):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        data = {
            "id": order_id
        }
        result = connectToMySQL('girl_scouts').query_db(query,data)
        if result:
            order = result[0]
            return order

    @classmethod
    def save_order(cls, data):
        query = "INSERT INTO orders (name, cookie_type, number_of_boxes) VALUES (%(name)s, %(cookie_type)s, %(number_of_boxes)s);"

        return connectToMySQL('girl_scouts').query_db(query, data)
    
    @classmethod
    def update_order(cls, data):
        query = "UPDATE orders SET name = %(name)s, cookie_type = %(cookie_type)s, number_of_boxes = %(number_of_boxes)s WHERE id = %(id)s;"

        return connectToMySQL('girl_scouts').query_db(query,data)
    @classmethod
    def validate_order(cls,order):
        is_valid = True
        if len(order['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(order['cookie_type']) < 3:
            flash("Invalid Cookie Type")
            is_valid = False
        if int(order['number_of_boxes']) < 1:
            flash("Please purchase at least 1 box.")
            is_valid = False
        return is_valid
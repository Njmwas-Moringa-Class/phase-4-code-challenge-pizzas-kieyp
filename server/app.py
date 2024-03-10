#!/usr/bin/env python3
import os
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify

# Importing os module is unnecessary if you're not using it later in the script
# Same goes for make_response import, it's not used

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate = Migrate(app, db)

# Initializing the app with the database
db.init_app(app)

# Define routes

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        # Ensure you're returning a valid JSON response with status code 200
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    except Exception as e:
        # Handle any unexpected errors gracefully
        return jsonify({"error": str(e)}), 500

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify(restaurant.to_dict(include_pizzas=True)), 200
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    try:
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/restaurant_pizzas', methods=['POST'])
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        price = request.json.get('price')
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")

        new_restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=request.json.get('pizza_id'),
            restaurant_id=request.json.get('restaurant_id'),
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Retrieve the associated pizza and restaurant
        pizza = Pizza.query.get(new_restaurant_pizza.pizza_id)
        restaurant = Restaurant.query.get(new_restaurant_pizza.restaurant_id)

        return jsonify({
            'id': new_restaurant_pizza.id,
            'price': new_restaurant_pizza.price,
            'pizza': pizza.to_dict(),
            'pizza_id': new_restaurant_pizza.pizza_id,
            'restaurant': restaurant.to_dict(),
            'restaurant_id': new_restaurant_pizza.restaurant_id
        }), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Make sure to run the app with debug mode off in production
    app.run(port=5555, debug=True)

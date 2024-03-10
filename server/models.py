from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', backref=db.backref('restaurants', lazy=True))

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant_pizzas', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('restaurant_pizzas', lazy=True))

    def __init__(self, price, pizza_id, restaurant_id):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30")
        self.price = price
        self.pizza_id = pizza_id
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'

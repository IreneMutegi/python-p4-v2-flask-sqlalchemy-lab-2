from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Customer model with serialization
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # Define the serialization rules to avoid recursion
    serialize_rules = ('-reviews.customer',)  # Exclude 'customer' in 'reviews' to avoid recursion

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = relationship('Review', back_populates='customer')
    # Add the association proxy for 'items'
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# Item model with serialization
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    # Define the serialization rules to avoid recursion
    serialize_rules = ('-reviews.item',)  # Exclude 'item' in 'reviews' to avoid recursion

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# Review model with serialization
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    # Define the serialization rules to avoid recursion
    serialize_rules = ('-customer.reviews', '-item.reviews')  # Exclude 'reviews' to avoid recursion in 'customer' and 'item'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.customer_id}, {self.item_id}, {self.comment}>'

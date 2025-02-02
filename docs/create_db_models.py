# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class Customer(Base):
    """description: Stores customer details, including basic contact and account information."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, default=0.0)


class Product(Base):
    """description: Contains details about the products that are available for order."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    unit_price = Column(Float, nullable=True)
    stock_quantity = Column(Integer, nullable=True)


class Order(Base):
    """description: Represents customer orders, storing information about the order and its fulfillment status."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now)
    date_shipped = Column(DateTime, nullable=True)
    amount_total = Column(Float, default=0.0)


class OrderDetail(Base):
    """description: Items within an order, detailing the product, quantity, and pricing."""
    __tablename__ = 'order_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    amount = Column(Float, default=0.0)


class Supplier(Base):
    """description: Provides information about suppliers who supply products to the store."""
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    phone = Column(String, nullable=True)


class Inventory(Base):
    """description: Manages product inventory, tracking stock levels and restocks."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    quantity_on_hand = Column(Integer, default=0)
    restock_level = Column(Integer, default=10)
    restock_amount = Column(Integer, default=50)


class Shipment(Base):
    """description: Details about shipments to customers, including carrier and tracking information."""
    __tablename__ = 'shipment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    shipment_date = Column(DateTime, nullable=True)
    carrier = Column(String, nullable=True)
    tracking_number = Column(String, nullable=True)
    delivered = Column(Boolean, default=False)


class Invoice(Base):
    """description: Invoices generated for customer orders, including total and status information."""
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    date_issued = Column(DateTime, default=datetime.datetime.now)
    total_amount = Column(Float, nullable=True)
    paid = Column(Boolean, default=False)


class Payment(Base):
    """description: Records customer payments against invoices."""
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now)
    amount = Column(Float, nullable=True)
    payment_method = Column(String, nullable=True)


class Category(Base):
    """description: Product categories for organizing the product catalog."""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)


class ProductCategory(Base):
    """description: Junction table associating products with categories."""
    __tablename__ = 'product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


class Review(Base):
    """description: Customer reviews of products."""
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    review_date = Column(DateTime, default=datetime.datetime.now)
    rating = Column(Integer, nullable=True)
    comments = Column(Text, nullable=True)


# Simplified engine creation without commit
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Session for data population
Session = sessionmaker(bind=engine)
session = Session()

# Inserting sample data
customer1 = Customer(name='John Doe', email='john.doe@example.com', phone='123-456-7890', balance=150.0, credit_limit=1000.0)
customer2 = Customer(name='Jane Smith', email='jane.smith@example.com', phone='987-654-3210', balance=50.0, credit_limit=500.0)
session.add_all([customer1, customer2])

product1 = Product(name='Widget', unit_price=10.0, stock_quantity=100)
product2 = Product(name='Gadget', unit_price=20.0, stock_quantity=50)
session.add_all([product1, product2])

order1 = Order(customer_id=1, amount_total=150.0)  # Assuming id based on insertion order
order2 = Order(customer_id=2, amount_total=40.0)
session.add_all([order1, order2])

order_detail1 = OrderDetail(order_id=1, product_id=1, quantity=3, unit_price=10.0, amount=30.0)
order_detail2 = OrderDetail(order_id=2, product_id=2, quantity=2, unit_price=20.0, amount=40.0)
session.add_all([order_detail1, order_detail2])

supplier1 = Supplier(name='SupplyCo', contact_name='Alice', contact_email='alice@supplyco.com', phone='555-555-5555')
session.add(supplier1)

inventory1 = Inventory(product_id=1, supplier_id=1, quantity_on_hand=70)
inventory2 = Inventory(product_id=2, supplier_id=1, quantity_on_hand=30)
session.add_all([inventory1, inventory2])

shipment1 = Shipment(order_id=1, shipment_date=datetime.datetime.now(), carrier='FastShip', tracking_number='123ABC')
shipment2 = Shipment(order_id=2, shipment_date=datetime.datetime.now(), carrier='Speedy', tracking_number='456DEF')
session.add_all([shipment1, shipment2])

invoice1 = Invoice(order_id=1, total_amount=150.0)
invoice2 = Invoice(order_id=2, total_amount=40.0)
session.add_all([invoice1, invoice2])

payment1 = Payment(invoice_id=1, amount=150.0, payment_method='Credit Card')
payment2 = Payment(invoice_id=2, amount=40.0, payment_method='PayPal')
session.add_all([payment1, payment2])

category1 = Category(name='Electronics', description='Electronic items')
category2 = Category(name='Household', description='Household items')
session.add_all([category1, category2])

product_category1 = ProductCategory(product_id=1, category_id=1)
product_category2 = ProductCategory(product_id=2, category_id=2)
session.add_all([product_category1, product_category2])

review1 = Review(product_id=1, customer_id=1, rating=5, comments='Great product!')
review2 = Review(product_id=2, customer_id=2, rating=4, comments='Very useful.')
session.add_all([review1, review2])

session.commit()
session.close()

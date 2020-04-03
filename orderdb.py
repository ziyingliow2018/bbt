import sys
import os
import random
import datetime
from flask import Flask
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Date
import requests
import telebot
import json

import pika
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bubbletea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
 
# create Order class
class Order(db.Model):
    __tablename__ = 'order'
 
    orderid = db.Column(db.String(13), primary_key=True, nullable=False)
    base = db.Column(db.String(100), nullable=False)
    toppings = db.Column(db.String(200), nullable=False)
    totalprice = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(15), nullable=False)
 
    def __init__(self, orderid, base, toppings, totalprice, status):
        self.orderid = orderid
        self.base = base
        self.toppings = toppings
        self.totalprice = totalprice
        self.status = status
 
    def json(self):
        return {"orderid": self.orderid, "base": self.base, 
        "toppings": self.toppings,"totalprice": self.totalprice, "status": self.status}
 

# returns all orders
@app.route("/order")
def get_all():
    return jsonify({"orders": [order.json() for order in Order.query.all()]})
 
# returns order by orderid
@app.route("/order/<string:orderid>")
def find_by_orderid(orderid):
    order = Order.query.filter_by(orderid=orderid).first()
    if order:
        return jsonify(order.json())
    return jsonify({"message": "Order not found."}), 404

# POST an order
@app.route("/order/<string:orderid>", methods=['POST'])
def create_order(orderid):
    status = 201
    result = {}
    if (Order.query.filter_by(orderid=orderid).first()):
        return jsonify({"message": "A order with orderid '{}' already exists.".format(orderid)}), 400
    
    data = request.get_json()
    order = Order(orderid, **data)
    if status == 201:
        try:
            db.session.add(order)
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred creating the order."}), 500
    
    if status == 201:
        result = order.json()
    send_order(result)
    return jsonify(order.json()), status



# Update an order
@app.route("/order/<string:orderid>", methods=['PUT'])
def update_status(orderid):
    order_update = Order.query.filter_by(orderid=orderid).first()
    order_update.status = 'Completed'
    db.session.commit()
    
    if (order_update):
        orderdetails = order_update.base + ' with ' + order_update.toppings

        token = '1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk'

        chat_id = '254976991'
        send_text_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=NRIC+Number:+{orderid},+{orderdetails},+is+ready+for+collection!++Thank+You+for+waiting!+:)'
        requests.get(send_text_url)
        return jsonify({"data":order_update.json()}), 200
        
    return jsonify({"message": "Order not found."}), 404


###




def send_order(order):
    """inform Notification/Monitoring/Error as needed"""
    hostname = "localhost" # default broker hostname. 
    port = 5672 # default messaging port.
    
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
      
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="bbtorder_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps('Order Creation Successful!!!!', default=str) # convert a JSON object to a string

    # send the message
    # always inform Monitoring for logging
    channel.basic_publish(exchange=exchangename, routing_key="monitoring.info", body=message)
  
    print("Order sent to monitoring.")
    # close the connection to the broker
    connection.close()

# get data from orderdb
serviceURL= "http://127.0.0.1:5001/order"


if __name__ == '__main__':
    print("This is " + os.path.basename(__file__) + ": receiving an order...")
    app.run(port=5001, debug=True)
    

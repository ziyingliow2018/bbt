import sys
import os
import random
import datetime
from flask import Flask
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flaskext.mysql import MySQL
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
 
class Order(db.Model):
    __tablename__ = 'order'
 
    orderid = db.Column(db.String(13), primary_key=True, nullable=False)
    base = db.Column(db.String(100), nullable=False)
    # datetime = db.Column(db.TimeStamp, nullable=False)
    toppings = db.Column(db.String(200), nullable=False)
    totalprice = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(15), nullable=False)
 
    def __init__(self, orderid, base, toppings, totalprice, status):
        self.orderid = orderid
        self.base = base
        # self.datetime = datetime
        self.toppings = toppings
        self.totalprice = totalprice
        self.status = status
 
    def json(self):
        return {"orderid": self.orderid, "base": self.base, 
        "toppings": self.toppings,"totalprice": self.totalprice, "status": self.status}
 
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'bubbletea'
# mysql = MySQL(app)

# @app.route('/hello')
# def index():
#    cur = mysql.connection.cursor()
#    cur.execute('''SELECT * FROM order''')
#    row_headers=[x[0] for x in cur.description] #this will extract row headers
#    rv = cur.fetchall()
#    json_data=[]
#    for result in rv:
#         json_data.append(dict(zip(row_headers,result)))
#    return json.dumps(json_data)

@app.route("/order")
def get_all():
    return jsonify({"orders": [order.json() for order in Order.query.all()]})
 
@app.route("/order/<string:orderid>")
def find_by_orderid(orderid):
    order = Order.query.filter_by(orderid=orderid).first()
    if order:
        return jsonify(order.json())
    return jsonify({"message": "Order not found."}), 404


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



###

@app.route("/order/<string:orderid>", methods=['PUT'])
def update_status(orderid):
    order_update = Order.query.filter_by(orderid=orderid).first()
    order_update.status = 'Completed'
    db.session.commit()
    
    if (order_update):
        orderdetails = order_update.base + ' with ' + order_update.toppings
        #xs bot
        # token = '1118152555:AAHxrro7MkFKmrQp1cIvJ17Oq1wF0p4v_Uk' 
        #zh bot
        token = '1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk'
        #idp grp
        # chat_id = '-1001240530419'
        # #zh tele
        chat_id = '254976991'
        send_text_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=NRIC+Number:+{orderid},+{orderdetails},+is+ready+for+collection!++Thank+You+for+waiting!+:)'
        requests.get(send_text_url)
        return jsonify({"data":order_update.json()}), 200
        
    return jsonify({"message": "Order not found."}), 404


###




def send_order(order):
    """inform Notification/Monitoring/Error as needed"""
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="bbtorder_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps('Order Creation Successful!!!!', default=str) # convert a JSON object to a string

    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="monitoring.info", body=message)
        # By default, the message is "transient" within the broker;
        #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
        # If need durability of a message, need to declare the queue in the sender (see sample code below).

    # if "status" in order: # if some error happened in order creation
    #     # inform Error handler
    #     print("There has been an error.")
    # else: 
    # inform Notification and exit
        # prepare the channel and send a message to Monitoring
    # channel.queue_declare(queue='monitoring', durable=True) # make sure the queue used by Shipping exist and durable
    # channel.queue_bind(exchange=exchangename, queue='monitoring', routing_key='monitoring.info') # make sure the queue is bound to the exchange
    # channel.basic_publish(exchange=exchangename, routing_key="monitoring.info", body=message,
    #     properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
    #     )
    # )
    print("Order sent to monitoring.")
    # close the connection to the broker
    connection.close()

# orders = get_everything()
#orders = index()
# create_order(orders)
serviceURL= "http://127.0.0.1:5001/order"


if __name__ == '__main__':
    print("This is " + os.path.basename(__file__) + ": recieving an order...")
    # send_order(order)
    app.run(port=5001, debug=True)
    

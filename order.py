
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
import random
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika
import mysql.connector

StaffUIURL = "http://localhost:5002/staff_UI"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  passwd='',
  database='bubbletea'
)

mycursor = mydb.cursor()

sql = 'SELECT * FROM order'

try:
    curser.execute(sql)
    results = mycursor.fetchall()

    orders = []

    for row in results:
        orderid = row[0]
        base = row[1]
        datetime = row[2]
        toppings = row[3]
        totalprice = row[4]
        status = row[5]
        order = [orderid, base, datetime, toppings, totalprice, status]
        orders.append(order)

    return results
except:
    print("Unable to fetch data")
mydb.close()

# class Order(db.Model):
#     __tablename__ = 'order'

#     orderid = db.Column(db.String(13), primary_key=True)
#     base = db.Column(db.String(100), nullable=False)
#     datetime = db.Column(db.Date, nullable=False)
#     toppings = db.Column(db.String(200), nullable=True)
#     totalprice = db.Column(db.Float(precision=2),nullable=False)
#     status = db.Column(db.String(20), nullable=False)

#     def __init__(orderid, base, datetime, toppings, totalprice, status):
#         self.orderid = orderid
#         self.base = base
#         self.dateime = datetime
#         self.toppings = toppings
#         self.totalprice = totalprice
#         self.status = status

#     def json(self):
#         return {"orderid": self.orderid, "base": self.base, "datetime": self.datetime, "toppings":self.toppings, "totalprice":self.totalprice, "status":self.status}

# def get_all_orders():
#     return jsonify({"orders": [order.json() for order in order.query.all()]})

# def orders_json():
#     """return all orders as a JSON object (not a string)"""
#     return Order.orders
    
# def orders_save(orders_file):
#     """ save all orders to a file"""
#     with open(orders_file, 'w') as order_json_outfile:
#         json.dump(Order.orders, order_json_outfile, indent=2, default=str) # convert a JSON object to a string
#     order_json_outfile.close()

# def find_by_order_id(order_id):
#     """Return an order (orders) of the order_id"""
#     order = [ o for o in Order.orders["orders"] if o["order_id"]==order_id ]
#     if len(order)==1:
#         return order[0]
#     elif len(order)>1:
#         return {'message': 'Multiple orders found for id ' + str(order_id), 'orders': order}
#     else:
#         return {'message': 'Order not found for id ' + str(order_id)}
 
def create_order(order_input):
    """Create a new order according to the order_input"""
    # assume status==200 indicates success
    status = 200
    message = "Success"

    # Load the order info from a cart (from a file in this case; can use DB too, or receive from HTTP requests)
    try:
        with open(order_input) as sample_order_file:
            cart_order = json.load(sample_order_file)
    except:
        status = 501
        message = "An error occurred in loading the order cart."
    finally:
        sample_order_file.close()
    if status!=200:
        print("Failed order creation.")
        return {'status': status, 'message': message}

    # Create a new order: set up data fields in the order as a JSON object (i.e., a python dictionary)
    order = dict()
    order["orderid"] = Order.last_order_id + 1
    order["base"] = []
    order["datetime"] = datetime.datetime.now()
    order["toppings"] = []
    order["totalprice"] = []
    order["status"] = []
    for index, ci in enumerate(cart_item):
        order["order_item"].append({"orderid": cart_item[index]['orderid'],
                                "base": cart_item[index]['base'],
                                "toppings": index + 1,
                                "order_id": order["order_id"]
        })
    # check if order creation is successful
    if len(order["order_item"])<1:
        status = 404
        message = "Empty order."
    # Simulate other errors in order creation via a random bit
    result = bool(random.getrandbits(1))
    if not result:
        status = 500
        message = "A simulated error occurred when creating the order."

    if status!=200:
        print("Failed order creation.")
        return {'status': status, 'message': message}

    # Append the newly created order to the existing orders
    Order.orders["orders"].append(order)
    # Increment the last_order_id; if using a DB, DBMS can manage this
    Order.last_order_id = Order.last_order_id + 1
    # Write the newly created order back to the file for permanent storage; if using a DB, this will be done by the DBMS
    orders_save("orders.new.json")

    # Return the newly created order when creation is succssful
    if status==200:
        print("OK order creation.")
        return order

def send_order(order):
    # inform Shipping
    r = requests.post(StaffUIURL, json = order)
    print("Order sent to staff_UI.")
    print(">> Response from staff_UI {}".format(r))
    result = json.loads(r.text.lower())
    # check/print shipping's result

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
    message = json.dumps(order, default=str) # convert a JSON object to a string

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
    channel.queue_declare(queue='notification', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='notification', routing_key='notification.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="notification.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
        )
    )
    print("Order sent to notfication.")
    # close the connection to the broker
    connection.close()

#var orders = object()
orders = get_all_orders()
serviceURL= "http://127.0.0.1:5000/order"




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": creating an order...")
    # order = create_order("sample_order.txt")
    send_order(results)
#    print(get_all())
#    print(find_by_order_id(3))

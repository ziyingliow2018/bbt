#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
import random
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from sqlalchemy import Date
import pika
# import telegram


# global TOKEN
# TOKEN = '1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk'

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bubbletea'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# CORS(app)
 
# class Order(db.Model):
#     __tablename__ = 'order'
 
#     orderid = db.Column(db.String(13), primary_key=True)
#     base = db.Column(db.String(100), nullable=False)
#     # datetime = db.Column(db.TimeStamp, nullable=False)
#     toppings = db.Column(db.String(200), nullable=False)
#     totalprice = db.Column(db.Float(precision=2), nullable=False)
#     status = db.Column(db.String(15), nullable=False)
 
#     def __init__(self, orderid, base, toppings, totalprice, status):
#         self.orderid = orderid
#         self.base = base
#         # self.datetime = datetime
#         self.toppings = toppings
#         self.totalprice = totalprice
#         self.status = status
 
#     def json(self):
#         return {"orderid": self.orderid, "base": self.base, 
#         "toppings": self.toppings,"totalprice": self.totalprice, "status": self.status}
 

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="order_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

def receiveOrder():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="notification", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='shipping.order') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order by " + __file__)
    result = processOrder(json.loads(body))
    # print processing result; not really needed
    json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator

   
def processOrder(order):
    print("Processing an order:")
    print(order)
    # Can do anything here. E.g., publish a message to the error handler when processing fails.
    resultstatus = bool(random.getrandbits(1)) # simulate success/failure with a random True or False
    result = {'status': resultstatus, 'message': 'Simulated random shipping result.', 'order': order}
    resultmessage = json.dumps(result, default=str) # convert the JSON object to a string
    if not resultstatus: # inform the error handler when shipping fails
        print("Failed order made.")
        send_error(resultmessage)
    else:
        print("OK order received.")
    return result

def send_error(resultmessage):
    # send the message to the eror handler
    channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
    channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='shipping.error') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=resultmessage,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    )



# @app.route('/{}'.format(TOKEN), methods=['POST'])
# def send_telegram(orderid):
#     send_text = 'https://api.telegram.org/bot1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk/sendMessage?chat_id=-438700758&text=' + 'Order ID' + orderid +'is+ready+for+collection!'
#     response = requests.post(send_text)
#     return response.json()




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": shipping for an order...")
    app.run(threaded=True)
    receiveOrder()
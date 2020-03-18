
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
import random
import datetime

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.

class Order:
    # Load existing orders from a JSON file (for simplicity here). In reality, orders will be stored in DB. 
    with open('orders.json') as order_json_file:
        orders = json.load(order_json_file)
    order_json_file.close()

    # Find the max of all existing "order_id" to be used as the last order_id; if in actual DB, the uniqueness of "order_id" will be managed by DBMS
    last_order_id = max([ o["order_id"] for o in orders["orders"] ])

def orders_json():
    """return all orders as a JSON object (not a string)"""
    return Order.orders
    
def orders_save(orders_file):
    """ save all orders to a file"""
    with open(orders_file, 'w') as order_json_outfile:
        json.dump(Order.orders, order_json_outfile, indent=2, default=str) # convert a JSON object to a string
    order_json_outfile.close()

class Order_Item:
    def __init__(self):
        self.OrderID = 0
        # self.CustomerID = 0
        self.Datetime = 0
        self.Base = ''
        self.Toppings = ''
        self.TotalPrice = ''
        self.Status = ''

    # return an order item as a JSON object
    def json(self):
        return {'OrderID': self.OrderID, 'Datetime': self.Datetime, 'Base': self.Base, 'Toppings': self.Toppings, 'TotalPrice': self.TotalPrice,'Status': self.Status}

 
@app.route("/tables")
def get_all():
    """Return all orders as a JSON object"""
    return Order.orders
 
def find_by_order_id(OrderID):
    """Return an order (orders) of the order_id"""
    order = [ o for o in Order.orders["orders"] if o["OrderID"]==OrderID ]
    if len(order)==1:
        return order[0]
    elif len(order)>1:
        return {'message': 'Multiple orders found for id ' + str(OrderID), 'orders': order}
    else:
        return {'message': 'Order not found for id ' + str(OrderID)}
 
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

    # ***Create a new order: set up data fields in the order as a JSON object (i.e., a python dictionary)
    order = dict()
    # order["customer_id"] = cart_order['customer_id']
    order["order_id"] = Order.last_order_id + 1
    order["timestamp"] = datetime.datetime.now()
    order["order_item"] = []
    #idontunds
    for index, ci in enumerate(cart_item):
        order["order_item"].append({"order_id": order["order_id"],
                                "timestamp": order["timestamp"],
                                "order_item": cart_item[index]['quantity'],
                                "item_id": index + 1,
                                
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
    """inform Shipping/Monitoring/Error as needed"""
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="order_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps(order, default=str) # convert a JSON object to a string

    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="shipping.info", body=message)
        # By default, the message is "transient" within the broker;
        #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
        # If need durability of a message, need to declare the queue in the sender (see sample code below).

    if "status" in order: # if some error happened in order creation
        # inform Error handler
        channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
        channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='shipping.error') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=message,
            properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        )
        print("Order status ({:d}) sent to error handler.".format(order["status"]))
    else: # inform Monitoring and exit
        # prepare the channel and send a message to Monitoring
        channel.queue_declare(queue='monitoring', durable=True) # make sure the queue used by Shipping exist and durable
        channel.queue_bind(exchange=exchangename, queue='monitoring', routing_key='monitoring.order') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="monitoring.order", body=message,
            properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            )
        )
        print("Order sent to monitoring.")
    # close the connection to the broker
    connection.close()


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": creating an order...")
    order = create_order("sample_order.txt")
    send_order(order)
#    print(get_all())
#    print(find_by_order_id(3))

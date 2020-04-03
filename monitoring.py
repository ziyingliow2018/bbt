import json
import sys
import os
import random
import pika



def receiveOrderLog():
    hostname = "localhost" # default hostname
    port = 5672 # default port

    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
   
    channel = connection.channel()
    # set up the exchange if the exchange doesn't exist
    exchangename="bbtorder_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="monitoring", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='monitoring.info') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) 
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming() 



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("A New Order Successfully created.")
    print(order)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": monitoring order creation...")
    receiveOrderLog()

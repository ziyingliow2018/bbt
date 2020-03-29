import json
import sys
import os
import random
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Date

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
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bubbletea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
 
class order(db.Model):
    __tablename__ = 'order'
 
    orderid = db.Column(db.String(13), primary_key=True)
    base = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.Date, nullable=False)
    toppings = db.Column(db.String(200), nullable=False)
    totalprice = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(15), nullable=False)
 
    def __init__(self, orderid, base, datetime, toppings, totalprice, status):
        self.orderid = orderid
        self.base = base
        self.datetime = datetime
        self.toppings = toppings
        self.totalprice = totalprice
        self.status = status
 
    def json(self):
        return {"orderid": self.orderid, "base": self.base, "datetime": self.datetime, 
        "toppings": self.toppings,"totalprice": self.totalprice, "status": self.status}

def get_all_orders():
    return jsonify({"orders": [order.json() for order in order.query.all()]})
 
@app.route("/order")
def get_all():
    return jsonify({"orders": [order.json() for order in order.query.all()]})
 
 
@app.route("/order/<string:orderid>")
def find_by_orderid(orderid):
    single_order = order.query.filter_by(orderid=orderid).first()
    if order:
        return jsonify(single_order.json())
    return jsonify({"message": "Order not found."}), 404


# @app.route("/order/<string:orderid>", methods=['POST'])
# def create_order(orderid):
#     if (order.query.filter_by(orderid=orderid).first()):
#         return jsonify({"message": "A order with '{}' already exists.".format(orderid)}), 400
 
#     data = request.get_json()
#     order = order(orderid, **data)
 
#     try:
#         db.session.add(order)
#         db.session.commit()
#     except:
#         return jsonify({"message": "An error occurred creating the order."}), 500
 
#     return jsonify(order.json()), 201

# @app.route("/order/<string:orderid>", methods=['PUT'])
# def update_order(orderid):
#     return order.query.update(order).values(status = 'Completed').where(order.columns.orderid == orderid)
#     # stmt = order.update().where(order.c.orderid== orderid).values(status = 'Completed')
#     # return stmt


@app.route("/order/<string:orderid>", methods=['PUT'])
def update_status(orderid):
    order_update = order.query.filter_by(orderid=orderid).first()
    order_update.status = 'Completed'
    db.session.commit()
    
    if (order_update):
        # If the order is valid I return a msg --- ask your team decide 1
        # return jsonify({"message":"Successfully updated order."}), 200

        # if the order is valid i return the order. --- ask your team decide 1
        return jsonify({"data":order_update.json()}), 200
        
    return jsonify({"message": "Order not found."}), 404

orders = get_all_orders()
serviceURL= "http://127.0.0.1:5000/order"
   
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




# @app.route('/{}'.format(TOKEN), methods=['POST'])
# def send_telegram(orderid):
#     send_text = 'https://api.telegram.org/bot1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk/sendMessage?chat_id=-438700758&text=' + 'Order ID' + orderid +'is+ready+for+collection!'
#     response = requests.post(send_text)
#     return response.json()




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": shipping for an order...")
    app.run(threaded=True)
    receiveOrder()

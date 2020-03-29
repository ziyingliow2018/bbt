from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Date
import requests
import telebot
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bubbletea'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
 
class Order(db.Model):
    __tablename__ = 'order'
 
    orderid = db.Column(db.String(13), primary_key=True)
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
    if (Order.query.filter_by(orderid=orderid).first()):
        return jsonify({"message": "A order with orderid '{}' already exists.".format(orderid)}), 400
 
    data = request.get_json()
    order = Order(orderid, **data)
 
    try:
        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the order."}), 500
 
    return jsonify(order.json()), 201


@app.route("/order/<string:orderid>", methods=['PUT'])
def update_status(orderid):
    order_update = Order.query.filter_by(orderid=orderid).first()
    order_update.status = 'Completed'
    db.session.commit()
    
    if (order_update):
        # If the order is valid I return a msg --- ask your team decide 1
        # return jsonify({"message":"Successfully updated order."}), 200

        # if the order is valid i return the order. --- ask your team decide 1
        return jsonify({"data":order_update.json()}), 200
        token = '1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk'
        chat_id = '-438700758'
        # send_text_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=Order+is+ready+for+collection!'
        send_text_url = 'https://api.telegram.org/bot1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk/sendMessage?chat_id=-438700758&text=order+is+ready+for+collection!'
        return requests.post(send_text_url)
        # bot.send_message(chat_id, msg)
        # send_text = 'https://api.telegram.org/bot1010659472:AAHL0PoXGBMKB8-mHY8YDPitOTC6U7j0kwk/sendMessage?chat_id=-438700758&text=' + 'Order ID' + orderid +'is+ready+for+collection!'
        # response = requests.post(send_text)
        
    return jsonify({"message": "Order not found."}), 404




if __name__ == '__main__':
    app.run(port=5000, debug=True)
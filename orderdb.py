from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Date

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

 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
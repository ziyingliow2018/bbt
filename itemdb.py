from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bubbletea'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)
 
# create a class item
class item(db.Model):
    __tablename__ = 'item'
 
    itemid = db.Column(db.String(10), primary_key=True)
    itemname = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    type = db.Column(db.String(20), nullable=False)
   
    def __init__(self, itemid, itemname, price,type):
        self.itemid = itemid
        self.itemname = itemname
        self.price = price
        self.type = type
 
    def json(self):
        return {"itemid": self.itemid, "itemname": self.itemname, "price": self.price, "type":self.type}

# retrive all items from itemdb
@app.route("/item")
def get_all():
    return jsonify({"items": [item.json() for item in item.query.all()]})

# retrieve an item by itemid
@app.route("/item/<string:itemid>")
def find_by_itemid(itemid):
    single_item = item.query.filter_by(itemid=itemid).first()
    if item:
        return jsonify(single_item.json())
    return jsonify({"message": "Item not found."}), 404

# run docker to run itemdb
## docker pull ziying123/itemdb:1.0.0
## docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/bubbletea <dockerid>/itemdb:1.0.0
# port: 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

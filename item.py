from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/item'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Item(db.Model):
    __tablename__ = 'Item'
    ItemID = db.Column(db.Integer, primary_key = True)
    ItemName = db.Column(db.String(64), nullable = False)
    Price = db.Column(db.Float(precision=2), nullable = False)

    def __init__(self, ItemID, ItemName, Price):
        self.ItemID = ItemID
        self.ItemName = ItemName
        self.Price = Price

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}

@app.route("/item")
def get_all():
    return jsonify({"items": [Item.json() for item in Item.query.all()]})

@app.route("/item/<integer:ItemID>")
def find_by_ItemID(ItemID):
    Item = Item.query.filter_by(ItemID=ItemID).first()
    if Item:
        return jsonify(Item.json())

    return jsonify({"message": "Item not found."}), 404

#@app.route("/item/<integer:ItemID>", methods=['GET'])
#def create_book(isbn13):
    #if (Book.query.filter_by(isbn13=isbn13).first()):
        #return jsonify({"message": "A book with isbn13 '{}' already exists.".format(isbn13)}), 400
    
    #data = request.get_json()
    #book = Book(isbn13, **data)

    #try:
        #db.session.add(book)
        #db.session.commit()
    #except:
        #return jsonify({"message": "An error occurred creating the book."}), 500
    
    #return jsonify(book.json()), 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
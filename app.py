from flask import Flask, jsonify, request
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB connection
client = MongoClient('20.166.164.119:27017')
db = client['bookstore']
books = db['books']

# Route to get all books
@app.route('/books', methods=['GET'])
def all_books():
    return jsonify(list(books.find({}, {"_id": 0})))

# Route to get a specific book by ISBN
@app.route('/books/<string:isbn>', methods=['GET'])
def get_book(isbn):
    book = books.find_one({"isbn": isbn}, {"_id": 0})
    return jsonify(book) if book else jsonify({"message": "Book not found"}), 404

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    books.insert_one(new_book)
    return jsonify({"message": "Book added successfully"}), 201

# Route to update a book by ISBN
@app.route('/books/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    updated_book = request.get_json()
    books.update_one({"isbn": isbn}, {"$set": updated_book})
    return jsonify({"message": "Book updated successfully"})

# Route to delete a book by ISBN
@app.route('/books/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books.delete_one({"isbn": isbn})
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)


from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json
from settings import *
from BookModel import *

# books = [
# 	{
# 		'name': 'Suresh',
# 		'isbn': 123456789,
# 		'price': '100 rupee'
# 	},
# 	{
# 		'name': 'Kansujiya',
# 		'isbn': 987654321,
# 		'price': '200 rupee'
# 	}
# ]

# print(__name__)

def validBookObject(bookObject):
	print(bookObject)
	if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
	else:
		return False

def validBookObjectForReplace(bookObject):
	print(bookObject)
	if ("name" in bookObject and "price" in bookObject):
		return True
	else:
		return False

#GET
@app.route('/') 
def print_hello():
	return 'Hello python learning'

@app.route('/books')
def get_books():
	return jsonify({'books': Book.get_all_book()})

@app.route('/book/<int:isbn>')
def get_book_isbn(isbn):
	returnValue = Book.get_book_isbn(isbn)
	# for b in books:
	# 	if b["isbn"] == isbn:
	# 		returnValue = {
	# 			'name': b["name"],
	# 			'price': b["price"]
	# 		}
	return jsonify(returnValue)

#POST
@app.route('/addbooks', methods=['POST'])
def add_book():	
	requestData = request.get_json()	
	if (validBookObject(requestData)):
		# books.insert(0, requestData)		
		Book.add_book(requestData['name'], requestData['price'], requestData['isbn'])
		response = Response("Book sucessfully added", 201, mimetype='applicatiopn/json')
		response.headers['Location'] = "/addbooks/" + str(requestData['isbn'])
		return response
	else:
		invalidBookObject = {
			"error": "Invalid book object passed"
		}
		response = Response(json.dumps(invalidBookObject), status=400,mimetype='applicatiopn/json')
		return response

#PUT /book/123456789
@app.route('/book/<int:isbn>/', methods=['PUT'])
def replcaeBook(isbn):
	requestData = request.get_json()
	if(not validBookObjectForReplace(requestData)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name: 'Book name', 'price': 'Book price'}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='applicatiopn/json')
		return response
	# new_book = {
	# 'name': requestData['name'],
	# 'price': requestData['price'],
	# 'isbn': isbn
	# }
	# i = 0;
	# for book in books:		
	# 	if book["isbn"] == isbn:
	# 		books[i] = new_book
	# 		i += 1
	Book.update_book(isbn, requestData['name'], requestData['price'])
	return Response("", status = 204)

#PATCH
@app.route('/updateBook/<int:isbn>/', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	#update_book = {}
	if("name" in request_data):
		# update_book["name"] = request_data['name']
		Book.update_book_name(isbn, request_data['name'])
	if("price" in request_data):
		# update_book["price"] = request_data['price']
		Book.update_book_price(isbn, request_data['price'])
	# for book in books:
	# 	if book["isbn"] == isbn:
	# 		book.update(update_book)
	response = Response("", status=204)
	response.headers['Location'] = "/updateBook" + str(isbn)
	return response

#DELETE
@app.route('/book/<int:isbn>/', methods=['DELETE'])
def delete_book(isbn):
	# i = 0;
	# for book in books:
	# 	if book["isbn"] == isbn:
	# 		books.pop(i)
	# 		response = Response("Deleted book sucessfully", status=204)
	# 		return response
	# 	i += 1
	if(Book.delete_book(isbn)):
		response = Response("Book deelted sucessfully", status=204)
		return response

	invalidBookObjectErrorMsg = {
		"error": "Book with ISBN number provided not found, So unable to delete"
	}
	response = Response(json.dumps(invalidBookObjectErrorMsg), status = 404, mimetype='application/json')
	return response

app.run(port=5000)


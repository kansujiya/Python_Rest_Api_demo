
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json
from functools import wraps
from settings import *
from BookModel import *
from UserModel import *
import jwt
import datetime

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

app.config['SECRET_KEY'] = 'Suresh'

@app.route('/login', methods=['POST'])
def get_token():
	requestData = request.get_json()
	username = str(requestData['username'])
	password = str(requestData['password'])

	match = User.username_password_match(username, password)

	if match:
		expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=500)
		token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
		return token
	else:
		return Response('Token is not valid or expired', 401, mimetype='application/json')

def token_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		token = request.args.get('token')
		try:
			jwt.decode(token, app.config['SECRET_KEY'])
			return f(*args, **kwargs)
		except:
			return Response('Token is not valid or expired', 401, mimetype='application/json')		
	return wrapper

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

def validUserObject(userObject):
	print(userObject)
	if ("username" in userObject and "password" in userObject):
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
@token_required
def add_book():	
	requestData = request.get_json()	
	if (validBookObject(requestData)):
		# books.insert(0, requestData)		
		Book.add_book(requestData['name'], requestData['price'], requestData['isbn'])
		response = Response("Book sucessfully added", 201, mimetype='application/json')
		response.headers['Location'] = "/addbooks/" + str(requestData['isbn'])
		return response
	else:
		invalidBookObject = {
			"error": "Invalid book object passed"
		}
		response = Response(json.dumps(invalidBookObject), status=400,mimetype='application/json')
		return response

#PUT /book/123456789
@app.route('/book/<int:isbn>/', methods=['PUT'])
@token_required
def replcaeBook(isbn):
	requestData = request.get_json()
	if(not validBookObjectForReplace(requestData)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name: 'Book name', 'price': 'Book price'}"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
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
@token_required
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
@token_required
def delete_book(isbn):
	# i = 0;
	# for book in books:
	# 	if book["isbn"] == isbn:
	# 		books.pop(i)
	# 		response = Response("Deleted book sucessfully", status=204)
	# 		return response
	# 	i += 1
	if(Book.delete_book(isbn)):
		Book.delete_book(isbn)
		response = Response("Book deelted sucessfully", status=204)
		return response

	invalidBookObjectErrorMsg = {
		"error": "Book with ISBN number provided not found, So unable to delete"
	}
	response = Response(json.dumps(invalidBookObjectErrorMsg), status = 404, mimetype='application/json')
	return response

@app.route('/adduser/', methods=['POST'])
def add_user():
	requestData = request.get_json()
	if (validUserObject(requestData)):
		# books.insert(0, requestData)
		User.create_user(requestData['username'], requestData['password'])	
		response = Response("New User sucessfully added", 201, mimetype='application/json')
		response.headers['Location'] = "/addUser/" + str(requestData['username'])
		return response
	else:
		invalidUserObject = {
			"error": "Invalid user object passed"
		}
		response = Response(json.dumps(invalidUserObject), status=400,mimetype='application/json')
		return response

app.run(port=5000)


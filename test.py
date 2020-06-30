
def validBookObject(bookObject):
	if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
	else:
		return False


validObject = {
	'name': 'Kansujiya',
	'isbn': 987654321,
	'price': '200 rupee'
}

unvValidObject = {
	'name': 'Kansujiya',
	'isbn': 987654321	
}
# Python_Rest_Api_demo

Python | Flask framework |  REST API | SQL DB | Books Demo | GET | PUT | POST | PATCH  | JWT Authentication

# Need to install 

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

# Run command to start the server

python3 app.py


# Endpoint created

- /login[POST]
- /adduser[POST]
- /books[GET]
- /book/<int:isbn>[GET]
- /addbook[POST]
- /book/<int:isbn>/[PUT]
- /updateBook/<int:isbn>/[PATCH]
- /book/<int:isbn>/[DELETE]

# Database : books
- Table Name: users
- Table name : books
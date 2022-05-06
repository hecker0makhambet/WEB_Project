from flask_restful import reqparse
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)

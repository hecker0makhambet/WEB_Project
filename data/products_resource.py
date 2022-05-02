from . import db_session
from .products import Product
from .users import User
from flask_restful import abort, Resource, reqparse
from flask import jsonify
from .products_parser import parser


def if_product_not_found(id):
    session = db_session.create_session()
    a = session.query(Product).get(id)
    if not a:
        abort(404, message=f"Product {id} not found")


class ProductResource(Resource):
    def get(self, product_id):
        if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify(product.to_dict(
            only=('name', 'about', 'user_id', 'price')))

    def delete(self, product_id):
        if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({'products': [item.to_dict(
            only=('name', 'about', 'user_id', 'price')) for item in products]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        product = Product(
            name=args['name'],
            about=args['about'],
            user_id=args['user_id'],
            price=args['price']
        )
        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})

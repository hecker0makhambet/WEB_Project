from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.users import User
from data.user_parser import parser


def if_user_not_found(user_id):
    session = db_session.create_session()
    a = session.query(User).get(user_id)
    if not a:
        abort(404, message=f"Product {id} not found")


class UserResource(Resource):
    def get(self, user_id):
        if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(user.to_dict(
            only=('name', 'about', 'email', 'created_date')))

    def delete(self, user_id):
        if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'about', 'email', 'created_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

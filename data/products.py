import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    price = sqlalchemy.Column(sqlalchemy.Integer)
    avatar_name = sqlalchemy.Column(sqlalchemy.String, default=None)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    likes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    starred = set()

    user = orm.relation("User")
    categories = orm.relation("Category",
                              secondary="association",
                              backref="products")

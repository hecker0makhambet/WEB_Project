from flask import Flask, render_template
from flask_restful import Api
from data.blueprints import blueprint
from data.db_session import create_session, global_init
from data import products_resource, db_session
from flask_wtf import FlaskForm
import flask
global_init('data\\database.db')
create_session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(blueprint)
api = Api(app)
api.add_resource(products_resource.ProductResource, '/api/<int:product_id>')
api.add_resource(products_resource.ProductListResource, '/api/')


if __name__ == '__main__':
    app.run()

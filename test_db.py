from data import db_session
from data.users import User
from data.products import Product
from requests import get, delete, post
db_session.global_init('data\\database.db')
session = db_session.create_session()
# a = User(name="USER1", about="FIRST USER OF THIS WEBSITE",
#          email="TEST@EMAIL")
# a.set_password("ABOBUS")
# b = Product(name="Product1", about='FIRST PRODUCT', user_id=1, price=100)
# session.add(a)
# session.add(b)
# session.commit()
# print(get('http://127.0.0.2:5000/api/users').json())
# a = {
#     'name': 'Makhambet', 'about': 'AMOGUS', 'email': 'AMOGUS@gmail.co', 'password': '12345678'
# }
# print(post('http://127.0.0.2:5000/api/users/', json=a).json())
# print(get('http://127.0.0.2:5000/api/users').json())

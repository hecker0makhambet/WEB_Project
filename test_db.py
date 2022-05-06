from data import db_session
from data.users import User
from data.products import Product
db_session.global_init('data\\database.db')
session = db_session.create_session()
# a = User(name="USER1", about="FIRST USER OF THIS WEBSITE",
#          email="TEST@EMAIL")
# a.set_password("ABOBUS")
b = Product(name="Product1", about='FIRST PRODUCT', user_id=1, price=100)
session.add(a)
session.add(b)
session.commit()
a = session.query(User).get(1)

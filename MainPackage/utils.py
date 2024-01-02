from MainPackage.models import User, Category, Product
from sqlalchemy import func
from MainPackage import db
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def product_count_by_cate():
    return Category.query.join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
                               .add_columns(func.count(Product.id)).group_by(Category.id).all()

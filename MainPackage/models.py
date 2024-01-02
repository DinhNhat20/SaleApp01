from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from MainPackage import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


product_tag = db.Table('product_tag',
                       Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                       Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    image = Column(String(100))
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='product_tag', lazy='subquery',
                        backref=backref('products', lazy=True))


class Tag(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Desktop')

        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)

        # p1 = Product(name='Iphone 7 Plus', description='Apple, 32GB', price=12, category_id=1)
        # p2 = Product(name='Iphone 12 Pro Max', description='Apple, 128GB', price=24, category_id=1)
        # p3 = Product(name='iPad Pro 2023', description='Apple, 64GB', price=36, category_id=2)
        # p4 = Product(name='Galaxy Tab S7 Plus', description='Sumsung, 256GB', price=48, category_id=3)

        # db.session.add(p1)
        # db.session.add(p2)
        # db.session.add(p3)
        # db.session.add(p4)

        # t1 = Tag(name='promotion')
        # t2 = Tag(name='new')
        # db.session.add(t1)
        # db.session.add(t2)

        # db.session.commit()

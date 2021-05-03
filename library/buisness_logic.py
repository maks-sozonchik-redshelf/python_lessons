from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library.models import Book

e = create_engine('sqlite:///libray.db', echo=True)
session = sessionmaker(bind=e)()


def create_back(title, author, price, year):
    book = Book(title, author, price, year)
    session.add(book)
    session.commit()
    return book.id


def read_back(author=None):
    if author:
        return session.query(Book).filter_by(author=author)
    else:
        return session.query(Book)


def update_back(id, data):
    book = session.query(Book).filter_by(id=id).first()
    book.title = data['title']
    book.author = data['author']
    book.price = data['price']
    book.year = data['year']
    session.commit()

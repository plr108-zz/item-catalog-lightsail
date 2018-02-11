from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_categories():
    categories = session.query(Category).all()
    return categories


@app.route('/')
def show_categories():
    categories = get_categories()
    latest = session.query(Item).order_by(desc(Item.id)).limit(5)
    return render_template('categories.html', categories=categories,
                           latest=latest)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

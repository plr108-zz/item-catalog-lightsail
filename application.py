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


@app.route('/')
def allCategories():
    categories = session.query(Category).all()
    latest = session.query(Item).order_by(desc(Item.id)).limit(5)
    return render_template('categories.html', categories=categories,
                           latest=latest)
    print sqlalchemy.__version__
    return 'sqlalchemy.__version__'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

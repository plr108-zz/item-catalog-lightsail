import sys
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


def get_category_by_name(category_name):
    category = session.query(
        Category).filter_by(name=category_name).one()
    return category


def get_item_by_names(category_name, item_name):
    selected_category = session.query(
        Category).filter_by(name=category_name).one()
    selected_item = session.query(Item).filter_by(
        name=item_name, category=selected_category).one()
    return selected_item


@app.route('/')
@app.route('/catalog')
def show_categories():
    categories = get_categories()
    latest = session.query(Item).order_by(desc(Item.id)).limit(5)
    return render_template('categories.html', categories=categories,
                           latest=latest)


@app.route('/catalog/<category_name>')
def show_category(category_name):
    try:
        categories = get_categories()
        selected_category = get_category_by_name(category_name)
        category_items = session.query(
            Item).filter_by(cat_id=int(selected_category.id)).all()
    except:
        response = 'Category not found: ' + category_name
        print sys.exc_info()[0]
    else:
        category_item_count = str(len(category_items))
        response = render_template(
            'category.html',
            categories=categories,
            selected_category=selected_category,
            category_items=category_items,
            category_item_count=category_item_count)
    return response


@app.route('/catalog/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        new_item = Item(name=request.form['name'],
                        description=request.form['description'],
                        category=get_category_by_name(
                            request.form['category']))
        session.add(new_item)
        session.commit()
        response = redirect(
            url_for('show_category', category_name=request.form['category']))

    else:
        categories = get_categories()
        response = render_template('new_item.html', categories=categories)
    return response


@app.route('/catalog/<category_name>/<item_name>')
def show_item(category_name, item_name):
    try:
        selected_item = get_item_by_names(category_name, item_name)
    except:
        response = 'Item not found: ' + item_name
        print sys.exc_info()[0]
    else:
        response = render_template('item.html', item=selected_item)
    return response


@app.route('/catalog/<category_name>/<item_name>/edit',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    try:
        selected_item = get_item_by_names(category_name, item_name)
    except:
        response = 'Item not found: ' + item_name
        print sys.exc_info()[0]
    else:
        categories = get_categories()
        if request.method == 'GET':
            response = render_template('edit_item.html',
                                       categories=categories,
                                       item=selected_item)
        else:
            # handle POST request
            if request.form['name']:
                selected_item.name = request.form['name']
                selected_item.description = request.form['description']
                selected_item.cat_id = get_category_by_name(
                    request.form['category']).id
                session.commit()
                response = redirect(
                    url_for('show_item',
                            category_name=selected_item.category.name,
                            item_name=selected_item.name))
            else:
                # handle case where name is empty
                flash('Name cannot be empty.  Please edit the item again.')
                response = render_template('edit_item.html',
                                           categories=categories,
                                           item=selected_item)
    return response


@app.route('/catalog/<category_name>/<item_name>/delete',
           methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    try:
        selected_item = get_item_by_names(category_name, item_name)
    except:
        response = 'Item not found: ' + item_name
        print sys.exc_info()[0]
    else:
        if request.method == 'GET':
            response = render_template('delete_item.html', item=selected_item)
        else:
            # handle POST request
            session.delete(selected_item)
            session.commit()
            flash(item_name + ' has been deleted')
            response = redirect(
                url_for('show_category', category_name=category_name))
    return response


if __name__ == '__main__':
    app.debug = True
    app.secret_key = '#if~you^can_read*this=it`s-too+late'
    app.run(host='0.0.0.0', port=8000)

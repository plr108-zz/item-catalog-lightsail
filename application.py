import httplib2
import json
import random
import requests
import string
import sys
from database_setup import Base, Category, Item, User
from flask import Flask, flash, jsonify, make_response
from flask import redirect, render_template, request, url_for
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
CLIENT_ID = json.loads(
    open('google_oauth2_client.json', 'r').read())['web']['client_id']


def get_categories():
    categories = session.query(Category).all()
    return categories


def get_category_by_name(category_name):
    category = session.query(
        Category).filter_by(name=category_name).one()
    return category


def get_category_items_by_category_name(category_name):
    category = get_category_by_name(category_name)
    category_items = session.query(Item).filter_by(
        cat_id=int(category.id)).all()
    return category_items


def get_item_by_names(category_name, item_name):
    selected_category = session.query(
        Category).filter_by(name=category_name).one()
    selected_item = session.query(Item).filter_by(
        name=item_name, category=selected_category).one()
    return selected_item


def get_latest():
    latest = session.query(Item).order_by(desc(Item.id)).limit(5)
    return latest


def create_user(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    categories = get_categories()
    latest = get_latest()
    return render_template('login.html', STATE=state, categories=categories,
                           latest=latest)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'google_oauth2_client.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    user_id = get_user_id(login_session['email'])
    # if user doesn't have a user_id then create new user_id
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    login_msg = login_session['username'] + ' has been logged in'
    flash(login_msg)
    print(login_msg)
    return login_msg


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        flash_msg = 'Current user not connected.'
    else:
        url = 'https://accounts.google.com/o/oauth2/revoke?token='
        url += login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
            username = login_session.get('username')
            del login_session['access_token']
            del login_session['google_id']
            del login_session['username']
            del login_session['email']
            flash_msg = username + ' has been logged out'
        else:
            print(result['status'])
            flash_msg = 'Error logging out user'
    flash(flash_msg)
    # redirect to top-level and show categories
    return redirect('/')


@app.route('/')
@app.route('/catalog')
def show_categories():
    categories = get_categories()
    latest = get_latest()
    return render_template('categories.html', categories=categories,
                           latest=latest)


@app.route('/catalog.json')
def show_catalog_json():
    categories = get_categories()
    category_json = [i.serialize for i in categories]
    latest = get_latest()
    latest_json = [i.serialize for i in latest]
    catalog_json = jsonify(Category=category_json, LatestItems=latest_json)
    return catalog_json


@app.route('/catalog/<category_name>')
def show_category(category_name):
    try:
        categories = get_categories()
        selected_category = get_category_by_name(category_name)
        category_items = get_category_items_by_category_name(category_name)
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


@app.route('/catalog/<category_name>.json')
def show_category_json(category_name):
    category_items = get_category_items_by_category_name(category_name)
    category_json = jsonify(
        category_name, [i.serialize for i in category_items])
    return category_json


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


@app.route('/catalog/<category_name>/<item_name>.json')
def show_item_json(category_name, item_name):
    item = get_item_by_names(category_name, item_name)
    item_json = jsonify(
        item_name, [item.serialize])
    return item_json


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

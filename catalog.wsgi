#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
engine = create_engine('postgresql+psycopg2://grader:1isGraderThan0@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
def application(environ, start_response):
    status = '200 OK'
    output = 'Hello!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
'''
from catalog import app as application
application.secret_key = 'Add your secret key'

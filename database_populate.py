from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def addCategory(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    return


addCategory('Soccer')
addCategory('Basketball')
addCategory('Baseball')
addCategory('Frisbee')
addCategory('Snowboarding')
addCategory('Rock Climbing')
addCategory('Foosball')
addCategory('Skating')
addCategory('Hockey')
print 'Database populated'

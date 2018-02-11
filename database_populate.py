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
    return category


def addItem(name, description, category):
    item = Item(name=name,
                description=description,
                category=category)
    session.add(item)
    session.commit()
    return


Raw = addCategory('Raw')
SmackDown = addCategory('SmackDown')
WWE_205_Live = addCategory('205 Live')
addItem('Brock Lesnar', 'The Beast Incarnate', Raw)
addItem('Finn Balor', 'The Demon King', Raw)
addItem('Samoa Joe', 'The Destroyer', Raw)
addItem('Triple H', 'The Game', Raw)
addItem('Braun Strowman', 'The Monster Among Men', Raw)
addItem('John Cena', 'The Face That Runs The Place', SmackDown)
addItem('Shinsuke Nakamura', 'The Artist', SmackDown)
addItem('Bobby Roode', 'The Glorious One', SmackDown)
addItem('Shane McMahon', 'Shane-O-Mac', SmackDown)
addItem('Randy Orton', 'The Viper', SmackDown)
addItem('Akira Tozawa', 'The Stamina Monster', WWE_205_Live)
addItem('Neville', 'The King of the Cruiserweights', WWE_205_Live)
print 'Database populated'

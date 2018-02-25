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


Soccer = addCategory('Soccer')
Basketball = addCategory('Basketball')
Baseball = addCategory('Baseball')
Frisbee = addCategory('Frisbee')
Snowboarding = addCategory('Snowboarding')
RockClimbing = addCategory('Rock Climbing')
Foosball = addCategory('Foosball')
Skating = addCategory('Skating')
Hockey = addCategory('Hockey')
addItem('Soccer Cleats', 'Better than barefoot', Soccer)
addItem('Jersey', 'Your uni top', Soccer)
addItem('Bat', 'You hit the ball with it', Baseball)
addItem('Frisbee', 'You throw it', Frisbee)
addItem('Shinguards', 'Safety First', Soccer)
addItem('Two shinguards', '..are better than one!', Soccer)
snowboarding_description = 'Way better than Skiing.  Also, Jamie Anderson.  '
snowboarding_description += 'Red Gerard.  Chloe Kim.  Even Shaun White.  '
snowboarding_description += 'Need I say more??'
addItem('Snowboarding', snowboarding_description, Snowboarding)
print 'Database populated'

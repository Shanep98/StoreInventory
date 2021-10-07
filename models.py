from sqlalchemy import (create_engine, Column, Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# #create a database
# inventory.db
engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# create a Module
# product_id, product_name,product_price,product_quantity,date_updated
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_name = Column('Product', String)
    product_price = Column('Price', Integer)
    product_quantity = Column('Quantity', Integer)
    date_updated = Column('Added', Date)
    
    def __repr__(self):
        return f'Product: {self.product_name} Price: {self.product_price} Quantity: {self.product_quantity} Added: {self.date_updated}'
    
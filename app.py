from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


# import models.py
# main menu a, v, b
def menu():
    while True:
        print('''
              \n***In house Inventory Manager***
              \ra) Add Product
              \rv) Search by id
              \rb) Backup Database
              \re) Exit''')
        choice = input('What would you like to do?> ')
        if choice.lower in ['a', 'v', 'b', 'e']:
            return choice
        else:
            ('''
            \rPlease enter an option from above.
            \r Options are (a, v, b, e)''')
            time.sleep(1.5)


# Cleanup

def clean_price(price_str):
    try:
        price = int(float(price_str.replace("$","")) * 100)
    except ValueError:
        input('''
              \n***Price Error***
              \rPlease reenter the price without a currency symbol.
              \r Ex: 12.99
              \rPress ENTER to try again.''')
    else:
        return price
    
    
def clean_date(date_str):
    date_str = str(date_str)
    date_str = date_str.strftime('%m/%d/%Y')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
               \n*****DATE ERROR*****
               \rThe date format should include a valid Month Day from the past
               \rEx: January 15, 2003
               \rPress enter to try again.
               \r*************************''')
        return
    else:    
        return return_date
    
    
def clean_id(id_str, options):
    try:
        item_id = int(id_str)
    except ValueError:
        input('''
              \n***Id Error***
              \rThe Product Id should be only a Number
              \rPress ENTER to try again.''')
        return
    else:
        if item_id in options:
            return item_id
        else:
            input(f'''
                  \n***Id Error***
                  \rId Options: {options}
                  \rPress ENTER to try again.''')
            return
    

def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = row[2]
                date_updated = row[3]#need to clean
                new_item = Product(name=name, price=price, quantity=quantity, date_updated=date_updated)
                session.add(new_item)
            session.commit()
# product_id, product_name,product_price,product_quantity,date_updated

# V- Display a produce by id
# A- Add a new produce
# B- backing up the Database 
# loop running


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'a':
            # add
            pass
        elif choice == 'v':
            #view by id
            id_options = []
            for item in session.query(Product):
                id_options.append(item.id)
            id_error = True
            while id_error:
                id_to_search = input(f'''
                                     ID Options: {id_to_search}
                                     Product id: ''')
                #***Need TO clean ID***
                id_to_search = clean_id(id_to_search, id_options)
                if type(id_to_search) == int:
                    id_error = False
            searched_item = session.query(Product).filter(Product.id==id_to_search).first()
            print(f'''
                  \n{searched_item.name} we have {searched_item.quantity}
                  \rCost: {searched_item.price}
                  \rLast Updated: {searched_item.date_updated}''')
        elif choice == 'b':
            #backup
            pass
        else:
            print('Thank you, have a nice day.')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_csv()
    
    # for item in session.query(Product):
    #     print(item)
    # test = clean_date(3/10/2018)
    # print(test)
    date = 3/10/2018
    # date = str(date)
    # date = date.datetime.strftime('%m-%d-%Y')
    print(date)
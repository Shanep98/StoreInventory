from models import (Base, session,
                    Product, engine)
import datetime
import csv


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
        return choice
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
        
        
def clean_date(date_str):

    split_date = date_str.split('/')
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
                date_updated = datetime.datetime.strptime(row[3], '%m/%d/%Y').date()
                new_item = Product(name=name, price=price, quantity=quantity, date_updated=date_updated)
                session.add(new_item)
            elif product_in_db != None:
                product_in_db.price = clean_price(row[1])
                product_in_db.quantity = row[2]
                product_in_db.date_updated = datetime.datetime.strptime(row[3], '%m/%d/%Y').date()
            session.commit()
# product_id, product_name,product_price,product_quantity,date_updated

# V- Display a produce by id
# A- Add a new produce
# B- backing up the Database 
# loop running


def app():
    add_csv()
    app_running = True
    while app_running:
        choice = menu().lower()
        if choice.lower() == 'a':
            #now = datetime.datetime.now()
            # add
            new_name = input('''\nWhat is the name of the Product you would like to add?(If the product has a descripition please seperate it with a '-')
                             \rExample of Product name with a description "Bagel - Whole White Sesame"
                             \r > ''')
            new_name = str(new_name.title())
            new_amount = int(input("\nHow much of this Product are we adding into our stock? > "))
            new_price = int(clean_price(input("\nHow much does the Product cost? > ")))
            new_date = clean_date(input('\nWhen was this product added(format mm/dd/yyyy)? > '))
            search_db = session.query(Product).filter(Product.name==new_name).one_or_none()
            if search_db == None:
                new_item = Product(name=new_name, price=new_price, quantity=new_amount, date_updated=new_date)
                session.add(new_item)
            else:
                search_db.price = new_price
                search_db.quantity = new_amount
                search_db.date_updated = new_date
            session.commit()
        elif choice.lower() == 'v':
            #view by id
            id_options = []
            for item in session.query(Product):
                id_options.append(item.id)
            id_error = True
            while id_error:
                id_to_search = input(f'''
                                     \nID Options: {id_options}
                                     \rProduct id: ''')
                #***Need TO clean ID***
                id_to_search = clean_id(id_to_search, id_options)
                if type(id_to_search) == int:
                    id_error = False
            searched_item = session.query(Product).filter(Product.id==id_to_search).first()
            print(f'''
                  \n{searched_item.name} we have {searched_item.quantity}
                  \rCost: {searched_item.price / 100}
                  \rLast Updated: {searched_item.date_updated}''')
            input('\nPress ENTER to be returned back to Main Menu.')
        elif choice.lower() == 'b':
            #backup
            with open('backup.csv', 'a') as csvfile:
                fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
                printer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                printer.writeheader()
                for product in session.query(Product):
                    printer.writerow({'product_name': (product.name), 'product_price': (product.price), 'product_quantity': (product.quantity), 'date_updated': (product.date_updated)})
        elif choice.lower() == 'e':
            print('\nThank you, have a nice day.')
            app_running = False
        else:
            input('''
                 \rPlease enter an option from above.
                 \r Options are (a, v, b, e)
                 \rPress Enter to try again.''')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #add_csv()
    app()

   
from models import (Base, Session,
                    Product, engine)


# import models.py
# main menu a, v, b
# Cleanup
# V- Display a produce by id
# A- Add a new produce
# B- backing up the Database 
# loop running


if __name__ == '__main__':
    Base.metadata.create_all(engine)
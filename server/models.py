from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from sqlalchemy_serializer import SerializerMixin

class Car(db.Model, SerializerMixin):

    __tablename__ = 'cars_table'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String)
    year = db.Column(db.Integer)
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealers_table.id'))
    
    dealer = db.relationship('Dealer', back_populates='cars')

    serialize_rules = ('-dealer.cars',)

    @validates('year')
    def validate_year(self, key, inc_year):
        if inc_year in range(1908, 2025):
            return inc_year
        else:
            raise ValueError('Year must be a valid year')

class Person(db.Model, SerializerMixin):

    __tablename__ = 'persons_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    dealers = db.relationship('Dealer',back_populates='person')

    cars = association_proxy('dealers', 'cars')

    serialize_rules = ('-dealers.person',)

class Dealer(db.Model, SerializerMixin):

    __tablename__ = 'dealers_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    person_id = db.Column(db.Integer, db.ForeignKey('persons_table.id'))
    
    person = db.relationship('Person', back_populates='dealers')
    cars = db.relationship('Car', back_populates='dealer')

    serialize_rules = ('-person.dealers', '-cars.dealer')
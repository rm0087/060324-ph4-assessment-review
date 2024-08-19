#!/usr/bin/env python3

from flask import request
from config import app, db
from models import Car, Person, Dealer

@app.get('/')
def index():
    return "Hello world"

@app.post('/cars')
def post_car():
    data = request.json # <<< the body of the request

    try:
        new_car = Car(name=data['name'], year=data['year'])
        db.session.add(new_car)
        db.session.commit()

        return new_car.to_dict(), 201
    except:
        return {'message':'OH NOES'}, 400
    
@app.patch('/cars/<int:id>')
def patch_car(id):
    data = request.json
    car = Car.query.where(Car.id == id).first()

    if car:
        try:
            for key in data:
                setattr(car, key, data[key])
            db.session.add(car)
            db.session.commit()

            return car.to_dict(), 202
        except:
            return {'error': 'Invalid data'}, 400
    else:
        return{'error': "Dude where's my car?"}, 404

@app.get('/cars')
def get_cars():
    data = Car.query.all()
    try: 
        return [car.to_dict() for car in data], 200
    except:
        return {'mesesage': 'OH NOES'}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)

##NO AUTH/PROXY STUFF

import pymongo
from fastapi import FastAPI
from mongoengine import connect

localhost = 'localhost'
port = 27017

app = FastAPI()

connect(db='apiTest', host=localhost, port=port)
url = pymongo.MongoClient(localhost, port)
dataBase = url['car']
collection = dataBase['car']


@app.get('/')
def home():
    return {'welcome to cars api'}


@app.post('/add_car')
def add_car(brand: str, price: str, model: str):
    q = {'brand': brand, 'price': price, 'model': model}
    collection.insert_one(q)
    return {'your car has been added'}


@app.put('/update_model')
def update_car_model(modelFilter: str, brand: str, price: str, model: str):
    filter = {'model': modelFilter}
    q = {'$set': {'brand': brand, 'price': price, 'model': model}}
    collection.update_one(filter, q)
    return {'the car ' + modelFilter + ' has been renamed ' + model}


@app.delete('/delete_car')
def delete_test(modelfilter: str):
    q = {'model': modelfilter}
    collection.delete_one(q)
    return {'the car ' + modelfilter + 'has been deleted'}

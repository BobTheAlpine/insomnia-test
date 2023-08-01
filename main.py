# from fastapi import FastAPI, Body
# import schemas
#
# app = FastAPI()
#
# fakeDatabase = {
#     1:{'task':'clean car'},
#     2:{'task':'wash dishes'},
#     3:{'task':'pet cat'},
# }
#
# @app.get("/")
# async def root():
#     return fakeDatabase
#
#
# @app.get("/{id}")
# def getItem(id:int):
#     return fakeDatabase[id]
#
# # @app.post("/")
# # def addItem(task:str):
# #     newId = len(fakeDatabase.keys()) + 1
# #     fakeDatabase[newId] = {"task":task}
# #     return fakeDatabase
#
# lastId = 0  # Keep track of the last assigned ID
#
# @app.post("/")
# def addItem(item: schemas.Item):
#     global lastId
#     newId = lastId + 1
#     lastId = newId
#     fakeDatabase[newId] = {"task": item.task}
#     return fakeDatabase
#
# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase
#
# @app.delete("/{id}")
# def deleteItem(id:int):
#     del fakeDatabase[id]
#     return fakeDatabase


from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# This will create our database if it doesn't already exist
Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.post("/")
def addItem(item: schemas.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

from database import SessionLocal, User
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app = FastAPI()

#CRUD operations

class UserBody(BaseModel):
    name: str
    email: str


@app.post("/user") # to add a new user to the database
def add_user(user: UserBody, 
             db: Session = Depends(get_db)):
    new_user = User(
        name = user.name,
        email = user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users") # to read all users from the database
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/user") # to read a user by id from the database
def get_user(user_id: int, 
             db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id==user_id).first())
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return user

@app.post("/user/{user_id}") # to update a user by id in the database
def update_user(
        user_id: int, 
        user: UserBody,
        db: Session = Depends(get_db)):
    db_user = (
        db.query(User).filter(User.id == user_id).first() # to get the first user with matching ID
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/user") # to delete a user from the database using ID
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = (db.query(User).filter(User.id==user_id).first())
    if db_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "user deleted"}
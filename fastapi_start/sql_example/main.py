from database import SessionLocal
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app = FastAPI()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(user).all()
    return users

#CRUD operations

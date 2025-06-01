from database_nosql import user_collection
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from bson import ObjectId

class Tweet(BaseModel):
    content: str
    hasgtags: list[str]

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    tweets: list[Tweet] | None = None
    @field_validator("age")
    def validate_age(cls, value):
        if value < 18 or value >100:
            raise ValueError("Age must be between 18 and 100")
        return value
    
class UserResponse(User):
    id: str


    
        
app = FastAPI()


@app.get("/users") # to read all users from the database
def read_users()-> list[User]:
    return [user for user in user_collection.find()]

@app.post("/users") # to create a new user in the database
def create_user(user: User):
    result = user_collection.insert_one(user.model_dump(exclude_none=True))
    user_response = UserResponse(id=str(result.inserted_id), **user.model_dump())
    return user_response #an ID is created which is attributed to the user record

@app.get("/user") # to read a user by user id from the database
def get_user(user_id:str)->UserResponse:
    db_user = user_collection.find_one({
        "_id": ObjectId(user_id)
        if ObjectId.is_valid(user_id) else None
    })
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user["id"] = str(db_user["_id"]) #to convert into a string
    return db_user #returns the record with the ID in a validated fashion




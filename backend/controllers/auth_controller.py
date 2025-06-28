from models.user_model import UserCreate, UserLogin, UserWithId
from fastapi import HTTPException
from utils import db
import bcrypt
from bson import ObjectId
from bson.errors import InvalidId

user_collection = db["users"]

async def signup(user: UserCreate):
    existing_user = await user_collection.find_one({
        "$or": [
            {"email": user.email.lower()},
            {"username": user.username.lower()}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already taken")

    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    user_dict = {
        "username": user.username.lower(),
        "email": user.email.lower(),
        "password": hashed_pw.decode("utf-8")
    }

    await user_collection.insert_one(user_dict)
    return {"username": user.username, "email": user.email}


async def signin(user: UserLogin):
    identifier = user.username_or_email.lower()

    found_user = await user_collection.find_one({
        "$or": [
            {"email": identifier},
            {"username": identifier}
        ]
    })

    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.password.encode("utf-8"), found_user["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"username": found_user["username"], "email": found_user["email"]}

async def get_user_by_id(user_id: str):
    try:
        _id = ObjectId(user_id) 
    except InvalidId: 
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await user_collection.find_one({"_id": _id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserWithId(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"]
    )
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from hashlib import sha256

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client["auth_db"]
users = db["users"]


SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    email: EmailStr
    password: str

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=24)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Routes


@app.post("/signup")
async def signup(user: User):
    if await users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

   
    prehashed = sha256(user.password.encode('utf-8')).hexdigest()
    hashed_pw = pwd_context.hash(prehashed)

    await users.insert_one({"email": user.email, "password": hashed_pw})
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: User):
    db_user = await users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    prehashed = sha256(user.password.encode('utf-8')).hexdigest()
    if not pwd_context.verify(prehashed, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

import argparse
import hashlib
import logging
import os
import random
import string
import sys

from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.schemas.users import UserBase, UserCreate, User
from app.models.users import UserTable


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# create async engine for interaction with database
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/about')
async def about(request: Request):
    logging.info('about')
    return templates.TemplateResponse("about.html", context={"request": request})


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("about.html", context={"request": request})


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


@app.post("/sign-up", response_model=UserCreate)
async def create_user(user: UserCreate):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)

    print(user.email)
    print(hashed_password)

    async with async_session() as session:
        async with session.begin():
            new_user = UserTable(
                name=user.name,
                email=user.email,
                hashed_password=hashed_password,
            )
            session.add(new_user)
            await session.flush()

    return {"email": user.email, "name": user.name, "password": hashed_password}


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args = args_parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "80")), log_level="info")

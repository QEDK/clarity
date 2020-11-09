import urllib
import os
import sqlalchemy
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate
import databases

host_server = os.environ.get('host_server', "localhost")
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
# credentials of the postgres db instance:
database_name = os.environ.get('database_name', 'fastapidbname')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'password')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_username, db_password, host_server, db_server_port, database_name)

metadata = sqlalchemy.MetaData()

user_journal = sqlalchemy.Table(
    "user_journal",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("text_journal", sqlalchemy.String),
    sqlalchemy.Column("journal_url", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=0)

metadata.create_all(engine)


class Journal_in(BaseModel):
    email: str
    text_journal: str
    journal_url: str
    time: str


class Journal(BaseModel):
    id: int
    email: str
    text_journal: str
    journal_url: str
    time: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True
)

database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/api/add_note")
async def add_note(journal: Journal_in):
    check_user_query = user_journal.select().where(user_journal.c.email == journal.email)
    user = await database.fetch_one(check_user_query)
    if user is None:
        url = generate(size=36)
    else:
        url = user.get("journal_url")
    query = user_journal.insert().values(email=journal.email, text_journal=journal.text_journal,
                                         journal_url=url, time=journal.time)
    last_record_id = await database.execute(query)
    return {** journal.dict(), "id": last_record_id}


@app.get("/api/get_note/{email}")
async def get_note(email: str):
    query = user_journal.select().where(user_journal.c.email == email)
    userlist = await database.fetch_all(query)
    return userlist


@app.get("/api/get_from_url/{url}")
async def get_from_url(url: str):
    query = user_journal.select().where(user_journal.c.journal_url == url)
    userlist = await database.fetch_all(query)
    return userlist

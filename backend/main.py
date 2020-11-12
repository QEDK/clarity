import databases
import os
import sqlalchemy
import sys
import urllib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nanoid import generate
from pathlib import Path
from pydantic import BaseModel
sys.path.append(str(Path(__file__).resolve().parents[1].joinpath("ml")))
from processtext import ProcessText  # noqa

nlp = ProcessText()  # noqa: init the ML model

db_server = os.environ.get("db_server", "localhost")
db_server_port = urllib.parse.quote_plus(str(os.environ.get("db_server_port", "5432")))
# Credentials of the PostgreSQL instance:
db_name = os.environ.get("db_name", "fastapidbname")
db_username = urllib.parse.quote_plus(str(os.environ.get("db_username", "postgres")))
db_password = urllib.parse.quote_plus(str(os.environ.get("db_password", "password")))
db_url = f"postgresql://{db_username}:{db_password}@{db_server}:{db_server_port}/{db_name}"

metadata = sqlalchemy.MetaData()

user_journal = sqlalchemy.Table(
    "user_journal",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("text_journal", sqlalchemy.String),
    sqlalchemy.Column("journal_url", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column("model_output", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(db_url, pool_size=6, max_overflow=0)

metadata.create_all(engine)


class Journal_in(BaseModel):
    email: str
    text_journal: str
    time: str


class Journal(BaseModel):
    id: int
    email: str
    text_journal: str
    journal_url: str
    time: str
    model_output: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database = databases.Database(db_url)


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
    model_response = await nlp.process(journal.text_journal)
    query = user_journal.insert().values(email=journal.email, text_journal=journal.text_journal,
                                         journal_url=url, time=journal.time,
                                         model_output=model_response)
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

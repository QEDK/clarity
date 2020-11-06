from datetime import time
import urllib
import os
import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from typing import List
import databases

host_server = os.environ.get('host_server', "localhost")
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
# setup the below database in your localmachine 
database_name = os.environ.get('database_name', 'fastapidbname')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'password')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server, db_server_port, database_name)

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

@app.post("/api/add_user", response_model=Journal)
async def add_user(journal: Journal_in):
    query = user_journal.insert().values(email = journal.email, text_journal = journal.text_journal, journal_url = journal.email, time = journal.time)
    last_record_id = await database.execute(query)
    return {** journal.dict(), "id": last_record_id}





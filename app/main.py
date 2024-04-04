

from fastapi import FastAPI
from typing import Optional
from app import setting 
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session



# schemas of db
class Todo(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    title : str = Field(index=True)

# connect to database
connect_string : str =  str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
# DATABASE_URL = "postgresql://wajid_db_owner:1XGykD5uJlom@ep-round-dawn-a1poihie.ap-southeast-1.aws.neon.tech/wajid?sslmode=require"

engine = create_engine(connect_string)

def create_table_and_db():
   SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_table_and_db()
    yield


app : FastAPI = FastAPI(lifespan=lifespan)


@app.post("/mytask")
def creat_task(todo_data : Todo):
    with Session(engine) as session:
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return todo_data
    


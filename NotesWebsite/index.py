# To run the file in terminal 
# cd .\NotesWebsite
# uvicorn index:app --reload

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector as sql


# INTERFACING WITH STATIC FILES
app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name = "static")

# TEMPLATES
templates = Jinja2Templates(directory="templates")

# Connection with SQL
conn = sql.connect(user = "root", host  = "localhost", password  ="tiger")
mycursor = conn.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS NOTES")
mycursor.execute("USE NOTES")
mycursor.execute("CREATE TABLE IF NOT EXISTS NOTESSAVER (NOTE_TITLE VARCHAR(30) NOT NULL, NOTE_DESC VARCHAR(100), IMPORTANT VARCHAR(5), CREATE_DATE DATETIME)")

# HOME PAGE ROUTE
@app.get('/',response_class = HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

class Note(BaseModel):
    notestitle: str
    notesdesc: str
    important: bool = False

# Home Page post route
@app.post('/')
async def enter_notes(request: Request,notestitle: str = Form(), notesdesc: str | None = Form(None), important: str | None = Form(None)):
    notes = dict()
    notes.update({"title":notestitle})
    notes.update({"desc":notesdesc})
    checked = "True" if important == "on" else "False"
    notes.update({"important":checked})
    print(notes)
    mycursor.execute(F"INSERT INTO NOTESSAVER(NOTE_TITLE,NOTE_DESC,IMPORTANT,CREATE_DATE) VALUES ('{notestitle}','{notesdesc}','{checked}',CURRENT_TIMESTAMP())")
    conn.commit()
    return templates.TemplateResponse("index.html",{"request":request})

# Saved Notes
@app.get("/saved",response_class=HTMLResponse)
async def savednotes(request: Request):
    mycursor.execute("SELECT * FROM NOTESSAVER")
    data = mycursor.fetchall()
    return templates.TemplateResponse("saved.html",{"request":request,"data":data})
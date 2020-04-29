import sqlite3
import bcrypt
from datetime import datetime

db="z_Database1.db"
conn=sqlite3.connect(db)
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (username,password,email,phoneNumber) ")
cur.execute("CREATE TABLE IF NOT EXISTS logs (username,Date,Datetime,TypeOfWork,Description) ")


def add_creds(username,password,email,phoneNumber):
  password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
  cur.execute(" INSERT INTO users VALUES (?,?,?,?) ",(username,password_hash,email,phoneNumber))
  conn.commit()
  return None


def check_username(username):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    return True


def check_email(email):
  for user in cur.execute("SELECT * FROM users WHERE email = ? ",(email,)):
    return True


def validate_creds(username,password):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    encodedPass = password.encode('utf8')
    return bcrypt.checkpw(encodedPass, user[1])
  return False


def addWork(dic):
  typeOfWork = dic['typeOfWork']#escape these
  description = dic['description']
  username = dic['username']
  dateTime = datetime.now()
  date = dateTime.strftime("%x")
  cur.execute(" INSERT INTO logs VALUES (?,?,?,?,?) ",(username,date,dateTime,typeOfWork,description))
  conn.commit()
  return {'message':"log added"}

def filterLogs(date):
  retLi = []
  logS =cur.execute("SELECT * FROM logs WHERE Date = ? ",(date,))
  for log in logS:
    li = []
    for i in log:
      li.append(i)
    retLi.append(li)
  return retLi

def logsToday():
  dateTime = datetime.now()
  date = dateTime.strftime("%x")
  logss = filterLogs(date)
  return logss
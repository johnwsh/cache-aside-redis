import mysql.connector
import redis
import os
from dotenv import load_dotenv

load_dotenv()

senha = os.getenv("MYSQL_SENHA")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=senha,
  database="tpch"
)

cursor = mydb.cursor(dictionary=True)

def getPedido():
    return None
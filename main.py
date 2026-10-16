from operator import ne

import mysql.connector
import redis
import os
from decimal import Decimal
import datetime
from dotenv import load_dotenv

load_dotenv()

senha = os.getenv("MYSQL_SENHA")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=senha,
  database="tpch"
)

cursor = mydb.cursor(dictionary=True)

def getPedido(idpedido: int):
    cache_key = f"order:{idpedido}"

    cached_data = r.get(cache_key)

    if cached_data:
        print("Cache hit")
        return eval(cached_data)

    print("Cache miss")

    query = """
        SELECT 
            o.O_ORDERKEY,
            o.O_CUSTKEY,
            o.O_ORDERSTATUS,
            o.O_TOTALPRICE,
            o.O_ORDERDATE,
            o.O_ORDERPRIORITY,
            o.O_CLERK,
            o.O_SHIPPRIORITY,
            o.O_COMMENT
        FROM ORDERS o
        WHERE o.O_ORDERKEY = %s
    """
    cursor.execute(query, (idpedido,))

    pedido = cursor.fetchone()

    if not pedido:
        return None

    query_itens = """
        SELECT 
            l.L_PARTKEY,
            l.L_QUANTITY,
            l.L_EXTENDEDPRICE,
            l.L_DISCOUNT,
            l.L_TAX,
            l.L_RETURNFLAG,
            l.L_LINESTATUS
        FROM LINEITEM l
        WHERE l.L_ORDERKEY = %s
    """
    cursor.execute(query_itens, (idpedido,))
    itens = cursor.fetchall()

    pedido['itens'] = itens

    r.set(cache_key, str(pedido), ex=3600)

    return pedido

def atualizarPedido(idpedido: int, novo_status: str):
    query = "UPDATE ORDERS SET O_ORDERSTATUS = %s WHERE O_ORDERKEY = %s"
    cursor.execute(query, (novo_status, idpedido))
    mydb.commit()

    cache_key = f"order:{idpedido}"
    r.delete(cache_key)
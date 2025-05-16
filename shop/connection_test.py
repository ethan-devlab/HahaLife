# coding=utf-8

import mysql.connector
import mysql.connector.cursor


def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='DBMS_A13',
        password='DBMS_A13',
        db='shopping',
        charset='utf8mb4',
    )

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
    finally:
        conn.close()

# 用select, show的時候要加上fetch=True，其他的都不用

# query = execute_query("SHOW COLUMNS FROM SELLER", fetch=True)
# columns = [i[0] for i in query]
# print(columns)
# result = execute_query("SELECT * FROM SELLER", fetch=True)
# print(result)
#
# print([dict(zip(columns, row)) for row in result])

query = execute_query("SELECT * FROM SELLER WHERE UID = %s", params=['S000000001',], fetch=True)
print(query[0])

# get new id
# next_uid = execute_query("SELECT LPAD(COUNT(*)+1, 9, '0') AS next_id FROM PRODUCT", fetch=True)[0][0]
# pid = f"P{next_uid}"
# print(pid)
# insert new values
# product_name = "Abc"
# query = execute_query("INSERT INTO PRODUCT VALUES (%s, %s, %s, %s, %s, %s, %s)", params=(pid, category, ... and other values), fetch=False)

query = execute_query("SELECT * FROM PRODUCT WHERE PID = %s", params=['P000000001',], fetch=True)
print(query[0])

query = execute_query("SELECT * FROM MEMBER WHERE Email=%s AND Password=%s AND AccStatus='Active'",
                      params=("alice@example.com", "pass1234"), fetch=True)[0]
print(dict(query))


# 取得下一個 UID（例如 A000000123）
# next_uid_raw = execute_query(
#     "SELECT LPAD(COUNT(*) + 1, 9, '0') AS next_id FROM APPLICANT", fetch=True)
# print(next_uid_raw[0]['next_id'])
# uid = f"A{next_uid_raw[0]['next_id']}"
# print("New UID:", uid)
#
# # 模擬表單輸入
# full_name = "Charlie Wu"
# email = "charlie@example.com"
# phone = "0988777666"
# address = "123 Happy St."
# birth_date = "2000-01-15"
#
# # 新增進資料庫
# query = """
#     INSERT INTO APPLICANT (UID, FULL_NAME, EMAIL, PHONE, ADDRESS, BIRTH_DATE)
#     VALUES (%s, %s, %s, %s, %s, %s)
# """
# params = (uid, full_name, email, phone, address, birth_date)
# execute_query(query, params=params)
#
# # 查詢剛剛新增的資料
# result = execute_query("SELECT * FROM APPLICANT WHERE UID = %s", params=[uid], fetch=True)
# print("Inserted record:", result[0])

oid = 'O000000004'

sale = execute_query(
    "SELECT * FROM SOLDHISTORY WHERE OID = %s", (oid,), fetch=True
)[0]

ship = execute_query("SELECT * FROM `CREATE` WHERE OID = %s", (oid,), fetch=True)[0]

products = execute_query(
    "SELECT OD.PID, P.PName, OD.Quantity, OD.UPrice, OD.Subtotal FROM ORDER_DETAIL OD JOIN PRODUCT P ON OD.PID=P.PID WHERE OD.OID=%s",
    (oid,), fetch=True
)
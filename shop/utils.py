# coding=utf-8

import mysql.connector
from functools import wraps
from django.shortcuts import redirect

USER_ROLES = {
    'member': 'MEMBER',
    'seller': 'SELLER',
    'admin': 'ADMIN',
    'applicant': 'APPLICANT',
    'guest': 'GUEST',
}

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
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            conn.commit()
    finally:
        conn.close()


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            uid = request.session.get('uid')
            user_role = request.session.get('role')
            table = USER_ROLES.get(user_role)
            if user_role not in roles or not uid:
                return redirect('login')
            if user_role != 'applicant':
                sql = f"SELECT * FROM {table} WHERE UID=%s"
                if user_role != 'guest':
                    sql += " AND AccStatus='Active'"
                result = execute_query(sql, (uid,), fetch=True)
                if not result:
                    return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
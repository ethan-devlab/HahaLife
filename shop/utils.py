# coding=utf-8

import mysql.connector
from functools import wraps
from django.shortcuts import redirect


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
            user_role = request.session.get('role')
            if user_role not in roles or not request.session.get('uid'):
                return redirect('/hahalife/login/')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# def role_required(role):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             if request.session.get('role') != role or not request.session.get('uid'):
#                 return redirect('/hahalife/login/')
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator

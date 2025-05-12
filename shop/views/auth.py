# coding=utf-8

from django.shortcuts import render, redirect
from ..utils import execute_query
from django.contrib import messages
import datetime


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_roles = {
            'member': 'MEMBER',
            'seller': 'SELLER',
            'admin': 'ADMIN'
        }

        for role, table in user_roles.items():
            result = execute_query(
                f"SELECT * FROM {table} WHERE Email=%s AND Password=%s AND AccStatus='Active'",
                (email, password),
                fetch=True
            )
            if result:
                user = result[0]
                request.session['uid'] = user['UID']
                request.session['role'] = role
                request.session['uname'] = user['UName']
                request.session.set_expiry(60 * 60 * 24)  # 1 day
                if role == 'admin':
                    return redirect(f'/hahalife/admin/')
                elif role == 'seller':
                    return redirect(f'/hahalife/seller/')
                return redirect(f'/hahalife/')

        messages.error(request, 'Invalid credentials or inactive account')
    return render(request, 'shared/login.html')


def register_view(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        phonenum = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        next_uid = execute_query("SELECT LPAD(COUNT(*)+1, 9, '0') AS next_id FROM MEMBER", fetch=True)[0]['next_id']
        mid = f"M{next_uid}"

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'shared/register.html')

        existing_user = execute_query(
            "SELECT * FROM MEMBER WHERE Email=%s",
            (email,),
            fetch=True
        )
        if existing_user:
            messages.error(request, f"Email '{email}' already exists.")
            return render(request, 'shared/register.html')

        existing_phone = execute_query(
            "SELECT * FROM MEMBER WHERE PhoneNumber=%s",
            (phonenum,),
            fetch=True
        )
        if existing_phone:
            messages.error(request, f"Phone number '{phonenum}' already exists.")
            return render(request, 'shared/register.html')

        try:
            execute_query(
                "INSERT INTO MEMBER (UID, UName, AccStatus, Password, Email, Address) VALUES (%s, %s, %s, %s, %s, %s)",
                (mid, uname, 'Active', password, email, address)
            )
            messages.success(request, "Registration successful. Please log in.")
            return redirect('/hahalife/login/')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")

    return render(request, 'shared/register.html')


def guest_view(request):
    uid = "G" + str(int(datetime.datetime.timestamp(datetime.datetime.now())))
    request.session['uid'] = uid
    request.session['role'] = 'guest'
    request.session['uname'] = 'Guest'
    request.session.set_expiry(60 * 60 * 2)  # 2 hours
    return redirect(f'/hahalife/')


def logout_view(request):
    request.session.flush()
    return redirect('/hahalife/login/')

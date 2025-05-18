# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query
from django.contrib import messages
import random
import pytz
from datetime import datetime

USER_ROLES = {
    'member': 'MEMBER',
    'seller': 'SELLER',
    'admin': 'ADMIN',
    'applicant': 'APPLICANT',
}


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        for role, table in USER_ROLES.items():
            sql = f"SELECT * FROM {table} WHERE Email=%s AND Password=%s AND AccStatus='Active'"
            result = execute_query(sql, (email, password), fetch=True)
            if result:
                user = result[0]
                request.session['uid'] = user['UID']
                request.session['role'] = role
                request.session['uname'] = user['UName']
                request.session.set_expiry(60 * 60 * 24)  # 1 day

                if role == 'admin':
                    sql = "UPDATE ADMIN SET L_Login = NOW() WHERE UID = %s"
                    execute_query(sql, (user['UID'],))
                    return redirect("admin_dashboard")
                elif role == 'seller':
                    return redirect("seller_dashboard")
                return redirect(f'/hahalife/')

        messages.error(request, 'Invalid credentials or inactive account')
    return render(request, 'shared/login.html')


def register_view(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        gender = request.POST.get('gender')
        birth = request.POST.get('birth')
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
                "INSERT INTO MEMBER (UID, UName, AccStatus, Password, Email, Address, Gender, BDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (mid, uname, 'Active', password, email, address, gender, birth)
            )
            messages.success(request, "Registration successful. Please log in.")
            return redirect('/hahalife/login/')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")

    return render(request, 'shared/register.html')


def guest_view(request):
    uid = "G" + str(random.randint(100000000, 999999999))
    while execute_query("SELECT * FROM GUEST WHERE UID = %s", (uid,), fetch=True):
        uid = "G" + str(random.randint(100000000, 999999999))
    request.session['uid'] = uid
    request.session['role'] = 'guest'
    request.session['uname'] = 'Guest'
    request.session.set_expiry(60 * 60 * 2)  # 2 hours
    TPE = pytz.timezone('Asia/Taipei')
    now = str(datetime.now(TPE).strftime('%Y%m%d%H%M%S'))
    name = f"G{now}"
    execute_query(
        "INSERT INTO GUEST (UID, UName) VALUES (%s, %s)",
        (uid, name)
    )
    return redirect(f'/hahalife/')


def applicant_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        sql = "SELECT * FROM APPLICANT WHERE Email=%s AND Password=%s"
        result = execute_query(sql, (email, password), fetch=True)
        if result:
            applicant = result[0]
            request.session['uid'] = applicant['AppID']
            request.session['role'] = 'applicant'
            request.session['uname'] = applicant['Name']
            request.session.set_expiry(60 * 60 * 24)

            return redirect("apply_status")

        messages.error(request, 'Invalid credentials or account does not exist')
    return render(request, 'applicant/applicant_login.html')


def logout_view(request):
    request.session.flush()
    return redirect('/hahalife/login/')

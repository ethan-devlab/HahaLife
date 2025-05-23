# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query
from django.contrib import messages
import random
import pytz
from datetime import datetime

LOGIN_SQL = "SELECT * FROM {table} WHERE Email=%s AND Password=%s AND AccStatus='Active'"
LOGIN_ERROR_MESSAGE = "Invalid credentials or inactive account"


def member_login_view(request):
    if request.method == 'POST':
        email = str(request.POST.get('email')).lower()  # avoid case-sensitive issues
        password = request.POST.get('password')

        result = execute_query(LOGIN_SQL.format(table="MEMBER"), (email, password), fetch=True)
        if result:
            user = result[0]
            request.session['uid'] = user['UID']
            request.session['role'] = 'member'
            request.session['uname'] = user['UName']
            request.session.set_expiry(60 * 60 * 24)  # 1 day

            return redirect(f'/hahalife/')

        messages.error(request, LOGIN_ERROR_MESSAGE)
    return render(request, 'shared/member_login.html')


def seller_login_view(request):
    if request.method == 'POST':
        email = str(request.POST.get('email')).lower()  # avoid case-sensitive issues
        password = request.POST.get('password')

        result = execute_query(LOGIN_SQL.format(table="SELLER"), (email, password), fetch=True)
        if result:
            user = result[0]
            request.session['uid'] = user['UID']
            request.session['role'] = 'seller'
            request.session['uname'] = user['UName']
            request.session.set_expiry(60 * 60 * 24)  # 1 day
            
            return redirect("seller_dashboard")

        messages.error(request, LOGIN_ERROR_MESSAGE)
    return render(request, 'shared/seller_login.html')


def admin_login_view(request):
    if request.method == 'POST':
        email = str(request.POST.get('email')).lower()  # avoid case-sensitive issues
        password = request.POST.get('password')

        result = execute_query(LOGIN_SQL.format(table="ADMIN"), (email, password), fetch=True)
        if result:
            user = result[0]
            request.session['uid'] = user['UID']
            request.session['role'] = 'admin'
            request.session['uname'] = user['UName']
            request.session.set_expiry(60 * 60 * 24)  # 1 day

            return redirect("admin_dashboard")

        messages.error(request, LOGIN_ERROR_MESSAGE)
    return render(request, 'shared/admin_login.html')


def member_register_view(request):
    err_response = render(request, 'shared/member_register.html')

    if request.method == 'POST':
        uname = request.POST.get('uname')
        gender = request.POST.get('gender')
        birth = request.POST.get('birth')
        email = str(request.POST.get('email')).lower()  # avoid case-sensitive issues
        phonenum = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        next_uid = execute_query("SELECT LPAD(COUNT(*)+1, 9, '0') AS next_id FROM MEMBER", fetch=True)[0]['next_id']
        mid = f"M{next_uid}"

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return err_response

        existing_user = execute_query(
            "SELECT * FROM MEMBER WHERE Email=%s",
            (email,),
            fetch=True
        )
        if existing_user:
            messages.error(request, f"Email '{email}' already exists.")
            return err_response

        existing_phone = execute_query(
            "SELECT * FROM MEMBER WHERE PhoneNumber=%s",
            (phonenum,),
            fetch=True
        )
        if existing_phone:
            messages.error(request, f"Phone number '{phonenum}' already exists.")
            return err_response

        try:
            execute_query(
                "INSERT INTO MEMBER (UID, UName, AccStatus, Password, Email, Address, Gender) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (mid, uname, 'Active', password, email, address, gender)
            )

            if birth and birth != "":
                execute_query("UPDATE MEMBER SET BDate = %s WHERE UID = %s", (birth, mid))

            # messages.success(request, "Registration successful. Please log in.")
            return render(request, 'shared/register_success.html', {
                'uname': uname,
            })
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")

    return render(request, 'shared/member_register.html')


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


def applicant_login_view(request):
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
    role = request.session.get('role')
    request.session.flush()
    if role == "guest":
        role = "member"

    return redirect(f'/hahalife/{role}/login/')


# testing purpose
def register_success(request):
    return render(request, 'shared/register_success.html')

# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from django.contrib import messages


@role_required('member', 'seller', 'admin')
def account_view(request):
    uid = request.session.get('uid')
    role = request.session.get('role')
    # if not uid or not role:
    #     return redirect('/hahalife/login/')

    table = {'member': 'MEMBER', 'seller': 'SELLER', 'admin': 'ADMIN'}.get(role)

    sql = """
        SELECT UID, UName, AccStatus, Email, Address, PhoneNumber
    """

    if role == "admin":
        sql += ", L_Login"
    elif role == "seller":
        sql += ", SName"
    elif role == "member":
        sql += ", MLevel, Gender, BDate"

    sql += f" FROM {table} WHERE UID = %s"

    user = execute_query(sql, (uid,), fetch=True)[0]
    user['Address'] = user['Address'] or ''
    user['PhoneNumber'] = user['PhoneNumber'] or ''

    user['role'] = role

    if role == 'member':
        user['BDate'] = str(user['BDate']) or ''

    if role == 'admin':
        role = 'customadmin'

    return render(request, f'shared/account.html', {
                    'user': user,
                    'role': role,
                })


@role_required('member', 'seller', 'admin')
def update_account(request):
    uid = request.session.get('uid')
    role = request.session.get('role')
    # if request.method != 'POST':
    #     return redirect('/hahalife/login/')
    table = {'member': 'MEMBER', 'seller': 'SELLER', 'admin': 'ADMIN'}.get(role)

    uname = request.POST.get('uname')
    gender = request.POST.get('gender')
    birth = request.POST.get('birth')
    sname = request.POST.get('sname')
    email = request.POST.get('email')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    password = request.POST.get('password')

    # Validate if email or phone or shop name is unique
    if email:
        sql = f"SELECT UID FROM {table} WHERE Email = %s AND UID != %s"
        if execute_query(sql, (email, uid), fetch=True):
            messages.error(request, 'Email already exists.')
            return redirect('account')
    if phone:
        sql = f"SELECT UID FROM {table} WHERE PhoneNumber = %s AND UID != %s"
        if execute_query(sql, (phone, uid), fetch=True):
            messages.error(request, 'Phone number already exists.')
            return redirect('account')
    if sname:
        sql = f"SELECT UID FROM {table} WHERE SName = %s AND UID != %s"
        if execute_query(sql, (sname, uid), fetch=True):
            messages.error(request, 'Shop name already exists.')
            return redirect('account')

    params = [uname, email, address, phone]
    sql = f"""
        UPDATE {table} SET UName = %s, Email = %s, Address = %s, PhoneNumber = %s
        """
    if birth and birth != "":
        sql += ", BDate = %s"
        params.append(birth)
    elif birth and birth == "":
        sql += ", BDate = NULL"

    if gender:
        sql += ", Gender = %s"
        params.append(gender)
    if sname:
        sql += ", SName = %s"
        params.append(sname)
    if password:
        sql += ", Password = %s"
        params.append(password)
    sql += " WHERE UID = %s"
    params.append(uid)

    execute_query(sql, tuple(params))
    messages.success(request, 'Account updated successfully.')
    return redirect('account')

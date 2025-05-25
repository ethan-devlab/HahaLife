# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from django.contrib import messages


@role_required('admin')
def manage_user(request):
    members = execute_query(
        "SELECT UID, UName, Email, AccStatus FROM MEMBER", fetch=True
    )
    sellers = execute_query(
        "SELECT UID, UName, Email, AccStatus FROM SELLER", fetch=True
    )

    user = None

    # If form submitted to update status
    if request.method == 'POST' and 'status' in request.POST:
        uid = request.POST.get('uid')
        new_status = request.POST.get('status')

        if uid.startswith('M'):
            table = 'MEMBER'
        elif uid.startswith('S'):
            table = 'SELLER'
        else:
            table = None

        if table:
            execute_query(
                f"UPDATE {table} SET AccStatus=%s WHERE UID=%s",
                (new_status, uid)
            )
            messages.success(request, f"Updated {uid} to {new_status}.")
        else:
            messages.error(request, "Invalid UID.")

        return redirect("manage_user")

    # Load user details for editing if requested via GET or POST
    uid_to_load = request.GET.get('uid') or request.POST.get('uid')
    if uid_to_load:
        if uid_to_load.startswith('M'):
            table = 'MEMBER'
        elif uid_to_load.startswith('S'):
            table = 'SELLER'
        else:
            table = None

        if table:
            result = execute_query(
                f"SELECT UID, UName, Email, AccStatus FROM {table} WHERE UID=%s",
                (uid_to_load,),
                fetch=True
            )
            if result:
                user = result[0]
                user['role'] = table.capitalize()
            else:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid UID.")

    return render(request, 'customadmin/manage_user.html', {
        'members': members,
        'sellers': sellers,
        'user': user,
    })


@role_required('admin')
def manage_product(request):
    products = execute_query(
        "SELECT PID, PName, Category, Price, Stock FROM PRODUCT", fetch=True
    )

    product = None

    if request.method == 'POST' and request.POST.get('action') == 'remove':
        pid = request.POST.get('pid')
        result = execute_query("SELECT * FROM PRODUCT WHERE PID = %s", (pid,), fetch=True)
        if result:
            execute_query("DELETE FROM PRODUCT WHERE PID = %s", (pid,))
            messages.success(request, f'Product {pid} removed.')
        else:
            messages.error(request, 'Product not found.')
        return redirect('manage_product')

    # Load specific product for details
    pid_to_load = request.POST.get('pid') or request.GET.get('pid')
    if pid_to_load:
        result = execute_query("SELECT * FROM PRODUCT WHERE PID = %s", (pid_to_load,), fetch=True)
        if result:
            product = result[0]
        else:
            messages.error(request, 'Product not found.')

    return render(request, 'customadmin/manage_product.html', {
        'products': products,
        'product': product,
    })

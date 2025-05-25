# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib import messages
from ...utils import execute_query, role_required
from django.views.decorators.csrf import csrf_exempt
import json


def get_cart_id(uid):
    sql = "SELECT CartID FROM SHOPPINGCART WHERE UID = %s"
    result = execute_query(sql, (uid,), fetch=True)
    if result:
        return result[0]['CartID']


@role_required('member')
def view_cart(request):
    uid = request.session.get('uid')
    # if not uid:
    #     return redirect('/hahalife/login/')
    cart_id = get_cart_id(uid)

    # Fetch cart items
    sql = """
        SELECT A.PID, P.PName, P.Price, A.Quantity, (P.Price * A.Quantity) AS Subtotal, S.SName, P.Stock
        FROM ADDED_TO A
        JOIN PRODUCT P ON A.PID = P.PID
        JOIN SELLER S ON P.SID = S.UID
        WHERE A.CartID = %s
    """
    items = execute_query(sql, (cart_id,), fetch=True)
    total_qty = sum(item['Quantity'] for item in items)
    total_price = sum(item['Subtotal'] for item in items)

    # Fetch available promos for these products
    promo_map = {}
    if items:
        pids = [item['PID'] for item in items]
        placeholders = ','.join(['%s'] * len(pids))
        sql2 = f"""
            SELECT HP.PID, HP.PromoCode, PR.DisAmount
            FROM HAS_PROMO HP
            JOIN PROMOTION PR ON HP.PromoCode = PR.PromoCode
            WHERE HP.PID IN ({placeholders})
        """
        promo_records = execute_query(sql2, pids, fetch=True)
        for pr in promo_records:
            promo_map.setdefault(pr['PID'], {})[pr['PromoCode']] = pr['DisAmount']

    return render(request, 'member/cart.html', {
        'items': items,
        'total_qty': total_qty,
        'total_price': total_price,
        'promo_map_json': json.dumps(promo_map),
    })


@role_required('member')
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        cart_id = get_cart_id(uid)
        pid = request.POST.get('pid')
        qty = int(request.POST.get('quantity'))

        try:
            check = execute_query("SELECT 1 FROM ADDED_TO WHERE CartID = %s AND PID = %s", (cart_id, pid), fetch=True)
            if check:
                execute_query("UPDATE ADDED_TO SET Quantity = Quantity + %s WHERE CartID = %s AND PID = %s",
                            (qty, cart_id, pid))
            else:
                execute_query("INSERT INTO ADDED_TO (CartID, PID, Quantity) VALUES (%s, %s, %s)",
                              (cart_id, pid, qty))

            messages.success(request, "Product added to cart successfully!")
            # Primarily returns to the previous page
            # print(request.META.get('HTTP_REFERER'))
            return redirect(request.META.get('HTTP_REFERER', f'/hahalife/product/{pid}/'))
        
        except Exception as e:
            messages.error(request, f"Error adding product to cart: {str(e)}")

    return redirect('/hahalife/')


@role_required('member')
def delete_from_cart(request, pid):
    cart_id = get_cart_id(request.session['uid'])
    execute_query("DELETE FROM ADDED_TO WHERE CartID = %s AND PID = %s", (cart_id, pid))
    return redirect('/hahalife/cart/')


@role_required('member')
def update_quantity(request, pid):
    if request.method == 'POST':
        cart_id = get_cart_id(request.session['uid'])
        qty = int(request.POST.get('quantity'))
        if qty > 0:
            execute_query("UPDATE ADDED_TO SET Quantity = %s WHERE CartID = %s AND PID = %s",
                          (qty, cart_id, pid))
        else:
            return delete_from_cart(request, pid)

    return redirect('/hahalife/cart/')

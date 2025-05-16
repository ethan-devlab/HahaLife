# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from ...utils import execute_query, role_required


@role_required('seller')
def order_list(request):
    sid = request.session['uid']
    orders = execute_query(
        "SELECT SHID, OID, SDate, TotalPrice FROM SOLDHISTORY WHERE SID = %s ORDER BY SDate DESC",
        (sid,), fetch=True
    )
    return render(request, 'seller/order.html', {'orders': orders})


@role_required('seller')
def order_detail_s(request, oid):
    sid = request.session['uid']
    sale = execute_query(
        "SELECT * FROM SOLDHISTORY WHERE OID = %s AND SID = %s",
        (oid, sid), fetch=True
    )
    if not sale:
        return redirect('/hahalife/seller/order/')
    sale = sale[0]

    if request.method == 'POST':
        ostatus = request.POST['ostatus']
        pay_status = request.POST['pay_status']
        ship_status = request.POST['ship_status']
        courier = request.POST['courier']
        track_number = request.POST['track_number']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        execute_query("UPDATE `ORDER` SET OStatus=%s WHERE OID=%s", (ostatus, oid))
        execute_query("UPDATE ORDERHISTORY SET OStatus=%s WHERE OID=%s", (ostatus, oid))
        execute_query("UPDATE PAID_BY SET PayStatus=%s WHERE OID=%s", (pay_status, oid))
        execute_query(
            "UPDATE `CREATE` SET ShipStatus=%s, Courier=%s, TrackNumber=%s, UptTime=%s WHERE OID=%s",
            (ship_status, courier, track_number, now, oid)
        )
        messages.success(request, 'Order updated successfully.')
        return redirect(f'/hahalife/seller/order/{oid}/')

    ship = execute_query("SELECT * FROM `CREATE` WHERE OID=%s", (oid,), fetch=True)[0]
    payment = execute_query("SELECT PayMethod, PayStatus FROM PAID_BY WHERE OID=%s", (oid,), fetch=True)[0]
    
    products = execute_query(
        """
        SELECT OD.PID, P.PName, OD.Quantity, OD.UPrice, OD.Subtotal,
               R.Sell_R, R.Buy_R
        FROM ORDER_DETAIL OD 
        JOIN PRODUCT P ON OD.PID=P.PID 
        LEFT JOIN REVIEW R ON OD.PID = R.PID AND R.RevID = CONCAT('R', RIGHT(%s, 5), RIGHT(OD.PID, 3))
        WHERE OD.OID=%s
        """,
        (oid, oid), fetch=True
    )

    return render(request, 'seller/order_detail.html', {
        'sale': sale,
        'ship': ship,
        'payment': payment,
        'products': products
    })


@role_required('seller')
def submit_seller_review(request, oid, pid):
    if request.method == 'POST':
        sell_r = request.POST.get('sell_r', '')
        rev_id = 'R' + oid[-5:] + pid[-3:]
        
        execute_query("""
            INSERT INTO REVIEW (RevID, PID, Sell_R) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE Sell_R = VALUES(Sell_R)
        """, (rev_id, pid, sell_r))
        
        return redirect(f'/hahalife/seller/order/{oid}/')
    return None
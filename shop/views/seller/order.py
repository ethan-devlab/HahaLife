# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import random
import pytz
from ...utils import execute_query, role_required


@role_required('seller')
def order_list(request):
    sid = request.session['uid']
    orders = execute_query(
        "SELECT SHID, OID, SDate, TotalPrice FROM SOLDHISTORY WHERE SID = %s ORDER BY SDate DESC",
        (sid,), fetch=True
    )
    return render(request, 'seller/order.html', {'orders': orders})


def generate_notification_id(oid, mid):
    nid = "N" + oid[7:] + mid[7:] + str(random.randint(100, 999))
    while execute_query("SELECT NID FROM NOTIFICATION WHERE NID = %s", (nid,), fetch=True):
        nid = "N" + oid[7:] + mid[7:] + str(random.randint(100, 999))
    return nid


@role_required('seller')
def order_detail(request, oid):
    # Fetch sale summary (from SOLDHISTORY)
    sale = execute_query(
        """
        SELECT * FROM SOLDHISTORY WHERE OID = %s
        """,
        (oid,),
        fetch=True
    )
    if not sale:
        return render(request, '404.html')
    sale = sale[0]

    # Fetch order, payment, shipment info
    order = execute_query("SELECT * FROM `ORDER` WHERE OID = %s", (oid,), fetch=True)[0]
    payment = execute_query("SELECT * FROM PAID_BY WHERE OID = %s", (oid,), fetch=True)
    payment = payment[0] if payment else {}
    ship = execute_query("SELECT * FROM `CREATE` WHERE OID = %s", (oid,), fetch=True)
    ship = ship[0] if ship else {}

    # Fetch current statuses (for comparison)
    current_status = execute_query("""
        SELECT O.OStatus, C.ShipStatus, P.PayStatus, C.TrackNumber
        FROM `ORDER` O
        LEFT JOIN `CREATE` C ON O.OID = C.OID
        LEFT JOIN PAID_BY P ON O.OID = P.OID
        WHERE O.OID = %s
    """, (oid,), fetch=True)
    if current_status:
        current_status = current_status[0]
    else:
        current_status = {'OStatus': None, 'ShipStatus': None, 'PayStatus': None, 'TrackNumber': None}

    # Fetch products (with promo/review)
    products = execute_query(
        """
        SELECT OD.PID, P.PName, OD.Quantity, OD.UPrice, OD.Subtotal,
               UP.PromoCode, PR.DisAmount,
               R.Sell_R, R.Buy_R
        FROM ORDER_DETAIL OD
        JOIN PRODUCT P ON OD.PID = P.PID
        LEFT JOIN USE_PROMO UP ON OD.OID = UP.OID AND OD.PID = UP.PID
        LEFT JOIN PROMOTION PR ON UP.PromoCode = PR.PromoCode
        LEFT JOIN REVIEW R ON OD.PID = R.PID AND R.RevID = CONCAT('R', RIGHT(%s, 5), RIGHT(OD.PID, 3))
        WHERE OD.OID = %s
        """,
        (oid, oid),
        fetch=True
    )

    if request.method == 'POST':
        new_ostatus = request.POST.get('ostatus')
        new_ship_status = request.POST.get('ship_status')
        new_pay_status = request.POST.get('pay_status')
        new_courier = request.POST.get('courier')

        notify_msgs = []

        # Only update and notify if status changed
        if new_ostatus and new_ostatus != current_status['OStatus']:
            execute_query("UPDATE `ORDER` SET OStatus = %s WHERE OID = %s", (new_ostatus, oid))
            # Notification logic for order status change
            if new_ostatus == "Shipped":
                notify_msgs.append(f"Your order {oid} has been shipped.")
            elif new_ostatus == "Delivered":
                notify_msgs.append(f"Good news! Your order {oid} has been delivered.")
            elif new_ostatus == "Cancelled":
                notify_msgs.append(f"Your order {oid} has been cancelled by the seller.")

        if new_ship_status and new_ship_status != current_status['ShipStatus']:
            execute_query("UPDATE `CREATE` SET ShipStatus = %s WHERE OID = %s", (new_ship_status, oid))
            if new_ship_status == "In Transit":
                notify_msgs.append(f"Your order {oid} is now in transit. Tracking number: {new_track_number}.")
            elif new_ship_status == "Delivered":
                notify_msgs.append(f"Order {oid} was delivered successfully. If you have any questions, please contact support.")

        if new_pay_status and new_pay_status != current_status['PayStatus']:
            execute_query("UPDATE PAID_BY SET PayStatus = %s WHERE OID = %s", (new_pay_status, oid))
            if new_pay_status == "Completed":
                notify_msgs.append(f"Payment for order {oid} has been completed. Thank you!")
            elif new_pay_status == "Failed":
                notify_msgs.append(f"Payment for order {oid} failed. Please check your payment method.")

        if new_courier != ship.get('Courier'):
            execute_query("UPDATE `CREATE` SET Courier = %s WHERE OID = %s",
                          (new_courier, oid))

        # Only notify if something actually changed
        if notify_msgs:
            TPE = pytz.timezone('Asia/Taipei')
            now = datetime.now().astimezone(TPE).strftime('%Y-%m-%d %H:%M:%S')
            for msg in notify_msgs:
                nid = generate_notification_id(oid, order['MID'])
                execute_query(
                    """
                    INSERT INTO NOTIFICATION (NID, MID, OID, Message, NotifyTime, IsRead)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (nid, order['MID'], oid, msg, now, False)
                )
        messages.success(request, "Order status updated successfully.")

        return redirect(request.path)

    return render(request, 'seller/order_detail.html', {
        'sale': sale,
        'order': order,
        'payment': payment,
        'ship': ship,
        'products': products,
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
        
        # return redirect(f'/hahalife/seller/order/{oid}/')
        return redirect("seller_order_detail", oid=oid)
    
    return None
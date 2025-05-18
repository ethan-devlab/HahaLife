# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required


@role_required('member')
def purchase_list(request):
    uid = request.session.get('uid')
    # if not uid:
    #     return redirect('/hahalife/login/')
    sql = """
        SELECT OH.OID, OH.OrderDate, OH.TotalAmount, OH.OStatus, PB.PayMethod, PB.PayStatus
        FROM ORDERHISTORY OH
        LEFT JOIN PAID_BY PB ON OH.OID = PB.OID
        WHERE OH.MID = %s
        ORDER BY OH.OrderDate DESC
    """
    history = execute_query(sql, (uid,), fetch=True)
    return render(request, 'member/purchase.html', {'orders': history})


@role_required('member')
def purchase_detail(request, oid):
    # Order-level info
    order_info = execute_query("""
        SELECT OH.*, PB.PayMethod, PB.PayStatus, CR.Courier, CR.TrackNumber, CR.ShipStatus
        FROM ORDERHISTORY OH
        LEFT JOIN PAID_BY PB ON OH.OID = PB.OID
        LEFT JOIN `CREATE` CR ON OH.OID = CR.OID
        WHERE OH.OID = %s
    """, (oid,), fetch=True)[0]

    # Product details (with promo and review)
    products = execute_query("""
        SELECT OD.PID, P.PName, OD.Quantity, OD.UPrice, OD.Subtotal,
               UP.PromoCode, PR.DisAmount,
               R.Sell_R, R.Buy_R
        FROM ORDER_DETAIL OD
        JOIN PRODUCT P ON OD.PID = P.PID
        LEFT JOIN USE_PROMO UP ON OD.OID = UP.OID AND OD.PID = UP.PID
        LEFT JOIN PROMOTION PR ON UP.PromoCode = PR.PromoCode
        LEFT JOIN REVIEW R ON OD.PID = R.PID AND R.RevID = CONCAT('R', RIGHT(%s, 5), RIGHT(OD.PID, 3))
        WHERE OD.OID = %s
    """, (oid, oid), fetch=True)

    return render(request, 'member/purchased_detail.html', {
        'order': order_info,
        'products': products
    })


@role_required('member')
def cancel_order(request, oid):
    execute_query("UPDATE `ORDER` SET OStatus = 'Cancelled' WHERE OID = %s AND OStatus != 'Shipped'", (oid,))
    execute_query("UPDATE ORDERHISTORY SET OStatus = 'Cancelled' WHERE OID = %s AND OStatus != 'Shipped'", (oid,))
    # Restore stock
    execute_query("""
        UPDATE PRODUCT P
        JOIN ORDER_DETAIL OD ON P.PID = OD.PID
        SET P.Stock = P.Stock + OD.Quantity
        WHERE OD.OID = %s
    """, (oid,))

    return redirect(f'/hahalife/mypurchase/{oid}/')


@role_required('member')
def submit_review(request, oid, pid):
    if request.method == 'POST':
        # sell_r = request.POST.get('sell_r', '')
        buy_r = request.POST.get('buy_r', '')
        rev_id = 'R' + oid[-5:] + pid[-3:]

        # execute_query("REPLACE INTO REVIEW (RevID, PID, Sell_R, Buy_R) VALUES (%s, %s, %s, %s)",
        #               (rev_id, pid, sell_r, buy_r))
        execute_query("REPLACE INTO REVIEW (RevID, PID, Buy_R) VALUES (%s, %s, %s)",
                      (rev_id, pid, buy_r))
        return redirect(f'/hahalife/mypurchase/{oid}/')
    return None

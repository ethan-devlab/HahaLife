# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from datetime import datetime
import random
import json


@role_required('member')
def checkout_view(request):
    uid = request.session.get('uid')
    # if not uid or request.method != 'POST':
    #     return redirect('/hahalife/cart/')

    cart_id = f'CART{uid[-5:]}'
    selected = request.POST.getlist('selected_pids')

    # Fetch selected items
    sql = f"""
        SELECT P.PID, P.PName, P.Price, C.Quantity, (P.Price * C.Quantity) AS Subtotal,
               S.SName, P.SID
        FROM SHOPPINGCART C
        JOIN PRODUCT P ON C.PID = P.PID
        JOIN SELLER S ON P.SID = S.UID
        WHERE C.CartID = %s AND C.PID IN ({','.join(['%s'] * len(selected))})
    """
    items = execute_query(sql, [cart_id] + selected, fetch=True)
    total = sum(item['Subtotal'] for item in items)

    # Fetch promos for these products
    promo_map = {}
    if items:
        pids = [i['PID'] for i in items]
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

    return render(request, 'member/checkout.html', {
        'items': items,
        'total': total,
        'selected_pids': selected,
        'promo_map_json': json.dumps(promo_map),
    })


@role_required('member')
def place_order(request):
    if request.method != 'POST':
        return redirect('/hahalife/cart/')

    uid = request.session['uid']
    cart_id = f'CART{uid[-5:]}'
    selected = request.POST.getlist('selected_pids')
    postal_code = request.POST['postal_code']
    city = request.POST['city']
    district = request.POST['district']
    street = request.POST['street']
    address = f"{postal_code}{city}{district}{street}"
    shipping = request.POST['shipping']
    ploc = request.POST['pickup_location']
    pay_method = request.POST['pay_method']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Fetch all items and group by seller
    items = execute_query(
        f"""
        SELECT C.PID, C.Quantity, P.Price, P.SID
        FROM SHOPPINGCART C
        JOIN PRODUCT P ON C.PID = P.PID
        WHERE C.CartID = %s AND C.PID IN ({','.join(['%s'] * len(selected))})
        """,
        [cart_id] + selected,
        fetch=True
    )

    # Group items by seller
    seller_items = {}
    for item in items:
        if item['SID'] not in seller_items:
            seller_items[item['SID']] = []
        seller_items[item['SID']].append(item)

    order_ids = []  # Store all created order IDs

    # Process orders for each seller
    for seller_id, seller_products in seller_items.items():
        # Generate unique OID
        while True:
            oid = 'O' + str(random.randint(100000000, 999999999))
            check_oid = execute_query("SELECT 1 FROM `ORDER` WHERE OID = %s", [oid], fetch=True)
            if not check_oid:
                break

        order_ids.append(oid)
        seller_total = 0
        seller_promo_codes = []

        # Calculate total and handle promos for this seller's items
        for item in seller_products:
            item_total = item['Quantity'] * item['Price']
            code = request.POST.get(f'promo_{item["PID"]}', '').strip()
            if code:
                promo_info = execute_query(
                    """
                    SELECT PR.DisAmount
                    FROM PROMOTION PR
                    JOIN HAS_PROMO HP ON PR.PromoCode = HP.PromoCode
                    WHERE PR.PromoCode = %s AND HP.PID = %s
                    """,
                    [code, item['PID']],
                    fetch=True
                )
                if promo_info:
                    item_total -= promo_info[0]['DisAmount']
                    seller_promo_codes.append(code)
            seller_total += item_total

        # Insert seller-specific order
        execute_query(
            """
            INSERT INTO `ORDER`
              (OID, OStatus, SID, Address, TotalAmount, MID, CreatedAt)
            VALUES
              (%s, 'Processing', %s, %s, %s, %s, %s)
            """,
            (oid, seller_id, address, seller_total, uid, created_at)
        )

        # Insert promo codes used
        for promo_code in seller_promo_codes:
            execute_query(
                """
                INSERT INTO USE_PROMO (PromoCode, OID)
                VALUES (%s, %s)
                """,
                (promo_code, oid)
            )

        # Insert order details for each product
        for item in seller_products:
            item_discount = 0
            promo_code = request.POST.get(f'promo_{item["PID"]}', '').strip()
            if promo_code:
                promo_info = execute_query(
                    """
                    SELECT PR.DisAmount
                    FROM PROMOTION PR
                    JOIN HAS_PROMO HP ON PR.PromoCode = HP.PromoCode
                    WHERE PR.PromoCode = %s AND HP.PID = %s
                    """,
                    [promo_code, item['PID']],
                    fetch=True
                )
                if promo_info:
                    item_discount = promo_info[0]['DisAmount']

            subtotal = (item['Quantity'] * item['Price']) - item_discount
            execute_query(
                """
                INSERT INTO ORDER_DETAIL (OID, PID, Quantity, UPrice, Subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (oid, item['PID'], item['Quantity'], item['Price'], subtotal)
            )

        # Payment for this order
        execute_query(
            """
            INSERT INTO PAID_BY (PayID, OID, PayMethod, PayStatus)
            VALUES (%s, %s, %s, 'Pending')
            """,
            ('PAY' + oid[-6:], oid, pay_method)
        )

        # Shipment for this order
        execute_query(
            """
            INSERT INTO `CREATE` (ShipID, OID, UptTime, ShipStatus, TrackNumber, Courier)
            VALUES (%s, %s, %s, 'Preparing', %s, %s)
            """,
            (
                'SHIP' + oid[-6:], oid, created_at,
                'T' + str(random.randint(1000000000000000, 9999999999999999)),
                ploc if shipping == "store_pickup" else shipping
            )
        )

        # Order history for this order
        ohid = 'OH' + uid[8:10] + oid[-6:]
        execute_query(
            """
            INSERT INTO ORDERHISTORY
              (OHID, OID, MID, OrderDate, TotalAmount, OStatus, PayMethod)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s)
            """,
            (ohid, oid, uid, created_at, seller_total, 'Processing', pay_method)
        )

        # Sold history for this order
        execute_query(
            """
            INSERT INTO SOLDHISTORY (SHID, OID, SID, PromoCode, PayMethod, SDate, TotalPrice, BID, Quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                'SH' + seller_id[8:10] + oid[-6:], oid, seller_id, ','.join(seller_promo_codes),
                pay_method, created_at, seller_total, uid, sum(item['Quantity'] for item in seller_products)
            )
        )

        # Deduct stock for this seller's products
        for item in seller_products:
            execute_query(
                """
                UPDATE PRODUCT
                SET Stock = Stock - %s
                WHERE PID = %s
                """,
                (item['Quantity'], item['PID'])
            )

    # Clear cart for all processed items
    for pid in selected:
        execute_query("DELETE FROM ADDED_TO WHERE CartID = %s AND PID = %s", (cart_id, pid))
        execute_query("DELETE FROM SHOPPINGCART WHERE CartID = %s AND PID = %s", (cart_id, pid))

    return render(request, 'member/checkout_success.html')

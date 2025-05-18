# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from datetime import datetime
from tzlocal import get_localzone
import pytz


@role_required('member', 'guest')
def product_list(request):
    # uid = request.session.get('uid')
    # if not uid or request.session.get('role') != 'member':
    #     return redirect('/hahalife/login/')

    name = request.GET.get('search', '')
    tag = request.GET.get('tag')
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    discount_only = request.GET.get('discount') == '1'
    sort = request.GET.get('sort')

    sql = """
          SELECT P.PID, P.PName, P.Category, P.Stock, P.Price,
                EXISTS (
                    SELECT 1 FROM HAS_PROMO HP
                    WHERE HP.PID = P.PID
                ) AS HasPromo,
                CASE
                    WHEN EXISTS (
                        SELECT 1 FROM HAS_PROMO HP
                        WHERE HP.PID = P.PID
                    ) THEN (
                        SELECT Pr.DisAmount FROM HAS_PROMO HP
                        JOIN PROMOTION Pr ON HP.PromoCode = Pr.PromoCode
                        WHERE HP.PID = P.PID
                        LIMIT 1
                    )
                    ELSE NULL
                END AS DisAmount,
                COALESCE(SC.SoldCount, 0) AS SoldCount,
                GROUP_CONCAT(DISTINCT PT.Tag) AS Tags
            FROM PRODUCT P
            LEFT JOIN (
                SELECT PID, SUM(Quantity) AS SoldCount
                FROM ORDER_DETAIL
                GROUP BY PID
            ) SC ON P.PID = SC.PID
            LEFT JOIN PRODUCT_TAG PT ON P.PID = PT.PID
            WHERE 1=1
        """

    params = []

    if name:
        sql += " AND (P.PName LIKE %s OR P.PID LIKE %s)"
        params += [f'%{name}%', f'%{name}%']
    if tag:
        sql += " AND PT.Tag = %s"
        params.append(tag)
    if category:
        sql += " AND P.Category = %s"
        params.append(category)
    if price_min:
        sql += " AND P.Price >= %s"
        params.append(price_min)
    if price_max:
        sql += " AND P.Price <= %s"
        params.append(price_max)
    if discount_only:
        sql += " AND EXISTS (SELECT 1 FROM HAS_PROMO HP WHERE HP.PID = P.PID)"

    sql += " GROUP BY P.PID"

    if sort == 'low':
        sql += " ORDER BY P.Price ASC"
    elif sort == 'high':
        sql += " ORDER BY P.Price DESC"

    products = execute_query(sql, params, fetch=True)

    print(products)

    categories = execute_query("SELECT DISTINCT Category FROM PRODUCT", fetch=True)
    tags = execute_query("SELECT DISTINCT Tag FROM PRODUCT_TAG", fetch=True)

    return render(request, 'member/index.html',
                  {
                        'products': products,
                        'categories': categories,
                        'tags': tags,
                        'role': request.session.get('role'),
                  }
                  )


@role_required('member')
def product_detail(request, pid):
    # uid = request.session.get('uid')
    # if not uid or request.session.get('role') != 'member':
    #     return redirect('/hahalife/login/')

    sql = """
        SELECT 
            P.PID, P.PName, P.Category, P.Price, P.Stock, P.Descript, S.SName AS SellerName,
            Pr.PromoCode, Pr.DisAmount, GROUP_CONCAT(PT.Tag) AS Tags
        FROM PRODUCT P
        JOIN SELLER S ON P.SID = S.UID
        LEFT JOIN HAS_PROMO HP ON P.PID = HP.PID
        LEFT JOIN PROMOTION Pr ON HP.PromoCode = Pr.PromoCode
        LEFT JOIN PRODUCT_TAG PT ON P.PID = PT.PID
        WHERE P.PID = %s
        GROUP BY P.PID, P.PName, P.Category, P.Price, P.Stock, P.Descript, S.SName, Pr.PromoCode, Pr.DisAmount
        LIMIT 1
        """

    product = execute_query(sql, (pid,), fetch=True)[0]

    reviews = execute_query(
        "SELECT Sell_R AS seller_review, Buy_R AS buyer_review FROM REVIEW WHERE PID = %s",
        (pid,), fetch=True
    )

    return render(request, 'member/product_detail_m.html', {
        'product': product,
        'reviews': reviews
    })

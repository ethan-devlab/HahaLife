# coding=utf-8

from django.shortcuts import render
from ...utils import execute_query, role_required


@role_required('member')
def seller_product(request, sname):
    sql = """
          SELECT P.PID, P.PName, P.Category, P.Stock, P.Price, P.ImagePath,
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
            WHERE P.SID = (
                SELECT UID FROM SELLER WHERE SName = %s
            )
            GROUP BY P.PID
        """
    
    products = execute_query(sql, (sname,), fetch=True)

    return render(request, 'member/shop.html', {'products': products, 'seller': sname})
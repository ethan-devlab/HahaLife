# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.conf import settings
import os


def check_permission(sid, pid):
    permission = execute_query(
        "SELECT 1 FROM PRODUCT WHERE PID = %s AND SID = %s", (pid, sid), fetch=True
    )
    return bool(permission)


@role_required('seller')
def add_product(request):
    promotions = execute_query(
        """
        SELECT PromoCode, DisAmount 
        FROM PROMOTION P
        WHERE P.SID IS NULL OR P.SID = %s
        """, (request.session.get('uid'),), fetch=True)
    if request.method == 'POST':
        image = request.FILES.get('image')
        pname = request.POST.get('pname')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        tags = request.POST.get('tags', '')  # comma-separated
        promo_code = request.POST.get('promo_code')  # may be '' or a valid code
        sid = request.session['uid']

        # Generate PID
        next_id = execute_query(
                """
                SELECT LPAD(COUNT(*)+1, 9, '0') AS next_id FROM PRODUCT
                """, fetch=True)[0]['next_id']
        pid = f"P{next_id}"

        sql = "INSERT INTO PRODUCT (PID, PName, Category, Price, Descript, Stock, SID"
        values = "VALUES (%s, %s, %s, %s, %s, %s, %s"
        params = [pid, pname, category, price, description, stock, sid]

        if image:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'product_image')  # MEDIA_ROOT/product_image/
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, image.name)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_path = os.path.join('media/product_image', image.name)  # Store relative path
            sql += ", ImagePath)"
            values += ", %s)"
            params += [image_path]
        else:
            sql += ")"
            values += ")"

        execute_query(f"{sql} {values}", params)

        # Insert tags
        for tag in [t.strip() for t in tags.split(',') if t.strip()]:
            execute_query("INSERT INTO PRODUCT_TAG (PID, Tag) VALUES (%s, %s)", (pid, tag))
        # Associate promotion if selected
        if promo_code:
            execute_query("INSERT INTO HAS_PROMO (PID, PromoCode) VALUES (%s, %s)", (pid, promo_code))
        messages.success(request, 'Product added successfully.')

    return render(request, 'seller/addproduct.html', {'promotions': promotions})


@role_required('seller')
def manage_products(request):
    sid = request.session['uid']
    sql = """
        SELECT P.PID,
               P.PName,
               P.Category,
               P.Price,
               P.Stock,
               P.ImagePath,
               Pr.DisAmount,
               GROUP_CONCAT(DISTINCT PT.Tag SEPARATOR ', ') AS Tags,
               GROUP_CONCAT(DISTINCT Pr.PromoCode SEPARATOR ', ') AS PromoCodes
        FROM PRODUCT P
        LEFT JOIN PRODUCT_TAG PT ON P.PID = PT.PID
        LEFT JOIN HAS_PROMO HP ON P.PID = HP.PID
        LEFT JOIN PROMOTION Pr ON HP.PromoCode = Pr.PromoCode
        WHERE P.SID = %s
        GROUP BY P.PID, P.PName, P.Category, P.Price, P.Stock, Pr.DisAmount
    """
    products = execute_query(sql, (sid,), fetch=True)
    return render(request, 'seller/manage.html', {'products': products})


@role_required('seller')
def product_detail_s(request, pid):
    # only allow access to the product if the user is the one who possess it
    sid = request.session['uid']
    if not check_permission(sid=sid, pid=pid):
        return HttpResponseForbidden("You do not have permission to view this product.")

    product = execute_query(
        """
        SELECT P.PID,
               P.PName,
               P.Category,
               P.Price,
               P.Stock,
               P.Descript,
               P.ImagePath,
               GROUP_CONCAT(DISTINCT PT.Tag SEPARATOR ', ') AS Tags,
               GROUP_CONCAT(DISTINCT CONCAT(Pr.PromoCode, ' - NT$', Pr.DisAmount) SEPARATOR ', ') AS Promotions
        FROM PRODUCT P
        LEFT JOIN PRODUCT_TAG PT ON P.PID = PT.PID
        LEFT JOIN HAS_PROMO HP ON P.PID = HP.PID
        LEFT JOIN PROMOTION Pr ON HP.PromoCode = Pr.PromoCode
        WHERE P.PID = %s
        GROUP BY P.PID, P.PName, P.Category, P.Price, P.Stock, P.Descript
        """,
        (pid,), fetch=True
    )[0]
    reviews = execute_query(
        "SELECT Sell_R AS seller_review, Buy_R AS buyer_review FROM REVIEW WHERE PID = %s",
        (pid,), fetch=True
    )
    return render(request, 'seller/product_detail_s.html', {
        'product': product,
        'reviews': reviews
    })


@role_required('seller')
def edit_product(request, pid):
    # only allow access to the product if the user is the one who possess it
    sid = request.session['uid']
    if not check_permission(sid=sid, pid=pid):
        return HttpResponseForbidden("You do not have permission to view this product.")
    
    # fetch existing tags and promotions
    existing_tags = execute_query("SELECT Tag FROM PRODUCT_TAG WHERE PID = %s", (pid,), fetch=True)
    existing_tags = ', '.join([t['Tag'] for t in existing_tags])
    promotions = execute_query("SELECT PromoCode, DisAmount FROM PROMOTION", fetch=True)
    current_promo = execute_query("SELECT PromoCode FROM HAS_PROMO WHERE PID = %s", (pid,), fetch=True)
    current_promo = current_promo[0]['PromoCode'] if current_promo else ''
    if request.method == 'POST':
        image = request.FILES.get('image')
        pname = request.POST.get('pname')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        tags = request.POST.get('tags', '')
        promo_code = request.POST.get('promo_code')

        sql = "UPDATE PRODUCT SET PName=%s, Category=%s, Price=%s, Descript=%s, Stock=%s"
        params = [pname, category, price, description, stock]

        if image:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'product_image')  # MEDIA_ROOT/product_image/
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, image.name)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_path = os.path.join('media/product_image', image.name)  # Store relative path
            print(image_path)
            sql += ", ImagePath=%s"
            params += [image_path]

        sql += " WHERE PID=%s"
        params += [pid]

        execute_query(sql, params=params)

        # update tags
        execute_query("DELETE FROM PRODUCT_TAG WHERE PID = %s", (pid,))
        for tag in [t.strip() for t in tags.split(',') if t.strip()]:
            execute_query("INSERT INTO PRODUCT_TAG (PID, Tag) VALUES (%s, %s)", (pid, tag))
        # update promotion
        execute_query("DELETE FROM HAS_PROMO WHERE PID = %s", (pid,))
        if promo_code:
            execute_query("INSERT INTO HAS_PROMO (PID, PromoCode) VALUES (%s, %s)", (pid, promo_code))
        messages.success(request, 'Product updated successfully.')
        # return redirect(f'/hahalife/seller/product/{pid}/')
        return redirect(request.path)
    
    product = execute_query("SELECT * FROM PRODUCT WHERE PID = %s", (pid,), fetch=True)[0]
    return render(request, 'seller/edit.html', {
        'product': product,
        'tags': existing_tags,
        'promotions': promotions,
        'current_promo': current_promo
    })


@role_required('seller')
def delete_product(request, pid):
    # only allow access to the product if the user is the one who possess it
    sid = request.session['uid']
    if not check_permission(sid=sid, pid=pid):
        return HttpResponseForbidden("You do not have permission to delete this product.")

    execute_query("DELETE FROM PRODUCT WHERE PID = %s", (pid,))
    messages.success(request, 'Product deleted successfully.')
    return redirect('manage_products')


@role_required('seller')
def add_promotion(request):
    sid = request.session['uid']

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        promo_code = request.POST.get('promo_code')
        dis_amount = request.POST.get('dis_amount')

        if action == 'add':
            # Check if promotion code already exists
            existing = execute_query(
                "SELECT PromoCode FROM PROMOTION WHERE PromoCode = %s",
                (promo_code,),
                fetch=True
            )

            if existing:
                messages.error(request, 'Promotion code already exists.')
                return redirect('/hahalife/seller/promotion/')

            execute_query(
                "INSERT INTO PROMOTION (PromoCode, DisAmount, SID) VALUES (%s, %s, %s)",
                (promo_code, dis_amount, sid)
            )
            messages.success(request, 'Promotion added successfully.')

        elif action == 'edit':
            # Check if seller owns the promotion
            owner = execute_query(
                "SELECT SID FROM PROMOTION WHERE PromoCode = %s",
                (promo_code,),
                fetch=True
            )

            if not owner or owner[0]['SID'] != sid:
                messages.error(request, 'You can only edit your own promotions.')
                return redirect('/hahalife/seller/promotion/')

            execute_query(
                "UPDATE PROMOTION SET DisAmount = %s WHERE PromoCode = %s AND SID = %s",
                (dis_amount, promo_code, sid)
            )
            messages.success(request, 'Promotion updated successfully.')

        elif action == 'delete':
            # Check if seller owns the promotion
            owner = execute_query(
                "SELECT SID FROM PROMOTION WHERE PromoCode = %s",
                (promo_code,),
                fetch=True
            )

            if not owner or owner[0]['SID'] != sid:
                messages.error(request, 'You can only delete your own promotions.')
                return redirect('/hahalife/seller/promotion/')

            execute_query(
                "DELETE FROM PROMOTION WHERE PromoCode = %s AND SID = %s",
                (promo_code, sid)
            )
            messages.success(request, 'Promotion deleted successfully.')

        return redirect('/hahalife/seller/promotion/')

    promotions = execute_query(
        """
        SELECT P.*, CASE WHEN P.SID = %s THEN 1 ELSE 0 END as is_owner 
        FROM PROMOTION P
        ORDER BY PromoCode
        """,
        (sid,),
        fetch=True
    )
    return render(request, 'seller/promotion.html', {'promotions': promotions})

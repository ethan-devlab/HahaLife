# coding=utf-8

from django.shortcuts import render, redirect
from ..utils import execute_query, role_required


@role_required('member')
def notification_view(request):
    uid = request.session.get('uid')
    # if not uid:
    #     return redirect('/hahalife/login/')

    notifications = execute_query(
        """
        SELECT NID, OID, Message, NotifyTime, IsRead
        FROM NOTIFICATION
        WHERE MID = %s
        ORDER BY NotifyTime DESC
        """,
        (uid,), fetch=True
    )
    return render(request, 'member/notification.html', {'notifications': notifications})


@role_required('member')
def mark_read(request, nid):
    uid = request.session.get('uid')
    # if not uid:
    #     return redirect('/hahalife/login/')

    execute_query(
        "UPDATE NOTIFICATION SET IsRead = TRUE WHERE NID = %s AND MID = %s",
        (nid, uid)
    )
    return redirect('/hahalife/notification/')

# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from django.contrib import messages


@role_required('admin')
def review_applicant(request):
    applicants = execute_query("SELECT * FROM APPLICANT", fetch=True)
    if request.method == 'POST':
        appid = request.POST['appid']
        action = request.POST['action']  # 'approve' or 'reject'
        comment = request.POST.get('comment', '')
        uid = request.session['uid']

        status = 'Approved' if action == 'approve' else 'Disapproved'
        execute_query("UPDATE APPLICANT SET Status=%s, RevComment=%s, AID=%s WHERE AppID=%s",
                      (status, comment, uid, appid))

        if action == 'approve':
            appl = execute_query(
                """
                SELECT Name, Email, PhoneNumber, Password FROM APPLICANT WHERE AppID=%s
                """, (appid,), fetch=True)[0]

            next_id = execute_query(
                    """
                        SELECT LPAD(COUNT(*)+1, 9, '0') AS next_id FROM SELLER
                        """, fetch=True)[0]['next_id']
            sid_new = f"S{next_id}"

            execute_query("INSERT INTO SELLER (UID, UName, AccStatus, Password, Email) VALUES (%s,%s,'Active',%s,%s)",
                          (sid_new, appl['Name'], appl['Password'], appl['Email']))
            if appl['PhoneNumber']:
                execute_query("UPDATE SELLER SET PhoneNumber=%s WHERE UID=%s",
                              (appl['PhoneNumber'], sid_new))
            messages.success(request, f"Applicant {appid} approved. Seller ID: {sid_new}, Password: {appl['Password']}")

        else:
            messages.info(request, f"Applicant {appid} disapproved.")

        return redirect('review_applicant')

    return render(request, 'customadmin/review_applicant.html', {'applicants': applicants})
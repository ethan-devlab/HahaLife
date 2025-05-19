# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import execute_query, role_required
from django.utils import timezone
from django.contrib import messages


def apply_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        app_date = timezone.now().date().strftime('%Y-%m-%d')

        next_id = execute_query(
            "SELECT LPAD(COUNT(*)+1, 7, '0') AS next_appid FROM APPLICANT", fetch=True
        )[0]['next_appid']
        appid = f"APP{next_id}"

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'applicant/apply.html')

        # Check if the email already exists
        existing_applicant = execute_query(
            "SELECT * FROM APPLICANT WHERE Email=%s", (email,), fetch=True
        )
        if existing_applicant:
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'applicant/apply.html')

        # Check if the phone number already exists
        existing_phone = execute_query(
            "SELECT * FROM APPLICANT WHERE PhoneNumber=%s", (phone,), fetch=True
        )
        if existing_phone:
            messages.error(request, 'Phone number already exists. Please use a different phone number.')
            return render(request, 'applicant/apply.html')

        try:
            execute_query(
                "INSERT INTO APPLICANT (AppID, SID, Status, Name, Email, AppDate, Password) "
                "VALUES (%s, NULL, 'Pending', %s, %s, %s, %s)",
                (appid, name, email, app_date, password)
            )
            if phone:
                execute_query(
                    "UPDATE APPLICANT SET PhoneNumber=%s WHERE AppID=%s",
                    (phone, appid)
                )
            return redirect('apply_success')
        except Exception as e:
            messages.error(request, 'Submission failed: ' + str(e))
    return render(request, 'applicant/apply.html')


def apply_success(request):
    return render(request, 'applicant/apply_success.html')


@role_required('applicant')
def apply_status(request):
    uid = request.session.get('uid')
    # if not uid:
    #     return redirect('/hahalife/login/')

    applicant = execute_query(
        "SELECT * FROM APPLICANT WHERE AppID=%s", (uid,), fetch=True
    )
    if not applicant:
        messages.error(request, 'No application found.')
        return redirect('/hahalife/')

    applicant[0]['RevComment'] = applicant[0]['RevComment'] or ""

    return render(request, 'applicant/apply_status.html', {'applicant': applicant[0]})
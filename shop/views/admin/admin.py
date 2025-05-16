# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import role_required


@role_required('admin')
def dashboard(request):
    # if request.session.get('role') != 'admin':
    #     return redirect('/hahalife/login/')
    return render(request, 'customadmin/dashboard.html')

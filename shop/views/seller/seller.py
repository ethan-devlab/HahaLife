# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import role_required


@role_required('seller')
def dashboard(request):
    # if request.session.get('role') != 'seller':
    #     return redirect('/hahalife/login/')
    return render(request, 'seller/dashboard.html')

# coding=utf-8

from django.shortcuts import render, redirect
from ...utils import role_required


@role_required('admin')
def dashboard(request):
    return render(request, 'customadmin/dashboard.html')

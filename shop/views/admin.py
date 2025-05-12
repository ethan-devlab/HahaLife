# coding=utf-8

from django.shortcuts import render, redirect

def dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('/hahalife/login/')
    return render(request, 'admin/dashboard.html')

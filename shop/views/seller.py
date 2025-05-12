# coding=utf-8

from django.shortcuts import render, redirect

def dashboard(request):
    if request.session.get('role') != 'seller':
        return redirect('/hahalife/login/')
    return render(request, 'seller/dashboard.html')

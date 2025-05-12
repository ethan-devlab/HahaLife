# coding=utf-8

from django.shortcuts import render, redirect


def dashboard(request):
    if request.session.get('role') != 'member':
        return redirect('/hahalife/login/')
    return render(request, 'member/index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from product_program.models import ProductProgram
from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'admin':
                return redirect('admin_panel')
            elif user.user_type == 'worker':
                return redirect('program_select')
            else:
                return render(request, 'login.html', {'error': '사용자 권한이 올바르지 않습니다.'})
        else:
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def scan_view(request):
    return render(request, 'program_select.html')


@login_required
def admin_panel(request):
    return render(request, 'admin_panel.html')

@login_required
def program_select(request):
    programs = ProductProgram.objects.filter(is_deleted=False, is_active=True)
    return render(request, 'program_select.html', {'programs': programs})


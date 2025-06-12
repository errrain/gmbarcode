from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from product_program.models import ProductProgram
from product_info.models import Product
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

@login_required
def barcode_redirect_view(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        try:
            product = Product.objects.get(product_barcode=barcode)
            return redirect('product_check:barcode_check', product.id)
        except Product.DoesNotExist:
            return render(request, 'program_select.html', {
                'programs': ProductProgram.objects.filter(is_deleted=False, is_active=True),
                'error': '해당 바코드에 일치하는 제품이 없습니다.'
            })
    return redirect('program_select')

@login_required
def barcode_lookup_api(request):
    barcode = request.GET.get('barcode')
    if not barcode:
        return JsonResponse({'success': False, 'message': '바코드가 비어 있습니다.'})

    try:
        product = Product.objects.get(product_barcode=barcode)
        return JsonResponse({'success': True, 'product_id': product.id})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': '일치하는 제품이 없습니다.'})
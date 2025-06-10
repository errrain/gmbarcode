# product_check/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from product_check.models import BarcodeCheckLog
from product_info.models import Product
from product_program.models import ProductProgram

def product_list(request, program_id=1):
    program = get_object_or_404(ProductProgram, pk=program_id)
    products = Product.objects.filter(program=program, is_deleted=False)
    return render(request, 'product_check/check_list.html', {
        'program': program,
        'products': products,
    })

def barcode_check(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_deleted=False)
    return render(request, 'product_check/barcode_check.html', {
        'product': product,
    })

@csrf_exempt  # Ajax로만 사용, 필요시 csrf 적용 가능
def save_error_log(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        check_type = request.POST.get("check_type")  # 'mix' or 'box'
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"result": "not_found"}, status=404)
        user = request.user if request.user.is_authenticated else None

        BarcodeCheckLog.objects.create(
            check_type=check_type,
            product=product,
            result='오류',
            user=user
        )
        return JsonResponse({"result": "ok"})
    return JsonResponse({"result": "invalid"}, status=400)


@csrf_exempt  # Ajax 전용, CSRF 토큰이 없는 경우 대비
def save_success_log(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        check_type = request.POST.get("check_type")  # 'mix' or 'box'
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"result": "not_found"}, status=404)

        user = request.user if request.user.is_authenticated else None

        BarcodeCheckLog.objects.create(
            check_type=check_type,
            product=product,
            result='정상',  # 기존 '오류'와 구분
            user=user
        )
        return JsonResponse({"result": "ok"})

    return JsonResponse({"result": "invalid"}, status=400)

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from product_info.models import Product
from .models import ShippingSession

from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from .models import ShippingLog
from django.utils.dateparse import parse_date


# ✅ 출하 홈
def shipping_home(request):
    box_barcode = request.GET.get("box_barcode")
    product = None
    if box_barcode:
        try:
            product = Product.objects.get(box_barcode=box_barcode, is_deleted=False)
        except Product.DoesNotExist:
            product = None

    return render(request, 'shipping/shipping_home.html', {
        'box_barcode': box_barcode,
        'product': product
    })


# ✅ 검사 시작
def start_check(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id, is_deleted=False)
        user = request.user if request.user.is_authenticated else None

        # 세션 생성
        session = ShippingSession.objects.create(
            product=product,
            user=user,
            pallet_count=0,
            box_count=0
        )
        return redirect('shipping:scan_box', session_id=session.id)

    return redirect('shipping:shipping_home')


# ✅ 바코드 스캔 진행 화면
def scan_box(request, session_id):
    session = get_object_or_404(ShippingSession, id=session_id)
    message = ""
    status = ""

    if request.method == "POST":
        scanned_code = request.POST.get("scanned_code")

        if scanned_code == session.product.box_barcode:
            # 정상
            session.box_count += 1

            # 파레트 수량 증가 조건 확인
            if session.box_count % session.product.pallet_box_quantity == 0:
                session.pallet_count += 1

            message = "정상"
            status = "success"
        else:
            # 오류
            message = "오류 - 바코드 불일치"
            status = "error"

        session.checked_at = timezone.now()
        session.save()

    return render(request, 'shipping/scan_box.html', {
        'session': session,
        'message': message,
        'status': status
    })

@csrf_exempt
def save_shipping_log(request, session_id):
    if request.method == "POST":
        session = get_object_or_404(ShippingSession, id=session_id)

        try:
            box_count = int(request.POST.get("box_count", session.box_count))
            pallet_count = int(request.POST.get("pallet_count", session.pallet_count))
        except (ValueError, TypeError):
            return JsonResponse({"status": "error", "message": "유효하지 않은 데이터입니다."}, status=400)

        session.box_count = box_count
        session.pallet_count = pallet_count
        session.save()

        # ✅ 출하 이력 저장
        ShippingLog.objects.create(
            product=session.product,
            user=session.user,
            box_count=box_count,
            pallet_count=pallet_count
        )

        return JsonResponse({"status": "ok", "message": "출하 점검 저장 완료!"})
    return JsonResponse({"status": "error", "message": "허용되지 않은 요청 방식입니다."}, status=405)

def shipping_log_list(request):
    # 🔎 필터링 파라미터 받기
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    product = request.GET.get("product", "")
    user = request.GET.get("user", "")
    download = request.GET.get("download")

    logs = ShippingLog.objects.all().order_by("-created_at")

    if start_date:
        logs = logs.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        logs = logs.filter(created_at__date__lte=parse_date(end_date))
    if product:
        logs = logs.filter(product__name__icontains=product)
    if user:
        logs = logs.filter(user__full_name__icontains=user)

    # ⬇️ 엑셀 다운로드 기능
    if download == "xls":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shipping_logs.csv"'

        writer = csv.writer(response)
        writer.writerow(["출하점검일시", "제품명", "박스수", "파레트수", "작업자"])

        for log in logs:
            writer.writerow([
                log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else '',
                log.product.name if log.product else '',
                log.box_count,
                log.pallet_count,
                log.user.full_name if log.user else '',
            ])
        return response

    # 📄 페이지네이션
    paginator = Paginator(logs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'shipping/shipping_log_list.html', {
        'logs': page_obj.object_list,
        'page_obj': page_obj,
    })
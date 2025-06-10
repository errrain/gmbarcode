# check_log_viewer/views.py
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from product_check.models import BarcodeCheckLog

def log_list(request):
    logs = BarcodeCheckLog.objects.select_related('product', 'user').all()

    # ✅ 필터 처리
    result = request.GET.get("result")
    product_name = request.GET.get("product")
    user_name = request.GET.get("user")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if result:
        logs = logs.filter(result=result)
    if product_name:
        logs = logs.filter(product__name__icontains=product_name)
    if user_name:
        logs = logs.filter(
            user__username__icontains=user_name
        ) | logs.filter(
            user__full_name__icontains=user_name
        )
    if start_date:
        logs = logs.filter(checked_at__date__gte=start_date)
    if end_date:
        logs = logs.filter(checked_at__date__lte=end_date)

    logs = logs.order_by('-checked_at')

    # ✅ 엑셀 다운로드 처리
    if request.GET.get("download") == "xls":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="barcode_logs.csv"'
        # UTF-8 BOM 추가
        response.write('\ufeff')  # <- 이 부분이 핵심!

        writer = csv.writer(response)
        writer.writerow(['점검시간', '점검구분', '제품명', '작업자', '결과'])
        for log in logs:
            writer.writerow([
                log.checked_at.strftime('%Y-%m-%d %H:%M:%S'),
                log.get_check_type_display(),
                log.product.name,
                getattr(log.user, 'full_name', log.user.username if log.user else '미등록'),
                log.result
            ])
        return response

    # ✅ 페이징 처리
    paginator = Paginator(logs, 20)  # 20개씩 나눔
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'check_log_viewer/log_list.html', {
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'paginator': paginator,
        'request': request,  # 템플릿에서 파라미터 접근을 위해 추가
    })

from django.urls import path, include
from .views import (
    login_view,
    logout_view,
    scan_view,
    admin_panel,
    program_select,  # ✅ 추가
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('scan/', scan_view, name='scan_view'),  # 유지 or 삭제
    path('program-select/', program_select, name='program_select'),  # ✅ 추가
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('logout/', logout_view, name='logout'),
    path('programs/', include('product_program.urls')),  # ✅ product_program 연결
    path('product-info/', include('product_info.urls')),     # 💥 제품 정보 관리 추가
    path('product-check/', include('product_check.urls')),   # ← 이 줄이 반드시 있어야 함!




]
